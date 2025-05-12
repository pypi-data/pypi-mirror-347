from ..api.client import ApiClient

def get_stock_bars_long_term(
    client: ApiClient,
    ticker: str,
    type_: str = "stock",
    resolution: str = "D",
    to: int = None,
    countBack: int = None
) -> dict:
    """
    Get long-term stock bars from stock-insight API.
    """
    params = {
        "ticker": ticker,
        "type": type_,
        "resolution": resolution
    }
    if to is not None:
        params["to"] = to
    if countBack is not None:
        params["countBack"] = countBack
    response = client.get("stock-insight/v2/stock/bars-long-term", params=params)
    return response

def search_stock_insight(
    client: ApiClient,
    query: str
) -> dict:
    """
    Search stock insight using the stock-insight API.
    """
    params = {"key": query}
    response = client.get("stock-insight/v1/search", params=params)
    return response
