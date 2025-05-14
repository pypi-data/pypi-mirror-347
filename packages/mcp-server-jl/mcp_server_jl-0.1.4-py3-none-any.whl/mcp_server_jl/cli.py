import anyio
import sys
import os

# Thêm thư mục gốc vào đường dẫn để có thể import mcp_server_jl như một package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from .server import run_server
except ImportError:
    # Fallback khi chạy trực tiếp
    from mcp_server_jl.server import run_server

def main():
    """Entry point for the MCP server CLI"""
    print("Starting Joblogic MCP Server with version 1.0.0...")
    anyio.run(run_server)

if __name__ == "__main__":
    main()
