import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from models.esg_analyzer import ESGAnalyzer

def show_esg_analysis():
    st.title("🌍 ESG Analysis")
    
    # Initialize ESG analyzer
    esg = ESGAnalyzer()
    
    # Company selection
    company = st.selectbox(
        "Select company to analyze",
        ["Tesla", "Apple", "Google", "Microsoft", "Amazon", "Meta"]
    )
    
    # Create tabs for different analyses
    tabs = st.tabs(["ESG Scores", "Sustainability Analysis", "Portfolio Impact"])
    
    with tabs[0]:
        # Generate sample ESG data
        company_data = {
            'carbon_emissions': np.random.uniform(60, 90),
            'renewable_energy': np.random.uniform(60, 90),
            'waste_management': np.random.uniform(60, 90),
            'water_usage': np.random.uniform(60, 90),
            'biodiversity': np.random.uniform(60, 90),
            'employee_satisfaction': np.random.uniform(60, 90),
            'diversity_inclusion': np.random.uniform(60, 90),
            'community_relations': np.random.uniform(60, 90),
            'human_rights': np.random.uniform(60, 90),
            'health_safety': np.random.uniform(60, 90),
            'board_independence': np.random.uniform(60, 90),
            'shareholder_rights': np.random.uniform(60, 90),
            'executive_compensation': np.random.uniform(60, 90),
            'business_ethics': np.random.uniform(60, 90),
            'transparency': np.random.uniform(60, 90)
        }
        
        # Calculate ESG scores
        scores = esg.calculate_esg_score(company_data)
        
        # Display overall score
        st.metric(
            "Overall ESG Score",
            f"{scores['total_score']:.1f}",
            "+5.2",
            help="Combined ESG score out of 100"
        )
        
        # Display component scores
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Environmental",
                f"{scores['component_scores']['environmental']:.1f}",
                "+3.5",
                help="Environmental score out of 100"
            )
        with col2:
            st.metric(
                "Social",
                f"{scores['component_scores']['social']:.1f}",
                "+2.8",
                help="Social score out of 100"
            )
        with col3:
            st.metric(
                "Governance",
                f"{scores['component_scores']['governance']:.1f}",
                "+4.2",
                help="Governance score out of 100"
            )
        
        # Create radar chart for detailed scores
        categories = list(company_data.keys())
        values = list(company_data.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=company
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[1]:
        # Analyze sustainability reports
        st.subheader("Sustainability Report Analysis")
        
        # Sample sustainability metrics
        metrics = pd.DataFrame({
            'Metric': [
                'Carbon Emissions (tons)',
                'Renewable Energy Usage',
                'Water Consumption',
                'Waste Recycled',
                'Employee Diversity'
            ],
            'Value': [
                '125,000',
                '78%',
                '1.2M gallons',
                '85%',
                '42%'
            ],
            'Change': [
                '-12%',
                '+15%',
                '-8%',
                '+5%',
                '+10%'
            ]
        })
        
        st.dataframe(metrics, hide_index=True)
        
        # Key initiatives
        st.subheader("Key Sustainability Initiatives")
        
        initiatives = pd.DataFrame({
            'Initiative': [
                'Carbon Neutrality Program',
                'Renewable Energy Transition',
                'Diversity & Inclusion',
                'Supply Chain Sustainability'
            ],
            'Status': [
                'In Progress',
                'Completed',
                'In Progress',
                'Planning'
            ],
            'Target Date': [
                '2025',
                '2024',
                '2024',
                '2026'
            ]
        })
        
        st.dataframe(initiatives, hide_index=True)
    
    with tabs[2]:
        st.subheader("Portfolio ESG Impact")
        
        # Sample portfolio allocation
        portfolio = {
            'TSLA': 0.3,
            'AAPL': 0.2,
            'GOOGL': 0.2,
            'MSFT': 0.15,
            'AMZN': 0.15
        }
        
        # Sample company scores
        company_scores = {
            'TSLA': {
                'total_score': 85,
                'component_scores': {
                    'environmental': 90,
                    'social': 80,
                    'governance': 85
                }
            },
            'AAPL': {
                'total_score': 88,
                'component_scores': {
                    'environmental': 85,
                    'social': 90,
                    'governance': 90
                }
            },
            'GOOGL': {
                'total_score': 82,
                'component_scores': {
                    'environmental': 80,
                    'social': 85,
                    'governance': 80
                }
            },
            'MSFT': {
                'total_score': 90,
                'component_scores': {
                    'environmental': 90,
                    'social': 90,
                    'governance': 90
                }
            },
            'AMZN': {
                'total_score': 78,
                'component_scores': {
                    'environmental': 75,
                    'social': 80,
                    'governance': 80
                }
            }
        }
        
        # Calculate portfolio impact
        impact = esg.calculate_portfolio_esg_impact(portfolio, company_scores)
        
        # Display impact metrics
        st.metric(
            "Portfolio ESG Score",
            f"{impact['total_score']:.1f}",
            "+3.5",
            help="Overall portfolio ESG score"
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Carbon Footprint",
                "Low",
                "-15%",
                help="Portfolio carbon impact"
            )
        with col2:
            st.metric(
                "Social Impact",
                "High",
                "+12%",
                help="Portfolio social impact"
            )
        with col3:
            st.metric(
                "Governance Quality",
                "Strong",
                "+8%",
                help="Portfolio governance quality"
            )
        
        # Portfolio allocation chart
        fig = px.pie(
            values=list(portfolio.values()),
            names=list(portfolio.keys()),
            title="Portfolio Allocation",
            hole=0.4
        )
        
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)