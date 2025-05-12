from typing import Optional
from ..api.client import ApiClient


def get_event_info_trading_view(
    client: ApiClient,
    ticker: str,
    from_: Optional[int] = None,
    to: Optional[int] = None,
    resolution: str = "D"
) -> dict:
    """
    Get trading view event info from icalendar-service API.

    Args:
        client (ApiClient): The API client instance.
        ticker (str): The ticker symbol.
        from_ (Optional[int]): The start timestamp (optional).
        to (Optional[int]): The end timestamp (optional).
        resolution (str): The resolution of the data (default is "D").

    Returns:
        dict: The response from the API.
    """
    path = "icalendar-service/v1/event-info/trading-view"
    params = {"ticker": ticker, "resolution": resolution}
    if from_ is not None:
        params["from"] = from_
    if to is not None:
        params["to"] = to
    response = client.get(path, params=params)
    return response