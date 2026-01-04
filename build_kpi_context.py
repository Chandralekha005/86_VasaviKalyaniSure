def build_kpi_context(metrics: dict) -> str:
    """
    Convert numerical KPIs into structured narrative context
    suitable for Retrieval-Augmented Generation.
    """

    revenue_yoy = metrics.get("revenue_yoy")
    revenue_qoq = metrics.get("revenue_qoq")
    profit_margin = metrics.get("profit_margin")

    context = f"""
    The company reported a year-over-year revenue change of {revenue_yoy:.2%}.
    Quarter-over-quarter revenue growth was {revenue_qoq:.2%}.
    The profit margin stood at {profit_margin:.2%}.

    A decline in year-over-year revenue indicates pressure on long-term performance.
    Positive quarter-over-quarter growth may suggest short-term recovery or seasonality.
    Negative profit margins reflect ongoing cost or efficiency challenges.
    """

    # Clean spacing
    return " ".join(context.split())
