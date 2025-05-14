MCP Figma Tools
mcp-figma-tools is a Model Context Protocol (MCP) server that provides seamless integration with the Figma API. It enables users to fetch Figma file data, extract screen information, retrieve node details, and generate image URLs programmatically. Built with performance and reliability in mind, this package leverages asynchronous HTTP requests and robust environment variable handling, making it ideal for developers and MCP-based workflows.
Features

Fetch Figma File JSON: Retrieve the complete JSON representation of a Figma file using get_figma_file_json.
Extract Screen Information: Identify top-level frames (screens) and their image URLs with get_figma_screens_info.
Node Details: Access detailed JSON data for specific Figma nodes using get_figma_node_details_json.
Node Image URLs: Generate image URLs for specific nodes with customizable scale and format via get_figma_node_image_url.
Asynchronous Processing: Uses httpx for efficient, non-blocking API calls.
Environment Variable Management: Supports .env files and multiple fallback paths for FIGMA_API_TOKEN using python-dotenv.
MCP Integration: Designed for use with MCP clients (e.g., Claude Desktop) for seamless tool orchestration.
Robust Logging: Comprehensive logging for debugging and monitoring server operations.
Cross-Platform: Compatible with Python 3.9+ on Windows, macOS, and Linux.

Installation
Install mcp-figma-tools from PyPI:
pip install mcp-figma-tools

For development or testing, you can install from a local build or TestPyPI (see Development section).
Requirements

Python: 3.12 or higher
Dependencies (automatically installed):
mcp>=1.2.0: MCP server framework
httpx>=0.27.0: Asynchronous HTTP client
python-dotenv>=1.0.1: Environment variable management


Figma API Token: Obtain from Figma's API documentation

Setup

Obtain a Figma API Token:

Log in to your Figma account.
Go to your Figma profile settings and generate a personal access token.
Store the token securely (do not share it publicly).


Configure Environment Variables:Create a .env file in your project directory:
echo FIGMA_API_TOKEN=your-api-token > .env

Alternatively, set the environment variable manually:
export FIGMA_API_TOKEN=your-api-token  # Linux/macOS
set FIGMA_API_TOKEN=your-api-token     # Windows PowerShell


Verify Installation:
pip show mcp-figma-tools

Ensure the version is 0.1.0 (or the latest if updated).


Usage
Running the Server
Start the MCP server:
mcp-figma-tools

This launches the server, which listens for MCP client requests. You should see logs like:
2025-05-14 00:10:23,123 - __main__ - INFO - [server.py:XX] - Current working directory: /path/to/mcp-figma-tools
2025-05-14 00:10:23,124 - __main__ - INFO - [server.py:XX] - FIGMA_API_TOKEN: your-api-token
2025-05-14 00:10:23,125 - __main__ - INFO - [server.py:XX] - Starting Figma MCP Server (FastMCP)...

Alternatively, run the server directly via Python:
python -m mcp_figma_tools.server

Using with MCP Client
Integrate with an MCP client (e.g., Claude Desktop) by adding the server to your mcp_config.json:
{
  "mcpServers": {
    "figma": {
      "command": "python",
      "args": ["-m", "mcp_figma_tools.server"],
    }
  }
}

For use with uvx (after publishing to PyPI):
{
  "mcpServers": {
    "figma": {
      "commandteam": "uvx",
      "args": ["mcp-figma-tools"],
      "env": {"FIGMA_API_TOKEN": "your-api-token"},
    }
  }
}

OR

{
  "mcpServers": {
    "figma": {
      "commandteam": "mcp-figma-tools",
      "args": [],
      "env": {"FIGMA_API_TOKEN": "your-api-token"},
    }
  }
}

Available Tools
The server exposes four tools via the MCP protocol:

get_figma_file_json:

Description: Fetches the complete JSON of a Figma file.
Parameters:
figma_url (string): URL of the Figma file (e.g., https://www.figma.com/file/abc123...).


Example:get_figma_file_json(figma_url="https://www.figma.com/file/abc123xyz/MyFile")


Returns: Dictionary containing the file’s JSON data or an error object.


get_figma_screens_info:

Description: Extracts top-level frames (screens) and their image URLs.
Parameters:
figma_url (string): Figma file URL.
scale (float, optional): Image scale factor (default: 1.0).
image_format (string, optional): Image format (png, jpg, svg, pdf; default: png).


Example:get_figma_screens_info(figma_url="https://www.figma.com/file/abc123xyz/MyFile", scale=2.0, image_format="jpg")


Returns: Dictionary with a frames key containing frame metadata and image URLs.


get_figma_node_details_json:

Description: Retrieves JSON data for specific nodes.
Parameters:
figma_url (string): Figma file URL.
node_ids (string): Comma-separated node IDs (e.g., 1:2,3:4).


Example:get_figma_node_details_json(figma_url="https://www.figma.com/file/abc123xyz/MyFile", node_ids="1:2,3:4")


Returns: Dictionary with node data or an error object.


get_figma_node_image_url:

Description: Generates an image URL for a specific node.
Parameters:
figma_url (string): Figma file URL.
node_id (string): Single node ID (e.g., 1:2).
scale (float, optional): Image scale factor (default: 1.0).
image_format (string, optional): Image format (png, jpg, svg, pdf; default: png).


Example:get_figma_node_image_url(figma_url="https://www.figma.com/file/abc123xyz/MyFile", node_id="1:2", scale=1.5)


Returns: Dictionary with node_id and image_url or an error object.



Example Workflow

Start the server:
mcp-figma-tools


Use an MCP client to query:
# Fetch file JSON
result = get_figma_file_json(figma_url="https://www.figma.com/file/abc123xyz/MyFile")
print(result)

# Get screen info with images
screens = get_figma_screens_info(figma_url="https://www.figma.com/file/abc123xyz/MyFile", scale=2.0)
print(screens["frames"])

Contributing
Contributions are welcome! To contribute:

Fork the repository (once hosted on GitHub or similar).
Create a feature branch:git checkout -b feature/your-feature

Commit changes:git commit -m "Add your feature"

Push to the branch:git push origin feature/your-feature

Open a pull request.

Please include tests and update documentation as needed.
License
This project is licensed under the Accellor License. See the LICENSE file for details.
Contact
For issues or questions, contact:


Built with ❤️ for developers and designers working with Figma and MCP.
