import sys
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from mcp.server import Server
from markitdown import MarkItDown
import uvicorn

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from html2text import html2text
import re
import os
import datetime
from typing import List, Dict, Optional, Any, Tuple
import json
import sys
import anyio

from mcp.server.fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS
from mcp.server.stdio import stdio_server

# Initialize FastMCP server for MarkItDown (SSE)
mcp = FastMCP("markitdown")

@mcp.tool()
def generate_testcases_for_spec(markdown_content: str, spec_file_path: str, output_dir: str = None) -> dict:
    """
    Generate test cases for a markdown specification content and save to file.
    
    Args:
        markdown_content (str): The markdown specification content.
        spec_file_path (str): The file path of the spec markdown file.
        output_dir (str, optional): The directory where test cases should be saved.
                                  If not provided, will use current directory.

    Returns:
        dict: Contains the generated test cases and file path info
    """
    import os
    import re
    import time

    API_URL = "https://flowise-app-dev.purplestone-9506740f.westeurope.azurecontainerapps.io/api/v1/prediction/a7e965f2-3621-40c1-b40e-2b96a4ae9b4b"
    PROMPT = """
Please generate full coverage test cases based on the following specification.
Include positive and negative scenarios, edge cases, validation rules, and permission handling:
"""
    MAX_RETRIES = 3
    TIMEOUT = 60  # seconds per request
    RETRY_DELAY = 2  # seconds between retries

    try:
        if not markdown_content.strip():
            return {"status": "error", "message": "Input content is empty."}        # Use provided output directory or default to current directory
        if output_dir:
            # Ensure the output directory exists
            os.makedirs(output_dir, exist_ok=True)
        else:
            # Default to current working directory
            output_dir = os.getcwd()
            
        # Get the spec filename without extension
        spec_name = os.path.splitext(os.path.basename(spec_file_path))[0]        # Generate a unique filename based on spec name and timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"{spec_name}.testcase.md")

        # Call the API with retries
        testcases = None
        last_error = None

        for attempt in range(MAX_RETRIES):
            try:
                # Make the request with a longer timeout
                response = requests.post(
                    API_URL, 
                    json={"question": PROMPT + markdown_content},
                    timeout=TIMEOUT
                )
                response.raise_for_status()
                
                # Get response data
                response_data = response.json()
                
                # Validate response data
                if not response_data:
                    raise ValueError("Empty response from Flowise")
                
                testcases = response_data.get("text")
                if not testcases or testcases == "[No test cases returned]":
                    raise ValueError("No test cases in Flowise response")
                
                # If we got here, we have valid test cases
                break
                
            except requests.Timeout:
                last_error = "Request timed out"
            except requests.RequestException as e:
                last_error = f"Request failed: {str(e)}"
            except (KeyError, ValueError) as e:
                last_error = str(e)
            
            # Wait before retrying
            if attempt < MAX_RETRIES - 1:  # Don't sleep after the last attempt
                time.sleep(RETRY_DELAY)

        # If we couldn't get test cases after all retries
        if testcases is None:
            return {
                "status": "error",
                "message": f"Failed to get test cases after {MAX_RETRIES} attempts. Last error: {last_error}"
            }

        # Save the test cases to file, ensuring file is properly closed even if writing fails
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(testcases)
        except IOError as e:
            return {
                "status": "error",
                "message": f"Failed to save test cases to file: {str(e)}"
            }

        return {
            "status": "success",
            "message": f"Test cases saved to {output_file}",
            "file_path": output_file,
            "content": testcases
        }

    except Exception as e:
        return {
            "status": "error", 
            "message": f"Error processing content: {str(e)}",
            "error_type": type(e).__name__
        }

