import streamlit as st
import pandas as pd

def show_settings():
    st.title("⚙️ Settings")
    
    # Create tabs for different settings
    tabs = st.tabs(["General", "Trading", "Notifications", "API Keys"])
    
    with tabs[0]:
        st.subheader("General Settings")
        
        # Theme Settings
        st.markdown("### Theme")
        st.selectbox(
            "Color Theme",
            ["Dark (Default)", "Light", "Auto"],
            index=0
        )
        
        st.selectbox(
            "Chart Style",
            ["Tesla Modern", "Classic", "Minimalist"],
            index=0
        )
        
        # Data Update Settings
        st.markdown("### Data Updates")
        st.slider(
            "Real-time Data Refresh Rate (seconds)",
            min_value=1,
            max_value=60,
            value=5
        )
        
        st.multiselect(
            "Default Assets to Track",
            ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN", "BTC-USD", "ETH-USD"],
            ["AAPL", "TSLA"]
        )
    
    with tabs[1]:
        st.subheader("Trading Settings")
        
        # Risk Management
        st.markdown("### Risk Management")
        st.number_input(
            "Default Position Size (%)",
            min_value=1,
            max_value=100,
            value=5
        )
        
        st.number_input(
            "Stop Loss (%)",
            min_value=1,
            max_value=50,
            value=10
        )
        
        st.number_input(
            "Take Profit (%)",
            min_value=1,
            max_value=1000,
            value=25
        )
        
        # Trading Preferences
        st.markdown("### Trading Preferences")
        st.selectbox(
            "Default Order Type",
            ["Market", "Limit", "Stop", "Stop Limit"]
        )
        
        st.selectbox(
            "Time in Force",
            ["Day", "GTC", "IOC", "FOK"]
        )
        
        st.checkbox("Enable One-Click Trading", value=False)
        st.checkbox("Confirm Orders", value=True)
    
    with tabs[2]:
        st.subheader("Notification Settings")
        
        # Alert Settings
        st.markdown("### Alert Settings")
        st.multiselect(
            "Alert Types",
            ["Price Alerts", "Technical Indicators", "News", "Risk Warnings", "Trade Execution"],
            ["Price Alerts", "Risk Warnings"]
        )
        
        st.selectbox(
            "Alert Method",
            ["In-App", "Email", "SMS", "All"]
        )
        
        # Custom Alerts
        st.markdown("### Custom Price Alerts")
        alerts = pd.DataFrame({
            'Asset': ['AAPL', 'TSLA', 'BTC-USD'],
            'Type': ['Above', 'Below', 'Change %'],
            'Value': ['$180', '$150', '5%'],
            'Status': ['Active', 'Active', 'Active']
        })
        
        st.dataframe(alerts, hide_index=True)
        
        # Add New Alert
        st.button("Add New Alert")
    
    with tabs[3]:
        st.subheader("API Settings")
        
        # API Configuration
        st.markdown("### Trading APIs")
        
        # Binance API
        st.text_input("Binance API Key", type="password")
        st.text_input("Binance Secret Key", type="password")
        
        # Finnhub API
        st.text_input("Finnhub API Key", type="password")
        
        # Alpha Vantage API
        st.text_input("Alpha Vantage API Key", type="password")
        
        # OpenAI API
        st.text_input("OpenAI API Key", type="password")
        
        st.button("Save API Keys")
        
        st.info("API keys are encrypted and stored securely. Never share your API keys with anyone.")
    
    # Save Settings Button
    st.button("Save All Settings", type="primary")