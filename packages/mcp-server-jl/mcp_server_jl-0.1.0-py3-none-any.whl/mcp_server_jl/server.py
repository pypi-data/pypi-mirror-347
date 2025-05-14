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

# Create an MCP server instance with an identifier ("joblogic")
mcp = FastMCP("joblogic")

# Dictionary to store cached webpage data
webpage_cache = {}

@mcp.tool()
def generate_testcases_for_content_spec(markdown_content: str, spec_file_path: str) -> dict:
    """
    Generate test cases for a markdown specification content and save to file.
    
    Args:
        markdown_content (str): The markdown specification content.
        spec_file_path (str): The file path of the spec markdown file.

    Returns:
        dict: Contains the generated test cases and file path info
    """
    import os
    import re
    import time

    API_URL = "https://flowise-app.com"
    PROMPT = """
Please generate full coverage test cases based on the following specification.
Include positive and negative scenarios, edge cases, validation rules, and permission handling:
"""
    MAX_RETRIES = 3
    TIMEOUT = 60  # seconds per request
    RETRY_DELAY = 2  # seconds between retries

    try:
        if not markdown_content.strip():
            return {"status": "error", "message": "Input content is empty."}

        # Use absolute directory path
        output_dir = r"C:\appstore-starter\TestCases\auto"
        os.makedirs(output_dir, exist_ok=True)

        # Get the spec filename without extension
        spec_name = os.path.splitext(os.path.basename(spec_file_path))[0]

        # Generate a unique filename based on spec name and timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"{spec_name}_{timestamp}.testcase.md")

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
def format_all_testcases(input_folder: str, output_folder: str) -> Dict[str, Any]:
    """
    Force-format all test case files in the input_folder and save cleaned versions into output_folder.
    Keep only TC number, Title, Preconditions, and numbered Steps.
    """
    import re
    import os

    def clean_and_format(input_file: str, output_file: str) -> Dict[str, Any]:
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                content = f.read()

            formatted_content = ""
            
            # Extract test cases with a pattern that better matches the actual format
            tc_pattern = r'\*\*TC(\d+):\s*(.*?)\*\*\s*\n+\s*-\s*\*\*Title\*\*:\s*(.*?)(?=\n)'
            tc_matches = re.findall(tc_pattern, content, re.DOTALL)
            
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
                precond_match = re.search(precond_pattern, content, re.DOTALL)
                
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

                # Extract steps
                steps_pattern = r'\*\*TC' + re.escape(tc_num) + r':.*?(?:\n\s*-\s*\*\*Steps\*\*:)(.*?)(?=\n\s*-\s*\*\*|\Z)'
                steps_match = re.search(steps_pattern, content, re.DOTALL)
                
                if steps_match:
                    steps = steps_match.group(1).strip()
                    
                    # Extract individual steps using numbered list as separators
                    steps_items = re.findall(r'(?:\n|^)\s*\d+\.\s+(.*?)(?=\s*\n\s*\d+\.\s+|\s*$)', steps + "\n")
                    
                    if steps_items:
                        formatted_tc += "Steps:\n"
                        for i, item in enumerate(steps_items, 1):
                            item_text = item.strip()
                            if item_text:
                                formatted_tc += f"{i}. {item_text}\n"
                
                # Add to formatted content with spacing between test cases
                formatted_content += formatted_tc + "\n\n"
                
                # Mark this test case as processed
                processed_tcs.add(tc_num)
            
            # If we couldn't extract any test cases, return an error
            if not processed_tcs:
                return {"status": "error", "message": "No test cases found in file."}
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Save the formatted content
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(formatted_content)
            
            return {
                "status": "success",
                "message": f"Formatted {len(processed_tcs)} test cases.",
                "test_case_count": len(processed_tcs)
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

    try:
        if not os.path.isdir(input_folder):
            return {"status": "error", "message": f"Input folder does not exist: {input_folder}"}
        
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Track statistics
        formatted_count = 0
        error_files = []
        
        # Process each file in the input folder
        for filename in os.listdir(input_folder):
            if filename.endswith(".md") or filename.endswith(".markdown"):
                input_file = os.path.join(input_folder, filename)
                output_file = os.path.join(output_folder, filename)
                
                result = clean_and_format(input_file, output_file)
                
                if result["status"] == "success":
                    formatted_count += 1
                else:
                    error_files.append({
                        "file": filename,
                        "error": result["message"]
                    })
        
        return {
            "status": "completed",
            "formatted": formatted_count,
            "errors": error_files
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Error processing folder: {str(e)}",
            "error_type": type(e).__name__
        }

@mcp.tool()
async def convert_to_markdown(uri: str) -> str:
    """Convert a resource described by an http:, https:, file: or data: URI to markdown"""
    from markitdown import MarkItDown
    return MarkItDown().convert_uri(uri).markdown

async def run_server():
    """Run the MCP server using stdio transport"""
    _server = mcp._mcp_server
    async with stdio_server() as (reader, writer):
        await _server.run(reader, writer, _server.create_initialization_options())
