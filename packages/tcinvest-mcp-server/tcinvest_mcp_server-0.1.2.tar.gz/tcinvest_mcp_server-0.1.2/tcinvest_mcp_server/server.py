import logging
import os

from .services.bond_trading import get_iconnect_bond_products
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

    return mcp

if __name__ == "__main__":
    server = create_server()
    server.run(transport="sse")