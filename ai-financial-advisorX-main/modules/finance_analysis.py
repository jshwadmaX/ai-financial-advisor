"""
Activity 2.1: Financial Data Analysis
Handles all financial calculations and analysis logic.
"""


def calculate_financial_summary(income, expenses, savings, debts, emi=0):
    """Calculate key financial metrics from user inputs."""

    disposable_income = income - expenses - emi
    net_savings_potential = disposable_income - (
        debts * 0.1
    )  # 10% debt repayment suggestion

    # Ratios
    savings_rate = (savings / income * 100) if income > 0 else 0
    debt_to_income = (debts / (income * 12) * 100) if income > 0 else 0
    expense_ratio = (expenses / income * 100) if income > 0 else 0
    emi_ratio = (emi / income * 100) if income > 0 else 0

    # Budget classification (50/30/20 rule)
    needs_budget = income * 0.50
    wants_budget = income * 0.30
    savings_budget = income * 0.20

    # Financial health score (0-100)
    health_score = 100
    if savings_rate < 10:
        health_score -= 20
    elif savings_rate < 20:
        health_score -= 10

    if debt_to_income > 40:
        health_score -= 25
    elif debt_to_income > 20:
        health_score -= 10

    if expense_ratio > 80:
        health_score -= 20
    elif expense_ratio > 60:
        health_score -= 10

    if emi_ratio > 40:
        health_score -= 15
    elif emi_ratio > 20:
        health_score -= 5

    health_score = max(0, min(100, health_score))

    return {
        "income": income,
        "expenses": expenses,
        "savings": savings,
        "debts": debts,
        "emi": emi,
        "disposable_income": disposable_income,
        "net_savings_potential": net_savings_potential,
        "savings_rate": round(savings_rate, 2),
        "debt_to_income": round(debt_to_income, 2),
        "expense_ratio": round(expense_ratio, 2),
        "emi_ratio": round(emi_ratio, 2),
        "needs_budget": needs_budget,
        "wants_budget": wants_budget,
        "savings_budget": savings_budget,
        "health_score": health_score,
    }


def calculate_goal_plan(
    target_amount, current_savings, months_remaining, expected_return=8.0
):
    """Calculate monthly savings needed to reach a financial goal."""

    if months_remaining <= 0:
        return None

    # Monthly return rate
    monthly_rate = expected_return / 100 / 12

    # Future value of current savings
    fv_current = current_savings * ((1 + monthly_rate) ** months_remaining)

    # Additional amount needed
    amount_needed = target_amount - fv_current

    if amount_needed <= 0:
        monthly_required = 0
    elif monthly_rate == 0:
        monthly_required = amount_needed / months_remaining
    else:
        # PMT formula
        monthly_required = (
            amount_needed
            * monthly_rate
            / (((1 + monthly_rate) ** months_remaining) - 1)
        )

    total_contributions = monthly_required * months_remaining
    total_interest = max(0, target_amount - current_savings - total_contributions)

    return {
        "target_amount": target_amount,
        "current_savings": current_savings,
        "months_remaining": months_remaining,
        "monthly_required": round(monthly_required, 2),
        "total_contributions": round(total_contributions, 2),
        "total_interest": round(total_interest, 2),
        "expected_return": expected_return,
        "fv_current": round(fv_current, 2),
    }


def get_investment_allocation(risk_profile, monthly_investable):
    """Return investment allocation based on risk profile."""

    allocations = {
        "Conservative": {
            "FD / RD": 40,
            "PPF / NSC": 30,
            "Debt Mutual Funds": 20,
            "Equity MF (Large Cap)": 10,
        },
        "Moderate": {
            "Equity MF (SIP)": 35,
            "Debt Mutual Funds": 25,
            "PPF / NPS": 20,
            "FD / RD": 15,
            "Gold / REITs": 5,
        },
        "Aggressive": {
            "Equity MF (Mid/Small Cap)": 45,
            "Direct Stocks": 25,
            "International Funds": 15,
            "Crypto / High Risk": 10,
            "Gold": 5,
        },
    }

    profile = allocations.get(risk_profile, allocations["Moderate"])
    result = {}
    for instrument, pct in profile.items():
        result[instrument] = {
            "percentage": pct,
            "monthly_amount": round(monthly_investable * pct / 100, 2),
        }
    return result


def classify_health_score(score):
    """Return label and color for health score."""
    if score >= 80:
        return "Excellent 🟢", "#00C853"
    elif score >= 60:
        return "Good 🟡", "#FFD600"
    elif score >= 40:
        return "Fair 🟠", "#FF6D00"
    else:
        return "Needs Attention 🔴", "#D50000"
