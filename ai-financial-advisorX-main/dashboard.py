import streamlit as st

def render_dashboard(generate_btn=False):
    """
    Renders the Enhanced Output Display containing the financial dashboard metrics and progress indicators.
    
    Args:
        generate_btn (bool): The state of the generate button to trigger analysis.
    """
    # MAIN CONTENT AREA
    if 'user_data' in st.session_state and st.session_state.user_data and st.session_state.user_data.get('income', 0) > 0:
        
        # When user clicks the generate button, call the analysis functions.
        # Ensure these functions exist in your main app when merging files!
        if generate_btn:
            # st.session_state.analysis_data = analyze_finances(st.session_state.user_data)
            # st.session_state.generated_advice = generate_financial_advice(
            #     st.session_state.user_data,
            #     st.session_state.analysis_data
            # )
            pass # Placeholder - to be integrated with real functions later
            
        if 'analysis_data' in st.session_state and st.session_state.analysis_data:
            ad = st.session_state.analysis_data
            
            # Key Metrics row 1
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class='card' style='background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6; text-align: center; height: 100%;'>
                    <h5 style='color: #6c757d; margin-bottom: 5px; font-size: 1rem;'>Total Income</h5>
                    <h3 style='color: #28a745; margin: 0;'>${ad.get('total_income', 0):,.2f}</h3>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class='card' style='background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6; text-align: center; height: 100%;'>
                    <h5 style='color: #6c757d; margin-bottom: 5px; font-size: 1rem;'>Total Expenses</h5>
                    <h3 style='color: #dc3545; margin: 0;'>${ad.get('total_expenses', 0):,.2f}</h3>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class='card' style='background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6; text-align: center; height: 100%;'>
                    <h5 style='color: #6c757d; margin-bottom: 5px; font-size: 1rem;'>Net Savings</h5>
                    <h3 style='color: #007bff; margin: 0;'>${ad.get('net_savings', 0):,.2f}</h3>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class='card' style='background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6; text-align: center; height: 100%;'>
                    <h5 style='color: #6c757d; margin-bottom: 5px; font-size: 1rem;'>Savings Rate</h5>
                    <h3 style='color: #17a2b8; margin: 0;'>{ad.get('savings_rate', 0):.1f}%</h3>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown(" ")
            st.markdown(" ")
            
            # Additional metrics row 2
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class='card' style='background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 4px solid #fd7e14; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <h5 style='color: #495057; margin-bottom: 5px; font-size: 1rem;'>Debt-to-Income</h5>
                    <h4 style='color: #fd7e14; margin: 0;'>{ad.get('debt_to_income', 0):.1f}%</h4>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class='card' style='background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 4px solid #6f42c1; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <h5 style='color: #495057; margin-bottom: 5px; font-size: 1rem;'>Emergency Fund</h5>
                    <h4 style='color: #6f42c1; margin: 0;'>{ad.get('emergency_fund_months', 0):.1f} Months</h4>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class='card' style='background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 4px solid #20c997; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <h5 style='color: #495057; margin-bottom: 5px; font-size: 1rem;'>Discretionary</h5>
                    <h4 style='color: #20c997; margin: 0;'>${ad.get('discretionary_income', 0):,.2f}</h4>
                </div>
                """, unsafe_allow_html=True)
                
            # Progress Indicators
            st.markdown(" ")
            st.markdown(" ")
            st.markdown("#### Financial Health Indicators")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Savings Rate Progress** (Goal: 20%)")
                # Clamp the value between 0.0 and 1.0 for Streamlit progress bar
                savings_progress = min(max(ad.get('savings_rate', 0) / 20.0, 0.0), 1.0)
                st.progress(savings_progress)
                
            with col2:
                st.markdown("**Emergency Fund Status** (Goal: 6 Months)")
                emergency_progress = min(max(ad.get('emergency_fund_months', 0) / 6.0, 0.0), 1.0)
                st.progress(emergency_progress)
                
            st.markdown("---")


def render_about_tool():
    """
    Renders the 'About Tool' section, summarizing the purpose, use case, and technologies.
    """
    st.markdown("---")
    st.markdown("### ℹ️ About This Tool")
    
    # Custom styled card for the About section
    st.markdown("""
    <div style='background-color: #f0f7ff; padding: 20px; border-radius: 10px; border-left: 5px solid #0056b3;'>
        <p style='font-size: 1.1em; color: #333;'>
            <strong>AI Financial Advisor Dashboard</strong>
        </p>
        <p style='color: #555; line-height: 1.6;'>
            This tool functions as an intelligent virtual financial assistant. It analyzes your financial inputs—such as income, expenses, and savings goals—to provide personalized, data-driven recommendations and organize your information into clear, actionable insights.
        </p>
        
        <h5 style='color: #0056b3; margin-top: 15px;'>Key Features:</h5>
        <ul style='color: #555; line-height: 1.6;'>
            <li><strong>Summary & Metrics:</strong> Visualizes your financial health using intuitive cards and progress indicators (e.g., savings rate, debt-to-income ratio).</li>
            <li><strong>AI-Driven Insights:</strong> Leverages advanced AI models to generate tailored strategies covering debt management, budgeting, and investments.</li>
            <li><strong>Interactive Chatbot:</strong> A dedicated conversational interface for asking detailed financial questions and obtaining immediate advice.</li>
        </ul>
        
        <h5 style='color: #0056b3; margin-top: 15px;'>Technologies Used:</h5>
        <div style='display: flex; gap: 10px; margin-top: 5px;'>
            <span style='background-color: #0056b3; color: white; padding: 4px 10px; border-radius: 15px; font-size: 0.9em;'>Python</span>
            <span style='background-color: #0056b3; color: white; padding: 4px 10px; border-radius: 15px; font-size: 0.9em;'>Streamlit</span>
            <span style='background-color: #0056b3; color: white; padding: 4px 10px; border-radius: 15px; font-size: 0.9em;'>Google Gemini AI</span>
            <span style='background-color: #0056b3; color: white; padding: 4px 10px; border-radius: 15px; font-size: 0.9em;'>Pandas/Regex processing</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# To test this file individually:
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Enhanced Output Display Test")
    
    # Mock data for testing
    st.session_state.user_data = {'income': 5000}
    st.session_state.analysis_data = {
        'total_income': 5000,
        'total_expenses': 3000,
        'net_savings': 2000,
        'savings_rate': 40.0,
        'debt_to_income': 15.0,
        'emergency_fund_months': 4.5,
        'discretionary_income': 1000
    }
    
    render_dashboard(generate_btn=False)
    render_about_tool()
