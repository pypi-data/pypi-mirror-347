from typing import Dict
from ..api.client import ApiClient

def get_ticker_pivot(
    client: ApiClient,
    ticker: str,
    period: str = "D"
) -> dict:
    """
    Get pivot data for a ticker from ta API.

    Args:
        client (ApiClient): The API client instance.
        ticker (str): The ticker symbol.
        period (str): The period for pivot data. Default is "D".

    Returns:
        dict: The pivot data for the ticker.
    """
    path = f"ta/v1/pivot/{ticker}"
    params = {"period": period}
    response = client.get(path, params=params)
    return response

def get_summary_gaugechart(
    client: ApiClient,
    ticker: str,
    period: str = None
) -> dict:
    """
    Get summary gauge chart for a ticker from ta API.
    """
    path = f"ta/v1/summary/gaugechart/{ticker}"
    params = {}
    if period is not None:
        params["period"] = period
    response = client.get(path, params=params if params else None)
    return response