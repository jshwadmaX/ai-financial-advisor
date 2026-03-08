"""
Activity 2.3: Data Visualization
All Plotly chart generation functions.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def create_expense_donut(financial_summary):
    """Donut chart showing income breakdown."""

    labels = ["Expenses", "EMI", "Savings Potential", "Free Cash"]
    values = [
        financial_summary["expenses"],
        financial_summary["emi"],
        max(0, financial_summary["savings"]),
        max(0, financial_summary["disposable_income"] - financial_summary["savings"]),
    ]
    colors = ["#FF6B6B", "#FFA94D", "#51CF66", "#74C0FC"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.55,
                marker=dict(colors=colors, line=dict(color="#1a1a2e", width=2)),
                textinfo="label+percent",
                textfont=dict(size=12),
            )
        ]
    )

    fig.update_layout(
        title=dict(text="Income Distribution", font=dict(size=16, color="white")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        showlegend=True,
        legend=dict(font=dict(color="white")),
        height=350,
        margin=dict(t=50, b=20, l=20, r=20),
    )
    return fig


def create_budget_bar(financial_summary):
    """Bar chart comparing actual vs recommended budget."""

    categories = ["Needs (50%)", "Wants (30%)", "Savings (20%)"]
    recommended = [
        financial_summary["needs_budget"],
        financial_summary["wants_budget"],
        financial_summary["savings_budget"],
    ]
    actual = [
        financial_summary["expenses"],
        financial_summary["emi"],
        financial_summary["savings"],
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="Recommended",
            x=categories,
            y=recommended,
            marker_color="#74C0FC",
            opacity=0.8,
        )
    )
    fig.add_trace(
        go.Bar(
            name="Actual", x=categories, y=actual, marker_color="#FF6B6B", opacity=0.8
        )
    )

    fig.update_layout(
        title=dict(
            text="Budget: Actual vs 50/30/20 Rule", font=dict(size=16, color="white")
        ),
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(gridcolor="#333", color="white"),
        yaxis=dict(gridcolor="#333", color="white", title="Amount (₹)"),
        legend=dict(font=dict(color="white")),
        height=350,
        margin=dict(t=50, b=30, l=60, r=20),
    )
    return fig


def create_health_gauge(health_score):
    """Gauge chart for financial health score."""

    label, color = (
        ("Excellent", "#00C853")
        if health_score >= 80
        else (
            ("Good", "#FFD600")
            if health_score >= 60
            else (
                ("Fair", "#FF6D00")
                if health_score >= 40
                else ("Needs Attention", "#D50000")
            )
        )
    )

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=health_score,
            title={
                "text": f"Financial Health Score<br><span style='font-size:14px;color:{color}'>{label}</span>",
                "font": {"color": "white", "size": 16},
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickcolor": "white",
                    "tickfont": {"color": "white"},
                },
                "bar": {"color": color},
                "bgcolor": "#1e1e2e",
                "steps": [
                    {"range": [0, 40], "color": "#3a1a1a"},
                    {"range": [40, 60], "color": "#3a2a1a"},
                    {"range": [60, 80], "color": "#2a3a1a"},
                    {"range": [80, 100], "color": "#1a3a1a"},
                ],
                "threshold": {
                    "line": {"color": "white", "width": 3},
                    "value": health_score,
                },
            },
            number={"font": {"color": "white", "size": 40}, "suffix": "/100"},
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        height=280,
        margin=dict(t=60, b=20, l=30, r=30),
    )
    return fig


def create_goal_progress(goal_data):
    """Progress chart for goal planning."""

    months = goal_data["months_remaining"]
    monthly = goal_data["monthly_required"]
    current = goal_data["current_savings"]
    rate = goal_data["expected_return"] / 100 / 12

    month_list = list(range(0, months + 1))
    balances = []

    for m in month_list:
        if rate > 0:
            fv = current * ((1 + rate) ** m) + monthly * (((1 + rate) ** m - 1) / rate)
        else:
            fv = current + monthly * m
        balances.append(round(fv, 2))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=month_list,
            y=balances,
            mode="lines",
            fill="tozeroy",
            line=dict(color="#51CF66", width=2),
            fillcolor="rgba(81,207,102,0.15)",
            name="Projected Balance",
        )
    )
    fig.add_hline(
        y=goal_data["target_amount"],
        line_dash="dash",
        line_color="#FFA94D",
        annotation_text=f"Target ₹{goal_data['target_amount']:,.0f}",
        annotation_font_color="#FFA94D",
    )

    fig.update_layout(
        title=dict(text="Goal Progress Projection", font=dict(size=16, color="white")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(title="Months", gridcolor="#333", color="white"),
        yaxis=dict(title="Amount (₹)", gridcolor="#333", color="white"),
        height=350,
        margin=dict(t=50, b=50, l=60, r=20),
    )
    return fig


def create_investment_pie(allocation_data):
    """Pie chart for investment allocation."""

    labels = list(allocation_data.keys())
    values = [v["monthly_amount"] for v in allocation_data.values()]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.4,
                marker=dict(line=dict(color="#1a1a2e", width=2)),
                textinfo="label+percent",
                textfont=dict(size=11),
            )
        ]
    )

    fig.update_layout(
        title=dict(text="Investment Allocation", font=dict(size=16, color="white")),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        legend=dict(font=dict(color="white")),
        height=350,
        margin=dict(t=50, b=20, l=20, r=20),
    )
    return fig
