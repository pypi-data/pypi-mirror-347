from ..api.client import ApiClient

def get_ticker_activity_news(
    client: ApiClient,
    ticker: str,
    page: int = 0,
    size: int = 15
) -> dict:
    """
    Get activity news for a ticker from tcanalysis API.
    """
    path = f"tcanalysis/v1/ticker/{ticker}/activity-news"
    params = {
        "page": page,
        "size": size
    }
    response = client.get(path, params=params)
    return response

def get_company_overview(
    client: ApiClient,
    company: str
) -> dict:
    """
    Get company overview from tcanalysis API.
    """
    path = f"tcanalysis/v1/company/{company}/overview"
    response = client.get(path)
    return response

def get_ticker_rating_general(
    client: ApiClient,
    ticker: str,
    fType: str = "TICKER"
) -> dict:
    """
    Get general rating for a ticker from tcanalysis API.
    """
    path = f"tcanalysis/v1/rating/{ticker}/general"
    params = {"fType": fType}
    response = client.get(path, params=params)
    return response

def get_rating_business_operation(
    client: ApiClient,
    ticker: str,
    fType: str = None
) -> dict:
    """
    Get business operation rating for a ticker from tcanalysis API.
    """
    path = f"tcanalysis/v1/rating/{ticker}/business-operation"
    params = {}
    if fType is not None:
        params["fType"] = fType
    response = client.get(path, params=params if params else None)
    return response

def get_rating_financial_health(
    client: ApiClient,
    ticker: str,
    fType: str = "TICKER"
) -> dict:
    """
    Get financial health rating for a ticker from tcanalysis API.
    """
    path = f"tcanalysis/v1/rating/{ticker}/financial-health"
    params = {"fType": fType}
    response = client.get(path, params=params)
    return response

def get_ticker_price_volatility(
    client: ApiClient,
    ticker: str
) -> dict:
    """
    Get price volatility for a ticker from tcanalysis API.
    """
    path = f"tcanalysis/v1/ticker/{ticker}/price-volatility"
    response = client.get(path)
    return response

def get_psycho_toptrading(client: ApiClient) -> dict:
    """
    Get top trading psychology data from tcanalysis API.
    """
    path = "tcanalysis/v1/psycho/toptrading"
    response = client.get(path)
    return response

def get_psycho_timeline(
    client: ApiClient,
    ticker: str = None,
    scale: int = None,
    timeframe: int = None
) -> dict:
    """
    Get psychology timeline from tcanalysis API.
    """
    path = "tcanalysis/v1/psycho/timeline"
    params = {}
    if ticker is not None:
        params["ticker"] = ticker
    if scale is not None:
        params["scale"] = scale
    if timeframe is not None:
        params["timeframe"] = timeframe
    response = client.get(path, params=params if params else None)
    return response

def get_ticker_stock_same_ind(client: ApiClient, ticker: str) -> dict:
    """
    Get stocks in the same industry as the given ticker from tcanalysis API.
    """
    path = f"tcanalysis/v1/ticker/{ticker}/stock-same-ind"
    response = client.get(path)
    return response

def get_company_dividend_payment_histories(client: ApiClient, company: str) -> dict:
    """
    Get dividend payment histories for a company from tcanalysis API.
    """
    path = f"tcanalysis/v1/company/{company}/dividend-payment-histories"
    response = client.get(path)
    return response

def get_company_audit_firms(client: ApiClient, company: str) -> dict:
    """
    Get audit firms for a company from tcanalysis API.
    """
    path = f"tcanalysis/v1/company/{company}/audit-firms"
    response = client.get(path)
    return response

def get_ticker_overview(client: ApiClient, ticker: str) -> dict:
    """
    Get overview for a ticker from tcanalysis API.
    """
    path = f"tcanalysis/v1/ticker/{ticker}/overview"
    response = client.get(path)
    return response

def get_news_activities_iwc(client: ApiClient) -> dict:
    """
    Get IWC news activities from tcanalysis API.
    """
    path = "tcanalysis/v1/news/activities/iwc"
    response = client.get(path)
    return response

def get_evaluation(
    client: ApiClient,
    ticker: str
) -> dict:
    """
    Get evaluation for a ticker from tcanalysis API.
    """
    path = f"tcanalysis/v1/evaluation/{ticker}/evaluation"
    response = client.get(path)
    return response

def get_evaluation_historical_chart(
    client: ApiClient,
    ticker: str,
    period: int = None,
    tWindow: str = None
) -> dict:
    """
    Get historical chart evaluation for a ticker from tcanalysis API.
    """
    path = f"tcanalysis/v1/evaluation/{ticker}/historical-chart"
    params = {}
    if period is not None:
        params["period"] = period
    if tWindow is not None:
        params["tWindow"] = tWindow
    response = client.get(path, params=params if params else None)
    return response

def get_data_charts_indicator(
    client: ApiClient,
    ticker: str
) -> dict:
    """
    Get indicator data charts from tcanalysis API.
    """
    path = "tcanalysis/v1/data-charts/indicator"
    params = {
        "ticker": ticker
    }
    response = client.get(path, params=params)
    return response

