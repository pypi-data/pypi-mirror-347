import logging
import os

from .services.bond_trading import get_iconnect_bond_products
from .services.tcanalysis import (
    get_ticker_activity_news,
    get_company_overview,
    get_ticker_rating_general,
    get_rating_business_operation,
    get_rating_financial_health,
    get_ticker_price_volatility,
    get_psycho_toptrading,
    get_psycho_timeline,
    get_ticker_stock_same_ind,
    get_company_dividend_payment_histories,
    get_company_audit_firms,
    get_ticker_overview,
    get_news_activities_iwc,
    get_evaluation,
    get_evaluation_historical_chart,
    get_data_charts_indicator,
    get_data_charts_vol_foreign,
    get_ticker_events_news,
    get_finance_incomestatement,
    get_finance_balancesheet,
    get_news_events,
    get_rating_detail_single,
    get_news_industries,
    get_ticker_stockratio,
    get_rating_business_model,
    get_rating_valuation,
    get_company_sub_companies,
    get_company_insider_dealing,
    get_recommend_his
)
from . import constant
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from .api.client import ApiClient

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging configured. Writing to app.log.")

def load_configuration(env_path=None):
    if env_path:
        load_dotenv(env_path, override=True)
    else:
        load_dotenv(override=True)

    config = {
        "API_KEY": os.getenv("TCBS_API_KEY"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO")
    }
    return config

def create_server(env_path=None):
    
    configure_logging()
    config = load_configuration(env_path)
    logger = logging.getLogger(__name__)
    logger.info("environment variables loaded from %s", env_path or ".env")
    logger.info("Starting server with configuration: %s", config)

    mcp = FastMCP("TCinvest MCP Server")
    client_aws = ApiClient(config['API_KEY'], constant.API_EXT_AWS)
    client = ApiClient(config['API_KEY'], constant.API_EXT)
    
    @mcp.tool()
    def get_iconnect_bond_products_tool(filter: str = "channel:cus,markettype:iconnect", level: str="basic", order_by: str = "code(asc)", excludePP: int = 0) -> dict:
        """
        Get bond products from iConnect.
        """
        logger.info("Fetching bond products with filter: %s", filter)
        return get_iconnect_bond_products(client, filter, level, order_by, excludePP)

    @mcp.tool()
    def get_ticker_activity_news_tool(ticker: str, page: int = 0, size: int = 15) -> dict:
        """
        Get activity news for a ticker from tcanalysis API.
        """
        return get_ticker_activity_news(client_aws, ticker, page, size)

    @mcp.tool()
    def get_company_overview_tool(company: str) -> dict:
        """
        Get company overview from tcanalysis API.
        """
        return get_company_overview(client_aws, company)

    @mcp.tool()
    def get_ticker_rating_general_tool(ticker: str, fType: str = "TICKER") -> dict:
        """
        Get general rating for a ticker from tcanalysis API.
        """
        return get_ticker_rating_general(client_aws, ticker, fType)

    @mcp.tool()
    def get_rating_business_operation_tool(ticker: str, fType: str = None) -> dict:
        """
        Get business operation rating for a ticker from tcanalysis API.
        """
        return get_rating_business_operation(client_aws, ticker, fType)

    @mcp.tool()
    def get_rating_financial_health_tool(ticker: str, fType: str = "TICKER") -> dict:
        """
        Get financial health rating for a ticker from tcanalysis API.
        """
        return get_rating_financial_health(client_aws, ticker, fType)

    @mcp.tool()
    def get_ticker_price_volatility_tool(ticker: str) -> dict:
        """
        Get price volatility for a ticker from tcanalysis API.
        """
        return get_ticker_price_volatility(client_aws, ticker)

    @mcp.tool()
    def get_psycho_toptrading_tool() -> dict:
        """
        Get top trading psychology data from tcanalysis API.
        """
        return get_psycho_toptrading(client_aws)

    @mcp.tool()
    def get_psycho_timeline_tool(ticker: str = None, scale: int = None, timeframe: int = None) -> dict:
        """
        Get psychology timeline from tcanalysis API.
        """
        return get_psycho_timeline(client_aws, ticker, scale, timeframe)

    @mcp.tool()
    def get_ticker_stock_same_ind_tool(ticker: str) -> dict:
        """
        Get stocks in the same industry as the given ticker from tcanalysis API.
        """
        return get_ticker_stock_same_ind(client_aws, ticker)

    @mcp.tool()
    def get_company_dividend_payment_histories_tool(company: str) -> dict:
        """
        Get dividend payment histories for a company from tcanalysis API.
        """
        return get_company_dividend_payment_histories(client_aws, company)

    @mcp.tool()
    def get_company_audit_firms_tool(company: str) -> dict:
        """
        Get audit firms for a company from tcanalysis API.
        """
        return get_company_audit_firms(client_aws, company)

    @mcp.tool()
    def get_ticker_overview_tool(ticker: str) -> dict:
        """
        Get overview for a ticker from tcanalysis API.
        """
        return get_ticker_overview(client_aws, ticker)

    @mcp.tool()
    def get_news_activities_iwc_tool() -> dict:
        """
        Get IWC news activities from tcanalysis API.
        """
        return get_news_activities_iwc(client_aws)

    @mcp.tool()
    def get_evaluation_tool(ticker: str) -> dict:
        """
        Get evaluation for a ticker from tcanalysis API.
        """
        return get_evaluation(client_aws, ticker)

    @mcp.tool()
    def get_evaluation_historical_chart_tool(ticker: str, period: int = None, tWindow: str = None) -> dict:
        """
        Get historical chart evaluation for a ticker from tcanalysis API.
        """
        return get_evaluation_historical_chart(client_aws, ticker, period, tWindow)

    @mcp.tool()
    def get_data_charts_indicator_tool(ticker: str) -> dict:
        """
        Get indicator data charts from tcanalysis API.
        """
        return get_data_charts_indicator(client_aws, ticker)

    @mcp.tool()
    def get_data_charts_vol_foreign_tool(ticker: str) -> dict:
        """
        Get foreign volume data chart for a ticker from tcanalysis API.
        """
        return get_data_charts_vol_foreign(client_aws, ticker)

    @mcp.tool()
    def get_ticker_events_news_tool(ticker: str, page: int = 0, size: int = 15) -> dict:
        """
        Get events news for a ticker from tcanalysis API.
        """
        return get_ticker_events_news(client_aws, ticker, page, size)

    @mcp.tool()
    def get_finance_incomestatement_tool(ticker: str, yearly: int = 0, isAll: bool = True) -> dict:
        """
        Get income statement for a ticker from tcanalysis API.
        """
        return get_finance_incomestatement(client_aws, ticker, yearly, isAll)

    @mcp.tool()
    def get_finance_balancesheet_tool(ticker: str, yearly: int = 0, isAll: bool = True) -> dict:
        """
        Get balance sheet for a ticker from tcanalysis API.
        """
        return get_finance_balancesheet(client_aws, ticker, yearly, isAll)

    @mcp.tool()
    def get_news_events_tool(fData: str = None, fType: str = None, page: int = 0, size: int = 20) -> dict:
        """
        Get news events from tcanalysis API.
        """
        return get_news_events(client_aws, fData, fType, page, size)

    @mcp.tool()
    def get_rating_detail_single_tool(ticker: str, fType: str = "TICKER") -> dict:
        """
        Get single detail rating for a ticker from tcanalysis API.
        """
        return get_rating_detail_single(client_aws, ticker, fType)

    @mcp.tool()
    def get_news_industries_tool() -> dict:
        """
        Get news industries from tcanalysis API.
        """
        return get_news_industries(client_aws)

    @mcp.tool()
    def get_ticker_stockratio_tool(ticker: str) -> dict:
        """
        Get stock ratio for a ticker from tcanalysis API.
        """
        return get_ticker_stockratio(client_aws, ticker)

    @mcp.tool()
    def get_rating_business_model_tool(ticker: str, fType: str = None) -> dict:
        """
        Get business model rating for a ticker from tcanalysis API.
        """
        return get_rating_business_model(client_aws, ticker, fType)

    @mcp.tool()
    def get_rating_valuation_tool(ticker: str, fType: str = "TICKER") -> dict:
        """
        Get valuation rating for a ticker from tcanalysis API.
        """
        return get_rating_valuation(client_aws, ticker, fType)

    @mcp.tool()
    def get_company_sub_companies_tool(company: str, page: int = 0, size: int = 20) -> dict:
        """
        Get sub-companies for a company from tcanalysis API.
        """
        return get_company_sub_companies(client_aws, company, page, size)

    @mcp.tool()
    def get_company_insider_dealing_tool(company: str, page: int = 0, size: int = 20) -> dict:
        """
        Get insider dealing for a company from tcanalysis API.
        """
        return get_company_insider_dealing(client_aws, company, page, size)

    @mcp.tool()
    def get_recommend_his_tool(fData: str, fType: str = None, page: int = 0, size: int = 20, fRecommend: int = None, fTime: str = None) -> dict:
        """
        Get historical recommendations from tcanalysis API.
        """
        return get_recommend_his(client_aws, fData, fType, page, size, fRecommend, fTime)

    return mcp

if __name__ == "__main__":
    server = create_server()
    server.run(transport="sse")