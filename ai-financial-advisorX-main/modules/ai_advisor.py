"""
Activity 2.2: AI Financial Guidance
Handles all Gemini AI interactions and prompt engineering.
"""

import os
import sys
import google.generativeai as genai

# Load configuration logic from config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def validate_gemini_connection():
    """Activity 1.3: Validate Gemini LLM Connectivity."""
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content("Hello Gemini! Test connection successful.")
        return True, f"✅ Gemini AI connected successfully. Response: {response.text}"
    except Exception as e:
        return False, f"❌ Connection failed: {str(e)}"


def get_financial_advice(financial_summary, user_profile="General"):
    """Generate personalized financial advice from Gemini."""

    prompt = f"""
You are an expert AI Financial Advisor. Analyze the following financial profile and provide clear, actionable advice in Indian Rupees (₹).

USER PROFILE: {user_profile}

FINANCIAL DATA:
- Monthly Income: ₹{financial_summary['income']:,.0f}
- Monthly Expenses: ₹{financial_summary['expenses']:,.0f}
- Current Savings: ₹{financial_summary['savings']:,.0f}
- Total Debts: ₹{financial_summary['debts']:,.0f}
- Monthly EMI: ₹{financial_summary['emi']:,.0f}
- Disposable Income: ₹{financial_summary['disposable_income']:,.0f}
- Savings Rate: {financial_summary['savings_rate']}%
- Expense Ratio: {financial_summary['expense_ratio']}%
- Debt-to-Income Ratio: {financial_summary['debt_to_income']}%
- Financial Health Score: {financial_summary['health_score']}/100

Please provide:
1. **Financial Health Assessment** - Brief evaluation of their current situation
2. **Top 3 Immediate Actions** - Specific steps to improve finances right now
3. **Savings Strategy** - How to increase savings rate
4. **Debt Management Plan** - If applicable, how to reduce debt efficiently
5. **Investment Recommendations** - Where to invest based on their profile
6. **Monthly Budget Suggestion** - A simple budget breakdown

Keep advice practical, specific, and motivating. Use ₹ for all amounts.
"""

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Could not generate advice: {str(e)}\n\nPlease check your API key and internet connection."


def chat_with_advisor(user_message, financial_summary, chat_history):
    """Handle multi-turn chat with financial context."""

    system_context = f"""You are a friendly, expert AI Financial Advisor specializing in personal finance for Indian users. 
You have access to the user's financial profile:
- Monthly Income: ₹{financial_summary.get('income', 0):,.0f}
- Monthly Expenses: ₹{financial_summary.get('expenses', 0):,.0f}
- Current Savings: ₹{financial_summary.get('savings', 0):,.0f}
- Total Debts: ₹{financial_summary.get('debts', 0):,.0f}
- Health Score: {financial_summary.get('health_score', 0)}/100

Answer questions clearly and concisely. Use ₹ for amounts. Be encouraging and practical."""

    # Build conversation history
    messages = [
        {
            "role": "user",
            "parts": [
                system_context
                + "\n\nAcknowledge you understand the user's profile in one sentence."
            ],
        }
    ]
    messages.append(
        {
            "role": "model",
            "parts": [
                "Understood! I have your complete financial profile and I'm ready to provide personalized advice."
            ],
        }
    )

    for msg in chat_history[-6:]:  # Keep last 6 exchanges for context
        role = "model" if msg["role"] == "assistant" else msg["role"]
        messages.append({"role": role, "parts": [msg["content"]]})

    messages.append({"role": "user", "parts": [user_message]})

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        chat = model.start_chat(history=messages[:-1])
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


def get_goal_advice(goal_name, goal_data, financial_summary):
    """Generate goal-specific investment strategy."""

    prompt = f"""
You are an AI Financial Advisor. Create a detailed goal-based financial plan.

GOAL: {goal_name}
- Target Amount: ₹{goal_data['target_amount']:,.0f}
- Current Savings: ₹{goal_data['current_savings']:,.0f}
- Time Horizon: {goal_data['months_remaining']} months ({goal_data['months_remaining']//12} years {goal_data['months_remaining']%12} months)
- Monthly Investment Required: ₹{goal_data['monthly_required']:,.0f}
- Expected Annual Return: {goal_data['expected_return']}%

USER'S MONTHLY INCOME: ₹{financial_summary.get('income', 0):,.0f}
DISPOSABLE INCOME: ₹{financial_summary.get('disposable_income', 0):,.0f}

Provide:
1. **Goal Feasibility Analysis** - Is this goal achievable?
2. **Recommended Investment Instruments** - Best options for this timeline
3. **Month-by-Month Strategy** - Key milestones
4. **Risk Management** - How to protect the investment
5. **Contingency Plan** - What if income drops or expenses rise?

Be specific with ₹ amounts and percentages.
"""

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Could not generate goal advice: {str(e)}"
