import argparse
import os
from .server import create_server

def main():
    parser = argparse.ArgumentParser(description="Start TCInvest MCP Server")
    parser.add_argument('--env', type=str, default=".env", help="Path to .env file")
    args = parser.parse_args()
    os.environ["DOTENV_PATH"] = args.env
    print(f"Loading environment variables from {args.env}")
    server = create_server(env_path=args.env)
    server.run(transport="sse")

if __name__ == "__main__":
    main()
