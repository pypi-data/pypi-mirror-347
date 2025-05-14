import anyio
from .server import run_server

def main():
    """Entry point for the MCP server CLI"""
    print("Starting Joblogic MCP Server...")
    anyio.run(run_server)

if __name__ == "__main__":
    main()
