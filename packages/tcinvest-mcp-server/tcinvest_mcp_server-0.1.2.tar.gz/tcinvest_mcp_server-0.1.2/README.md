# TCInvest MCP Server

This project is a Model Context Protocol (MCP) server for TCInvest, designed to help users build LLM-powered applications with real-time and historical stock and bond data from the TCBS API. The goal is to enable users to interact with financial data using large language models (LLMs), similar to how DeepSeek operates in the Chinese stock market—using LLMs to replace traditional brokers and provide intelligent, automated investment support.

## Purpose
- Enable seamless integration of LLMs (such as GPT, DeepSeek, etc.) with Vietnamese stock and bond data from TCBS.
- Allow users to query, analyze, and visualize financial data using natural language.
- Provide a foundation for building next-generation AI investment assistants and tools.
- Continuously expand features and API coverage to support more financial products and use cases.

## Features
- Retrieve stock and bond data from the TCBS API
- Loads configuration from a `.env` file
- Logs activity to `app.log`
- Exposes MCP tools to retrieve and visualize bond data
- Generates charts (PNG, base64) for investment time by bond code
- Designed for easy extension with new APIs and features

## Project Structure
```
api/
  client.py         # API client for TCBS endpoints
business/
  bonds.py          # Business logic for bond products
constant.py         # API endpoint constants
server.py           # MCP server entry point
requirements.txt    # Python dependencies
.env                # Environment variables (API key, base URL)
app.log             # Log file
```

## Getting Started
1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment**
   - Copy `.env` and set your `TCBS_API_KEY` and `BASE_URL`.
4. **Run the server**
   ```bash
   python -m tcinvest_mcp_server
   ```

## Usage
- The server exposes MCP tools for bond data retrieval and visualization.
- Logs are written to `app.log`.
- Visualizations are returned as base64-encoded PNG images for easy embedding in HTML.

## Roadmap
- Add more TCBS API endpoints for stocks, funds, and other financial products
- Integrate advanced LLM-based query and reasoning capabilities
- Support more visualization types and analytics
- Enable conversational investment assistants and chatbots
- Community contributions and feature requests welcome!

## Disclaimer
See `DISCLAIM.md` for important legal and usage information.

## License
This project is for educational and demonstration purposes only. See `DISCLAIM.md` for details.
