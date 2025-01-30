import os
from typing import Any, Dict, Optional
from dotenv import load_dotenv
import yaml
import logging

logger = logging.getLogger(__name__)

class Environment:
    """Environment configuration manager"""
    
    def __init__(self):
        # Load .env file
        load_dotenv()
        
        # Load config.yaml
        self.config = self._load_config()
        
        # Initialize settings
        self.settings = self._initialize_settings()
        
    def _load_config(self) -> dict:
        """Load configuration from config.yaml"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config.yaml: {e}")
            return {}
            
    def _initialize_settings(self) -> Dict[str, Any]:
        """Initialize settings from environment variables and config"""
        settings = {
            # API Keys
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            
            # Cache Settings
            'cache_duration': int(os.getenv('CACHE_DURATION', 300)),
            'cache_strategy': os.getenv('CACHE_STRATEGY', 'aggressive'),
            
            # Performance Settings
            'use_gpu': os.getenv('USE_GPU', 'false').lower() == 'true',
            'num_workers': int(os.getenv('NUM_WORKERS', 4)),
            'batch_size': int(os.getenv('BATCH_SIZE', 32)),
            
            # Logging
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'log_file': os.getenv('LOG_FILE', 'quantum_trader.log'),
            
            # UI Settings
            'theme': os.getenv('THEME', 'dark'),
            'update_interval': int(os.getenv('UPDATE_INTERVAL', 1000)),
            
            # Model Settings
            'confidence_threshold': float(os.getenv('DEFAULT_CONFIDENCE_THRESHOLD', 0.95)),
            'ensemble_weights': [float(w) for w in os.getenv('ENSEMBLE_WEIGHTS', '0.3,0.3,0.2,0.2').split(',')]
        }
        
        # Update with config values if available
        if self.config:
            settings.update({
                'apis': self.config.get('apis', {}),
                'websocket': self.config.get('websocket', {}),
                'cache': self.config.get('cache', {}),
                'models': self.config.get('models', {})
            })
            
        return settings
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value by key"""
        return self.settings.get(key, default)
    
    def get_nested(self, *keys: str, default: Any = None) -> Any:
        """Get nested setting value"""
        value = self.settings
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
        return value if value is not None else default
    
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return os.getenv('ENV', 'development').lower() == 'production'
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, self.get('log_level', 'INFO')),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.get('log_file')),
                logging.StreamHandler()
            ]
        )

# Global environment instance
env = Environment()