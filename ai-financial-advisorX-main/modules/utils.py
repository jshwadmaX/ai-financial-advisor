"""
Activity 2.4: Helper Functions
Utility functions for formatting, validation, and display.
"""

import streamlit as st


def format_currency(amount):
    """Format number as Indian Rupee currency."""
    if amount >= 10_00_000:
        return f"₹{amount/10_00_000:.2f}L"
    elif amount >= 1_000:
        return f"₹{amount:,.0f}"
    else:
        return f"₹{amount:.2f}"


def format_percentage(value):
    """Format number as percentage string."""
    return f"{value:.1f}%"


def get_health_color(score):
    """Return color hex for health score."""
    if score >= 80:
        return "#00C853"
    elif score >= 60:
        return "#FFD600"
    elif score >= 40:
        return "#FF6D00"
    else:
        return "#D50000"


def validate_inputs(income, expenses, savings, debts):
    """Validate financial inputs."""
    errors = []
    if income <= 0:
        errors.append("Income must be greater than 0.")
    if expenses < 0:
        errors.append("Expenses cannot be negative.")
    if savings < 0:
        errors.append("Savings cannot be negative.")
    if debts < 0:
        errors.append("Debts cannot be negative.")
    if expenses > income:
        errors.append("⚠️ Expenses exceed income — review your budget.")
    return errors


def display_metric_card(col, label, value, delta=None, delta_color="normal"):
    """Display a styled metric in a column."""
    with col:
        st.metric(label=label, value=value, delta=delta, delta_color=delta_color)


def get_financial_tips(financial_summary):
    """Return quick financial tips based on analysis."""
    tips = []

    if financial_summary["savings_rate"] < 20:
        tips.append("💡 Try to save at least 20% of your income each month.")
    if financial_summary["expense_ratio"] > 70:
        tips.append(
            "✂️ Your expenses are high. Review subscriptions and discretionary spending."
        )
    if financial_summary["debt_to_income"] > 30:
        tips.append(
            "🏦 Consider the Avalanche method to pay high-interest debts first."
        )
    if financial_summary["disposable_income"] < 5000:
        tips.append(
            "⚠️ Very low disposable income. Building an emergency fund should be priority."
        )
    if financial_summary["health_score"] >= 80:
        tips.append(
            "🌟 Great financial health! Consider increasing equity exposure for wealth creation."
        )

    if not tips:
        tips.append(
            "✅ Your finances look balanced. Stay consistent and review quarterly."
        )

    return tips


def get_profile_defaults(profile):
    """Return default financial values based on user profile."""
    defaults = {
        "Student": {
            "income": 15000,
            "expenses": 10000,
            "savings": 2000,
            "debts": 50000,
            "emi": 0,
        },
        "Working Professional": {
            "income": 60000,
            "expenses": 35000,
            "savings": 10000,
            "debts": 200000,
            "emi": 8000,
        },
        "Business Owner": {
            "income": 150000,
            "expenses": 70000,
            "savings": 30000,
            "debts": 500000,
            "emi": 20000,
        },
        "Retiree": {
            "income": 40000,
            "expenses": 25000,
            "savings": 500000,
            "debts": 0,
            "emi": 0,
        },
    }
    return defaults.get(profile, defaults["Working Professional"])