def get_data_charts_vol_foreign(
    client: ApiClient,
    ticker: str
) -> dict:
    """
    Get foreign volume data chart for a ticker from tcanalysis API.
    """
    path = "tcanalysis/v1/data-charts/vol-foreign"
    params = {"ticker": ticker}
    response = client.get(path, params=params)
    return response

def get_ticker_events_news(
    client: ApiClient,
    ticker: str,
    page: int = 0,
    size: int = 15
) -> dict:
    """
    Get events news for a ticker from tcanalysis API.
    """
    path = f"tcanalysis/v1/ticker/{ticker}/events-news"
    params = {"page": page, "size": size}
    response = client.get(path, params=params)
    return response

def get_finance_incomestatement(
    client: ApiClient,
    ticker: str,
    yearly: int = 0,
    isAll: bool = True
) -> dict:
    """
    Get income statement for a ticker from tcanalysis API.
    """
    path = f"tcanalysis/v1/finance/{ticker}/incomestatement"
    params = {"yearly": yearly, "isAll": str(isAll).lower()}
    response = client.get(path, params=params)
    return response

def get_finance_balancesheet(
    client: ApiClient,
    ticker: str,
    yearly: int = 0,
    isAll: bool = True
) -> dict:
    """
    Get balance sheet for a ticker from tcanalysis API.
    """
    path = f"tcanalysis/v1/finance/{ticker}/balancesheet"
    params = {"yearly": yearly, "isAll": str(isAll).lower()}
    response = client.get(path, params=params)
    return response

def get_news_events(
    client: ApiClient,
    fData: str = None,
    fType: str = None,
    page: int = 0,
    size: int = 20
) -> dict:
    """
    Get news events from tcanalysis API.
    """
    path = "tcanalysis/v1/news/events"
    params = {}
    if fData is not None:
        params["fData"] = fData
    if fType is not None:
        params["fType"] = fType
    params["page"] = page
    params["size"] = size
    response = client.get(path, params=params)
    return response

def get_rating_detail_single(
    client: ApiClient,
    ticker: str,
    fType: str = "TICKER"
) -> dict:
    """
    Get single detail rating for a ticker from tcanalysis API.
    """
    path = "tcanalysis/v1/rating/detail/single"
    params = {"ticker": ticker, "fType": fType}
    response = client.get(path, params=params)
    return response

def get_news_industries(client: ApiClient) -> dict:
    """
    Get news industries from tcanalysis API.
    """
    path = "tcanalysis/v1/news/industries"
    response = client.get(path)
    return response

def get_ticker_stockratio(client: ApiClient, ticker: str) -> dict:
    """
    Get stock ratio for a ticker from tcanalysis API.
    """
    path = f"tcanalysis/v1/ticker/{ticker}/stockratio"
    response = client.get(path)
    return response

def get_rating_business_model(
    client: ApiClient,
    ticker: str,
    fType: str = None
) -> dict:
    """
    Get business model rating for a ticker from tcanalysis API.
    """
    path = f"tcanalysis/v1/rating/{ticker}/business-model"
    params = {}
    if fType is not None:
        params["fType"] = fType
    response = client.get(path, params=params if params else None)
    return response

def get_rating_valuation(
    client: ApiClient,
    ticker: str,
    fType: str = "TICKER"
) -> dict:
    """
    Get valuation rating for a ticker from tcanalysis API.
    """
    path = f"tcanalysis/v1/rating/{ticker}/valuation"
    params = {"fType": fType}
    response = client.get(path, params=params)
    return response

def get_company_sub_companies(
    client: ApiClient,
    company: str,
    page: int = 0,
    size: int = 20
) -> dict:
    """
    Get sub-companies for a company from tcanalysis API.
    """
    path = f"tcanalysis/v1/company/{company}/sub-companies"
    params = {"page": page, "size": size}
    response = client.get(path, params=params)
    return response

def get_company_insider_dealing(
    client: ApiClient,
    company: str,
    page: int = 0,
    size: int = 20
) -> dict:
    """
    Get insider dealing for a company from tcanalysis API.
    """
    path = f"tcanalysis/v1/company/{company}/insider-dealing"
    params = {"page": page, "size": size}
    response = client.get(path, params=params)
    return response

def get_recommend_his(
    client: ApiClient,
    fData: str,
    fType: str = None,
    page: int = 0,
    size: int = 20,
    fRecommend: int = None,
    fTime: str = None
) -> dict:
    """
    Get historical recommendations from tcanalysis API.
    """
    path = "tcanalysis/v1/recommend/his"
    params = {"fData": fData, "page": page, "size": size}
    if fType is not None:
        params["fType"] = fType
    if fRecommend is not None:
        params["fRecommend"] = fRecommend
    if fTime is not None:
        params["fTime"] = fTime
    response = client.get(path, params=params)
    return response
