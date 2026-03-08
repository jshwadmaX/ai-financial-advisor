"""
AI Financial Advisor - Main Streamlit Application
Activities 3.x, 4.x, 5.x
"""

import streamlit as st
import os
from dotenv import load_dotenv

from modules.finance_analysis import (
    calculate_financial_summary,
    calculate_goal_plan,
    get_investment_allocation,
    classify_health_score,
)
from modules.ai_advisor import (
    validate_gemini_connection,
    get_financial_advice,
    chat_with_advisor,
    get_goal_advice,
)
from modules.visualization import (
    create_expense_donut,
    create_budget_bar,
    create_health_gauge,
    create_goal_progress,
    create_investment_pie,
)
from modules.utils import (
    format_currency,
    format_percentage,
    get_health_color,
    validate_inputs,
    get_financial_tips,
    get_profile_defaults,
)

load_dotenv()

# ─────────────────────────────────────────────
# Activity 3.1: Streamlit Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Load custom CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

# ─────────────────────────────────────────────
# Session State Initialization
# ─────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "financial_summary" not in st.session_state:
    st.session_state.financial_summary = None
if "ai_advice" not in st.session_state:
    st.session_state.ai_advice = None
if "api_validated" not in st.session_state:
    st.session_state.api_validated = False


# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown(
    """
<div style='text-align:center; padding: 20px 0 10px 0;'>
    <h1 style='font-size:2.8rem; background: linear-gradient(135deg, #667eea, #f093fb);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0;'>
        💰 AI Financial Advisor
    </h1>
    <p style='color:#aaa; font-size:1.1rem; margin-top:8px;'>
        Powered by Google Gemini 1.5 Flash | Personalized Financial Intelligence
    </p>
</div>
<hr style='border-color: rgba(255,255,255,0.1); margin: 0 0 20px 0;'>
""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────
# Activity 3.2: Sidebar Input System
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("#### 👤 User Profile")
    user_profile = st.selectbox(
        "Profile Type",
        ["Student", "Working Professional", "Business Owner", "Retiree"],
        index=1,
    )

    defaults = get_profile_defaults(user_profile)

    # Load defaults button
    if st.button("📋 Load Sample Data"):
        st.session_state.update(
            {
                "income_val": defaults["income"],
                "expenses_val": defaults["expenses"],
                "savings_val": defaults["savings"],
                "debts_val": defaults["debts"],
                "emi_val": defaults["emi"],
            }
        )
        st.rerun()

    st.markdown("#### 💵 Monthly Financials")
    income = st.number_input(
        "Monthly Income (₹)",
        min_value=0,
        max_value=10_000_000,
        value=st.session_state.get("income_val", defaults["income"]),
        step=1000,
    )
    expenses = st.number_input(
        "Monthly Expenses (₹)",
        min_value=0,
        max_value=10_000_000,
        value=st.session_state.get("expenses_val", defaults["expenses"]),
        step=500,
    )
    savings = st.number_input(
        "Current Savings (₹)",
        min_value=0,
        max_value=100_000_000,
        value=st.session_state.get("savings_val", defaults["savings"]),
        step=5000,
    )
    debts = st.number_input(
        "Total Outstanding Debts (₹)",
        min_value=0,
        max_value=100_000_000,
        value=st.session_state.get("debts_val", defaults["debts"]),
        step=10000,
    )
    emi = st.number_input(
        "Monthly EMI Payments (₹)",
        min_value=0,
        max_value=1_000_000,
        value=st.session_state.get("emi_val", defaults["emi"]),
        step=500,
    )

    st.markdown("#### 📊 Risk Profile")
    risk_profile = st.select_slider(
        "Investment Risk Tolerance",
        options=["Conservative", "Moderate", "Aggressive"],
        value="Moderate",
    )

    st.divider()

    # Analyze button
    analyze_btn = st.button(
        "🔍 Analyze My Finances", type="primary", use_container_width=True
    )


# ─────────────────────────────────────────────
# Run Analysis
# ─────────────────────────────────────────────
if analyze_btn:
    errors = validate_inputs(income, expenses, savings, debts)
    if errors:
        for e in errors:
            st.warning(e)
    else:
        with st.spinner("Analyzing your financial profile..."):
            summary = calculate_financial_summary(income, expenses, savings, debts, emi)
            st.session_state.financial_summary = summary
            st.session_state.ai_advice = None  # reset advice
            st.success("✅ Analysis complete! Scroll down to view your results.")


# ─────────────────────────────────────────────
# Activity 3.3: Financial Summary & Visualization
# ─────────────────────────────────────────────
if st.session_state.financial_summary:
    summary = st.session_state.financial_summary
    health_label, health_color = classify_health_score(summary["health_score"])

    st.markdown("## 📊 Financial Dashboard")

    # Key Metrics Row
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Monthly Income", format_currency(summary["income"]))
    with c2:
        st.metric(
            "Total Expenses",
            format_currency(summary["expenses"] + summary["emi"]),
            delta=f"{-summary['expense_ratio']:.1f}% of income",
            delta_color="inverse",
        )
    with c3:
        st.metric("Disposable Income", format_currency(summary["disposable_income"]))
    with c4:
        st.metric(
            "Savings Rate",
            format_percentage(summary["savings_rate"]),
            delta="Target: 20%" if summary["savings_rate"] < 20 else "✅ On Track",
        )
    with c5:
        st.metric("Health Score", f"{summary['health_score']}/100", delta=health_label)

    st.divider()

    # Charts Row 1
    col_a, col_b, col_c = st.columns([1.2, 1.2, 1])
    with col_a:
        st.plotly_chart(create_expense_donut(summary), use_container_width=True)
    with col_b:
        st.plotly_chart(create_budget_bar(summary), use_container_width=True)
    with col_c:
        st.plotly_chart(
            create_health_gauge(summary["health_score"]), use_container_width=True
        )

    # Financial Tips
    tips = get_financial_tips(summary)
    with st.expander("💡 Quick Financial Tips", expanded=True):
        for tip in tips:
            st.markdown(f"> {tip}")

    # Detailed breakdown
    with st.expander("📋 Detailed Financial Breakdown"):
        d1, d2, d3 = st.columns(3)
        with d1:
            st.markdown("**Income vs Outflow**")
            st.markdown(f"- Income: `{format_currency(summary['income'])}`")
            st.markdown(f"- Expenses: `{format_currency(summary['expenses'])}`")
            st.markdown(f"- EMI: `{format_currency(summary['emi'])}`")
            st.markdown(
                f"- Free Cash: `{format_currency(summary['disposable_income'])}`"
            )
        with d2:
            st.markdown("**Key Ratios**")
            st.markdown(
                f"- Expense Ratio: `{format_percentage(summary['expense_ratio'])}`"
            )
            st.markdown(
                f"- Savings Rate: `{format_percentage(summary['savings_rate'])}`"
            )
            st.markdown(f"- EMI Ratio: `{format_percentage(summary['emi_ratio'])}`")
            st.markdown(
                f"- Debt/Income: `{format_percentage(summary['debt_to_income'])}`"
            )
        with d3:
            st.markdown("**50/30/20 Budget**")
            st.markdown(f"- Needs (50%): `{format_currency(summary['needs_budget'])}`")
            st.markdown(f"- Wants (30%): `{format_currency(summary['wants_budget'])}`")
            st.markdown(
                f"- Savings (20%): `{format_currency(summary['savings_budget'])}`"
            )

    st.divider()

    # ─────────────────────────────────────────────
    # Activity 3.4: AI Chatbot Section
    # ─────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["🤖 AI Advice", "💬 Chat Advisor", "🎯 Goal Planner"])

    with tab1:
        st.markdown("### 🤖 Personalized AI Financial Advice")
        if st.button("✨ Generate AI Advice", use_container_width=True):
            with st.spinner("Gemini AI is analyzing your profile..."):
                advice = get_financial_advice(summary, user_profile)
                st.session_state.ai_advice = advice

        if st.session_state.ai_advice:
            st.markdown(st.session_state.ai_advice)
        else:
            st.info(
                "Click the button above to get personalized AI-powered financial advice."
            )

        # Investment Allocation
        st.markdown("### 📈 Suggested Investment Allocation")
        investable = max(0, summary["disposable_income"] - summary["savings"] * 0.5)
        if investable > 0:
            allocation = get_investment_allocation(risk_profile, investable)

            col_pie, col_table = st.columns([1, 1])
            with col_pie:
                st.plotly_chart(
                    create_investment_pie(allocation), use_container_width=True
                )
            with col_table:
                st.markdown(
                    f"**Investable Amount: {format_currency(investable)}/month**"
                )
                st.markdown(f"*Risk Profile: {risk_profile}*")
                st.markdown("---")
                for instrument, data in allocation.items():
                    st.markdown(
                        f"**{instrument}** — {data['percentage']}% = `{format_currency(data['monthly_amount'])}/mo`"
                    )
        else:
            st.warning(
                "Increase disposable income to unlock investment recommendations."
            )

    with tab2:
        st.markdown("### 💬 Chat with Your AI Financial Advisor")
        st.caption("Ask anything about your finances, investments, or goals.")

        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input
        if prompt := st.chat_input("Ask your financial advisor..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    reply = chat_with_advisor(
                        prompt,
                        summary,
                        st.session_state.chat_history[:-1],
                    )
                st.markdown(reply)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": reply}
                )

        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

    # ─────────────────────────────────────────────
    # Activity 3.5: Goal-Oriented and Advanced Planning
    # ─────────────────────────────────────────────
    with tab3:
        st.markdown("### 🎯 Goal-Based Financial Planner")

        g1, g2 = st.columns(2)
        with g1:
            goal_name = st.text_input(
                "Goal Name",
                placeholder="e.g., Buy a Car, Emergency Fund, Home Down Payment",
            )
            target_amount = st.number_input(
                "Target Amount (₹)",
                min_value=1000,
                max_value=100_000_000,
                value=500000,
                step=10000,
            )
            current_goal_savings = st.number_input(
                "Current Savings for This Goal (₹)", min_value=0, value=0, step=5000
            )
        with g2:
            years = st.slider("Time Horizon (Years)", 1, 30, 3)
            months = years * 12
            expected_return = st.slider(
                "Expected Annual Return (%)", 4.0, 18.0, 8.0, 0.5
            )

        if st.button("📐 Calculate Goal Plan", use_container_width=True):
            goal_data = calculate_goal_plan(
                target_amount, current_goal_savings, months, expected_return
            )

            if goal_data:
                st.divider()

                gm1, gm2, gm3, gm4 = st.columns(4)
                gm1.metric(
                    "Monthly Required", format_currency(goal_data["monthly_required"])
                )
                gm2.metric(
                    "Total Contributions",
                    format_currency(goal_data["total_contributions"]),
                )
                gm3.metric(
                    "Interest Earned", format_currency(goal_data["total_interest"])
                )
                gm4.metric(
                    "Feasibility",
                    (
                        "✅ Feasible"
                        if goal_data["monthly_required"]
                        <= summary["disposable_income"] * 0.5
                        else "⚠️ Stretch Goal"
                    ),
                )

                st.plotly_chart(
                    create_goal_progress(goal_data), use_container_width=True
                )

                if st.button("🤖 Get AI Goal Strategy"):
                    with st.spinner("Creating your personalized goal roadmap..."):
                        goal_advice = get_goal_advice(
                            goal_name or "Financial Goal", goal_data, summary
                        )
                    st.markdown(goal_advice)

else:
    # Welcome screen
    st.markdown(
        """
    <div style='text-align:center; padding: 60px 20px;'>
        <div style='font-size:5rem;'>💰</div>
        <h2 style='color:#667eea; margin:16px 0 8px;'>Welcome to AI Financial Advisor</h2>
        <p style='color:#aaa; font-size:1.1rem; max-width:600px; margin:0 auto;'>
            Enter your financial details in the sidebar and click <strong>"Analyze My Finances"</strong> 
            to receive personalized, AI-powered financial guidance.
        </p>
        <br>
        <div style='display:flex; justify-content:center; gap:40px; flex-wrap:wrap; margin-top:20px;'>
            <div style='background:rgba(102,126,234,0.1); border:1px solid rgba(102,126,234,0.3);
                        border-radius:12px; padding:20px; width:180px;'>
                <div style='font-size:2rem;'>📊</div>
                <strong>Financial Analysis</strong>
                <p style='color:#aaa; font-size:0.85rem; margin:4px 0 0;'>Budget, ratios & health score</p>
            </div>
            <div style='background:rgba(240,147,251,0.1); border:1px solid rgba(240,147,251,0.3);
                        border-radius:12px; padding:20px; width:180px;'>
                <div style='font-size:2rem;'>🤖</div>
                <strong>AI Advice</strong>
                <p style='color:#aaa; font-size:0.85rem; margin:4px 0 0;'>Powered by Gemini 1.5 Flash</p>
            </div>
            <div style='background:rgba(81,207,102,0.1); border:1px solid rgba(81,207,102,0.3);
                        border-radius:12px; padding:20px; width:180px;'>
                <div style='font-size:2rem;'>🎯</div>
                <strong>Goal Planning</strong>
                <p style='color:#aaa; font-size:0.85rem; margin:4px 0 0;'>Smart investment roadmaps</p>
            </div>
            <div style='background:rgba(255,169,77,0.1); border:1px solid rgba(255,169,77,0.3);
                        border-radius:12px; padding:20px; width:180px;'>
                <div style='font-size:2rem;'>💬</div>
                <strong>Chat Advisor</strong>
                <p style='color:#aaa; font-size:0.85rem; margin:4px 0 0;'>Ask anything, anytime</p>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown(
    """
<hr style='border-color:rgba(255,255,255,0.08); margin-top:40px;'>
<p style='text-align:center; color:#555; font-size:0.8rem; padding:10px 0;'>
    AI Financial Advisor • Powered by Google Gemini 1.5 Flash • For educational purposes only
</p>
""",
    unsafe_allow_html=True,
)
