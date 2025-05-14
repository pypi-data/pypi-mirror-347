mcp-figma-tools
A Python MCP server for interacting with the Figma API. Provides tools to fetch Figma file data, screen information, node details, and image URLs.
Installation
Install the package via pip:
pip install mcp-figma-tools

Setup

Create a .env file in your project directory with your Figma API token:

FIGMA_API_TOKEN=your_figma_api_token


Alternatively, set the FIGMA_API_TOKEN environment variable manually.

Usage
Run the MCP server:
mcp-figma-tools

The server provides the following tools:

get_figma_file_json: Fetches the complete JSON of a Figma file.
get_figma_screens_info: Extracts top-level frames (screens) and their image URLs.
get_figma_node_details_json: Fetches JSON for specific nodes.
get_figma_node_image_url: Fetches the image URL for a specific node.

Configuration
To use the server in a Claude Desktop configuration, add:
{
  "mcpServers": {
    "figma_tools": {
      "command": "uvx",
      "args": [
        "mcp-figma-tools"
      ]
    }
  }
}

Requirements

Python >= 3.9
Figma Personal Access Token (set via FIGMA_API_TOKEN)

License
MIT License
