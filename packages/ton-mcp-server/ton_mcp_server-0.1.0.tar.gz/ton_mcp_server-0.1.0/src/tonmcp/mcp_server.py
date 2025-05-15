import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
import os
import sys
from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP

from tonmcp.ton_client import TonClient
from tonmcp.prompts import PromptManager
from tonmcp.tools import ToolManager
from tonmcp.utils import parse_natural_language_query

load_dotenv()

logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
tmcp = FastMCP("TON MCP Server")

class TonMcpServer:
    def __init__(self, api_key: str, base_url: str = " https://tonapi.io"):
        logger.debug("Initializing TonMcpServer with API key and base_url=%s", base_url)
        self.api_key = api_key
        self.ton_client = TonClient(api_key, base_url)
        self.prompt_manager = PromptManager()
        self.tool_manager = ToolManager(self.ton_client)
        self._register_tools()
        self._register_prompts()

    def _register_tools(self):
        logger.debug("Registering tools...")
        @tmcp.tool(
            description="Analyze a TON address for its balance, jetton holdings, NFTs, and recent activity. Optionally performs deep forensic analysis if deep_analysis is True. Use for questions about account overview, holdings, or activity."
        )
        async def analyze_address(address: str, deep_analysis: bool = False) -> any:
            logger.debug(f"analyze_address called with address={address}, deep_analysis={deep_analysis}")
            result = await self.tool_manager.analyze_address(address=address, deep_analysis=deep_analysis)
            logger.debug(f"analyze_address result: {result}")
            return result

        @tmcp.tool(
            description="Get details and analysis for a specific TON blockchain transaction by its hash. Use for questions about a particular transaction, its participants, value, or type."
        )
        async def get_transaction_details(tx_hash: str) -> Any:
            """Get details for a transaction hash."""
            return await self.tool_manager.get_transaction_details(tx_hash=tx_hash)

        @tmcp.tool(
            description="Find trending tokens, pools, or accounts on the TON blockchain for a given timeframe and category. Use for questions about what's hot, trending, or popular on TON."
        )
        async def find_hot_trends(timeframe: str = "1h", category: str = "tokens") -> Any:
            """Find hot trends on TON."""
            return await self.tool_manager.find_hot_trends(timeframe=timeframe, category=category)

        @tmcp.tool(
            description="Analyze trading patterns for a TON address over a specified timeframe. Use for questions about trading activity, frequency, jetton transfers, or DEX swaps for an account."
        )
        async def analyze_trading_patterns(address: str, timeframe: str = "24h") -> Any:
            """Analyze trading patterns for an address."""
            return await self.tool_manager.analyze_trading_patterns(address=address, timeframe=timeframe)

    def _register_prompts(self):
        logger.debug("Registering prompts...")
        @tmcp.prompt()
        async def trading_analysis(**kwargs) -> str:
            return await self.prompt_manager.get_trading_analysis_prompt(**kwargs)

        @tmcp.prompt()
        async def forensics_investigation(**kwargs) -> str:
            return await self.prompt_manager.get_forensics_prompt(**kwargs)

        @tmcp.prompt()
        async def trend_analysis(**kwargs) -> str:
            return await self.prompt_manager.get_trend_analysis_prompt(**kwargs)

def main():
    api_key = os.getenv("TON_API_KEY")
    logger.debug(f"Starting main with TON_API_KEY={api_key}")
    if not api_key:
        raise ValueError("TON_API_KEY environment variable is required")
    TonMcpServer(api_key)
    logger.debug("Running FastMCP server on STDIO...")
    tmcp.run(transport="stdio")

if __name__ == "__main__":
    main()