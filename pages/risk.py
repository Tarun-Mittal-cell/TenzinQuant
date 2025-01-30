import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from services.market_data import MarketDataService
from services.ai_analyst import AIAnalyst

def show_risk_assessment():
    st.title("🎯 Risk Assessment")
    
    # Initialize services
    market_data = MarketDataService()
    ai_analyst = AIAnalyst()
    
    # Portfolio Risk Metrics
    st.subheader("Portfolio Risk Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Value at Risk (95%)",
            "$25,000",
            "-2.5%",
            help="Maximum potential loss at 95% confidence level"
        )
    with col2:
        st.metric(
            "Sharpe Ratio",
            "1.85",
            "+0.2",
            help="Risk-adjusted return metric"
        )
    with col3:
        st.metric(
            "Beta",
            "0.85",
            "-0.05",
            help="Portfolio sensitivity to market movements"
        )
    with col4:
        st.metric(
            "Max Drawdown",
            "-12.3%",
            "+1.2%",
            help="Largest peak-to-trough decline"
        )
    
    # Risk Decomposition
    st.subheader("Risk Decomposition")
    
    # Sample risk data
    risk_data = pd.DataFrame({
        'Category': ['Market Risk', 'Sector Risk', 'Currency Risk', 'Interest Rate Risk', 'Volatility Risk'],
        'Contribution': [35, 25, 15, 15, 10]
    })
    
    fig = px.pie(
        risk_data,
        values='Contribution',
        names='Category',
        title='Risk Contribution by Category',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk Alerts
    st.subheader("Risk Alerts")
    
    alerts = pd.DataFrame({
        'Asset': ['TSLA', 'AAPL', 'BTC-USD'],
        'Alert Type': ['Volatility Spike', 'Correlation Change', 'Price Anomaly'],
        'Risk Level': ['High', 'Medium', 'High'],
        'Action Required': ['Review Position', 'Monitor', 'Hedge']
    })
    
    st.dataframe(
        alerts,
        hide_index=True,
        column_config={
            'Asset': 'Asset',
            'Alert Type': 'Alert',
            'Risk Level': 'Severity',
            'Action Required': 'Recommended Action'
        }
    )
    
    # AI Risk Analysis
    st.subheader("AI Risk Analysis")
    
    # Sample portfolio data
    portfolio_data = {
        'AAPL': {'weight': 0.2, 'value': 200000},
        'TSLA': {'weight': 0.15, 'value': 150000},
        'GOOGL': {'weight': 0.15, 'value': 150000},
        'MSFT': {'weight': 0.2, 'value': 200000},
        'AMZN': {'weight': 0.15, 'value': 150000},
        'BTC-USD': {'weight': 0.15, 'value': 150000}
    }
    
    market_conditions = """
    Current market conditions show elevated volatility with VIX at 22.
    Major indices are experiencing sector rotation.
    Interest rates remain high with potential for further increases.
    """
    
    analysis = ai_analyst.analyze_portfolio_risk(portfolio_data, market_conditions)
    st.markdown(f"<div style='background-color: #1E1E1E; padding: 20px; border-radius: 10px;'>{analysis}</div>", unsafe_allow_html=True)
    
    # Risk Management Tools
    st.subheader("Risk Management Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox(
            "Hedging Strategy",
            ["Options Hedge", "Inverse ETFs", "Stop Loss", "Collar Strategy"]
        )
        
        st.slider(
            "Risk Tolerance Level",
            min_value=1,
            max_value=10,
            value=5,
            help="Adjust your portfolio risk tolerance"
        )
    
    with col2:
        st.selectbox(
            "Position Sizing Model",
            ["Fixed Fractional", "Kelly Criterion", "Equal Weight", "Risk Parity"]
        )
        
        st.number_input(
            "Maximum Position Size (%)",
            min_value=1,
            max_value=100,
            value=20,
            help="Maximum allocation for any single position"
        )
    
    # Correlation Matrix
    st.subheader("Asset Correlation Matrix")
    
    # Sample correlation data
    corr_data = pd.DataFrame(
        [[1.0, 0.5, 0.3, 0.4, 0.2],
         [0.5, 1.0, 0.4, 0.3, 0.1],
         [0.3, 0.4, 1.0, 0.5, 0.3],
         [0.4, 0.3, 0.5, 1.0, 0.4],
         [0.2, 0.1, 0.3, 0.4, 1.0]],
        columns=['AAPL', 'TSLA', 'GOOGL', 'MSFT', 'BTC'],
        index=['AAPL', 'TSLA', 'GOOGL', 'MSFT', 'BTC']
    )
    
    fig = px.imshow(
        corr_data,
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)