@mcp.tool()
def format_all_testcases(markdown_content: str, testcase_file_path: str, output_dir: str = None) -> Dict[str, Any]:
    """
    Format test case content and save cleaned versions into specified output directory.
    Keep only TC number, Title, Preconditions, and numbered Steps.
    
    Args:
        markdown_content (str): The test case content to format.
        testcase_file_path (str): The file path of the test case markdown file.
        output_dir (str, optional): The directory where formatted test cases should be saved.
                                  If not provided, will use current directory.

    Returns:
        dict: Contains the formatted test cases and file path info
    """
    import re
    import os
    import datetime

    try:
        if not markdown_content.strip():
            return {"status": "error", "message": "Input content is empty."}        # Use provided output directory or default to current directory
        if output_dir:
            # Ensure the output directory exists
            os.makedirs(output_dir, exist_ok=True)
        else:
            # Default to current working directory
            output_dir = os.getcwd()
              # Extract the spec name from the testcase filename
        testcase_name = os.path.splitext(os.path.basename(testcase_file_path))[0]
        # If the testcase filename follows pattern 'specname_YYYYMMDD_HHMMSS.testcase', extract the specname
        spec_name_match = re.match(r'(.+?)_\d{8}_\d{6}\.testcase', os.path.basename(testcase_file_path))
        if spec_name_match:
            spec_name = spec_name_match.group(1)
        else:
            # If not matching the expected pattern, use the testcase name as fallback
            spec_name = testcase_name
            
        # Generate timestamp for the new filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"{spec_name}_{timestamp}_formatted.testcase.md")

        # Format the content
        formatted_content = ""
        
        # Extract test cases with a pattern that better matches the actual format
        tc_pattern = r'\*\*TC(\d+):\s*(.*?)\*\*\s*\n+\s*-\s*\*\*Title\*\*:\s*(.*?)(?=\n)'
        tc_matches = re.findall(tc_pattern, markdown_content, re.DOTALL)
        
        # Track processed test case numbers
        processed_tcs = set()
        
        # Process each test case
        for match in tc_matches:
            tc_num = match[0]
            tc_name = match[1].strip()
            tc_title = match[2].strip()
            
            # Skip if we've already processed this test case
            if tc_num in processed_tcs:
                continue
            
            # Format the test case
            formatted_tc = f"TC{tc_num}: {tc_name}\n\n"
            formatted_tc += f"Title: {tc_title}\n\n"
            
            # Extract preconditions
            precond_pattern = r'\*\*TC' + re.escape(tc_num) + r':.*?\n+\s*-\s*\*\*Preconditions\*\*:\s*(.*?)(?=\n\s*-\s*\*\*|\n\s*\|)'
            precond_match = re.search(precond_pattern, markdown_content, re.DOTALL)
            
            if precond_match:
                precond = precond_match.group(1).strip()
                
                # Check if there are multiple preconditions (indicated by bullet points)
                if re.search(r'-\s+', precond):
                    # Extract individual preconditions using bullet points as separators
                    precond_items = re.findall(r'-\s+(.*?)(?=\s*-\s+|\s*$)', precond + " ")
                    
                    if len(precond_items) > 1:
                        formatted_tc += "Preconditions:\n"
                        for item in precond_items:
                            item_text = item.strip()
                            if item_text:
                                formatted_tc += f"- {item_text}\n"
                    else:
                        # If we only find one despite the bullet point, format as single
                        formatted_tc += f"Preconditions: {precond_items[0].strip()}\n"
                else:
                    # Single precondition
                    formatted_tc += f"Preconditions: {precond}\n"
            else:
                formatted_tc += "Preconditions: None\n"
            
            formatted_tc += "\n"  # Add extra line after preconditions
            
            # Find the table for this test case
            table_pattern = r'\*\*TC' + re.escape(tc_num) + r':.*?\|\s*Steps\s*\|\s*Expected Result\s*\|.*?\n\|[\s-]+\|[\s-]+\|\n((?:\|.*?\|.*?\|\n)+)'
            table_match = re.search(table_pattern, markdown_content, re.DOTALL)
            
            steps = []
            if table_match:
                table_content = table_match.group(1)
                # Get each row from the table
                rows = re.findall(r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|', table_content)
                
                for row in rows:
                    # The first cell in each row contains the step
                    step_content = row[0].strip()
                    # Remove any existing step numbering
                    step_content = re.sub(r'^\d+\.\s*', '', step_content)
                    steps.append(step_content)
            
            if steps:
                formatted_tc += "Steps:\n"
                for i, step in enumerate(steps, 1):
                    formatted_tc += f"{i}. {step}\n"
            
            formatted_content += formatted_tc
            formatted_content += "\n" + "-" * 50 + "\n\n"
            
            # Mark this TC as processed
            processed_tcs.add(tc_num)
        
        # Find all TCs in the content to ensure we catch any with different formats
        all_tc_pattern = r'\*\*TC(\d+):\s*(.*?)\*\*'
        all_tc_matches = re.findall(all_tc_pattern, markdown_content)
        
        for tc_num, tc_name in all_tc_matches:
            if tc_num not in processed_tcs:
                # Handle TCs that weren't caught by the first pattern
                formatted_tc = f"TC{tc_num}: {tc_name}\n\n"
                
                # Try to extract the title
                title_pattern = r'\*\*TC' + re.escape(tc_num) + r':.*?\n+\s*-\s*\*\*Title\*\*:\s*(.*?)(?=\n)'
                title_match = re.search(title_pattern, markdown_content, re.DOTALL)
                if title_match:
                    tc_title = title_match.group(1).strip()
                    formatted_tc += f"Title: {tc_title}\n\n"
                
                # Extract preconditions with a more flexible pattern
                precond_pattern = r'\*\*TC' + re.escape(tc_num) + r':.*?(?:Preconditions|Prerequisites).*?:(.*?)(?=\n\s*-\s*\*\*|\n\s*\||Priority)'
                precond_match = re.search(precond_pattern, markdown_content, re.DOTALL | re.IGNORECASE)
                
                if precond_match:
                    precond = precond_match.group(1).strip()
                    
                    # Check for multiple preconditions by looking for bullet points
                    if re.search(r'-\s+', precond):
                        # Extract individual preconditions
                        precond_items = re.findall(r'-\s+(.*?)(?=\s*-\s+|\s*$)', precond + " ")
                        
                        if len(precond_items) > 1:
                            formatted_tc += "Preconditions:\n"
                            for item in precond_items:
                                item_text = item.strip()
                                if item_text:
                                    formatted_tc += f"- {item_text}\n"
                        else:
                            # If we only find one despite the bullet point, format as single
                            formatted_tc += f"Preconditions: {precond_items[0].strip()}\n"
                    else:
                        # Single precondition without bullet points
                        formatted_tc += f"Preconditions: {precond}\n"
                else:
                    formatted_tc += "Preconditions: None\n"
                
                formatted_tc += "\n"  # Add extra line after preconditions
                
                # Try to find steps in various formats
                step_patterns = [
                    r'\*\*TC' + re.escape(tc_num) + r':.*?\|\s*(?:\*\*)?Steps(?:\*\*)?\s*\|.*?\n\|[\s-]+\|[\s-]+\|\n((?:\|.*?\|.*?\|\n)+)',
                    r'\*\*TC' + re.escape(tc_num) + r':.*?Steps:\s*\n((?:\d+\.\s*.*?\n)+)'
                ]
                
                steps = []
                for pattern in step_patterns:
                    step_match = re.search(pattern, markdown_content, re.DOTALL)
                    if step_match:
                        step_content = step_match.group(1)
                        if '|' in step_content:
                            # It's a table format
                            step_rows = re.findall(r'\|\s*(.*?)\s*\|', step_content)
                            for row in step_rows:
                                if row.strip() and not all(c in '-|' for c in row):
                                    clean_step = re.sub(r'^\d+\.\s*', '', row.strip())
                                    if clean_step:
                                        steps.append(clean_step)
                        else:
                            # It's a list format
                            step_lines = step_content.split('\n')
                            for line in step_lines:
                                if line.strip():
                                    clean_step = re.sub(r'^\d+\.\s*', '', line.strip())
                                    if clean_step:
                                        steps.append(clean_step)
                        break
                
                if steps:
                    formatted_tc += "Steps:\n"
                    for i, step in enumerate(steps, 1):
                        formatted_tc += f"{i}. {step}\n"
                
                formatted_content += formatted_tc
                formatted_content += "\n" + "-" * 50 + "\n\n"
                processed_tcs.add(tc_num)
        
        # Remove the last separator if present
        if formatted_content.endswith("-" * 50 + "\n\n"):
            formatted_content = formatted_content[:-len("-" * 50 + "\n\n")]
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write the formatted content to the output file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(formatted_content)

        return {
            "status": "success",
            "message": f"Test cases formatted and saved to {output_file}",
            "file_path": output_file,
            "content": formatted_content
        }

    except Exception as e:
        return {
            "status": "error", 
            "message": f"Error processing content: {str(e)}",
            "error_type": type(e).__name__
        }

@mcp.tool()
async def convert_to_markdown(uri: str) -> str:
    """Convert a resource described by an http:, https:, file: or data: URI to markdown"""
    return MarkItDown().convert_uri(uri).markdown

# Setup servers
def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

# Main entry point
def main():
    import argparse

    mcp_server = mcp._mcp_server

    parser = argparse.ArgumentParser(description="Run MCP SSE-based MarkItDown server")

    parser.add_argument(
        "--sse",
        action="store_true",
        help="Run the server with SSE transport rather than STDIO (default: False)",
    )
    parser.add_argument(
        "--host", default=None, help="Host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", type=int, default=None, help="Port to listen on (default: 3001)"
    )
    args = parser.parse_args()

    if not args.sse and (args.host or args.port):
        parser.error("Host and port arguments are only valid when using SSE transport.")
        sys.exit(1)

    if args.sse:
        starlette_app = create_starlette_app(mcp_server, debug=True)
        uvicorn.run(
            starlette_app,
            host=args.host if args.host else "127.0.0.1",
            port=args.port if args.port else 3001,
        )
    else:
        mcp.run()


if __name__ == "__main__":
    main()