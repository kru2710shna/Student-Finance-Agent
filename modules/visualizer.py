import plotly.express as px
import pandas as pd

def cash_flow_chart(df: pd.DataFrame):
    """Bar chart of cash in/out per category."""
    if df.empty:
        return None
    return px.bar(df, x="category", y="amount", title="Cash Flow by Category")

def category_chart(df: pd.DataFrame):
    """Pie chart of top spending categories."""
    if df.empty:
        return None
    return px.pie(df, names="category", values="amount", title="Top Spending Categories")
