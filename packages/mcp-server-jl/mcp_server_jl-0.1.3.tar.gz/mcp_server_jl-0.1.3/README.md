# Joblogic MCP Server

This project implements an MCP (Model Context Protocol) server using stdio transport for communication. It provides tools for test case generation and formatting, along with other utilities for Joblogic documentation and API specifications.

## Installation

You can install the package directly from PyPI:

```bash
pip install mcp-server-jl
```

Or install it from the source code:

```bash
pip install .
```

## Usage

### Command Line

After installation, you can run the MCP server directly from the command line:

```bash
mcp-server-jl
```

### As a Python Package

```python
from mcp_server_jl.server import mcp, run_server
import anyio

# Add your custom tools
@mcp.tool()
def my_custom_tool():
    # Your code here
    pass

# Run the server
if __name__ == "__main__":
    anyio.run(run_server)
```

## Available Tools

### Generate Test Cases

Generates test cases from a markdown specification:

```python
result = await mcp.generate_testcases_for_content_spec(markdown_content, spec_file_path)
```

### Format Test Cases

Format and clean test case files:

```python
result = await mcp.format_all_testcases(input_folder, output_folder)
```

### Convert to Markdown

Convert a resource to markdown:

```python
markdown = await mcp.convert_to_markdown(uri)
```

## Docker

You can also run the server using Docker:

```bash
docker build -t mcp-local/joblogic .
docker run -it mcp-local/joblogic
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.



