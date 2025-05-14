#!/usr/bin/env python3

import asyncio
import os
import re
import json
import logging
from typing import Any, Dict, List, Tuple
import concurrent.futures

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
# Fallback to explicit .env paths for uvx and other environments
env_paths = [
    os.path.join(os.getcwd(), ".env"),
    os.path.expanduser("~/.mcp-figma-tools/.env"),
]
for env_path in env_paths:
    if os.path.exists(env_path):
        load_dotenv(env_path)
        logger.debug(f"Loaded .env from {env_path}")
        break

logger.info("Current working directory: %s", os.getcwd())
# logger.info("FIGMA_API_TOKEN: %s", os.getenv("FIGMA_API_TOKEN") or "Not found")

FIGMA_API_TOKEN = os.getenv("FIGMA_API_TOKEN")
BASE_URL = "https://api.figma.com/v1"

if not FIGMA_API_TOKEN:
    logger.error("FIGMA_API_TOKEN is not set. Server will not function correctly.")

# Initialize FastMCP server
mcp = FastMCP(
    name="figma-tools",
    version="0.1.0",
    description="MCP server for interacting with the Figma API using FastMCP. Provides tools to fetch file data, screen info, node details, and image URLs."
)

# Global ThreadPoolExecutor
_THREAD_POOL_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=(os.cpu_count() or 4))

def _run_coroutine_in_new_thread(coroutine_to_run):
    """Helper to execute asyncio.run(coroutine) in a separate thread."""
    return asyncio.run(coroutine_to_run)

async def _extract_file_key_from_url_async(figma_url: str) -> str:
    """Async: Extracts the Figma file key from various Figma URL formats."""
    pattern = r"figma\.com/(?:file|design)/([a-zA-Z0-9_-]+)"
    match = re.search(pattern, figma_url)
    if match:
        return match.group(1)
    board_pattern = r"figma\.com/(?:board|file|design)/([a-zA-Z0-9_-]+)"
    board_match = re.search(board_pattern, figma_url)
    if board_match:
        return board_match.group(1)
    parts = figma_url.split('/')
    for part in reversed(parts):
        if re.match(r"^[a-zA-Z0-9_-]{20,}$", part):
            key_candidate = part.split('?')[0] if '?' in part else part
            if re.match(r"^[a-zA-Z0-9_-]{20,}$", key_candidate):
                return key_candidate
    raise ValueError(f"Invalid Figma URL: Could not extract file key from {figma_url}")

async def _make_figma_api_request_async(url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Async: Helper function to make authorized GET requests to the Figma API."""
    if not FIGMA_API_TOKEN:
        raise ValueError("FIGMA_API_TOKEN is not configured.")
    headers = {"X-Figma-Token": FIGMA_API_TOKEN}
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            logger.debug(f"Async Figma API: GET {url} with params: {params}")
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Figma API HTTP error ({e.response.status_code}) for {url}: {e.response.text}")
            if e.response.status_code == 403:
                raise Exception(f"Access denied to Figma API. Check token. Details: {e.response.text}")
            elif e.response.status_code == 404:
                raise Exception(f"Figma resource not found. Check URL/key. Details: {e.response.text}")
            else:
                raise Exception(f"Figma API error ({e.response.status_code}): {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Network error calling Figma API ({url}): {e}")
            raise Exception(f"Network error: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error from Figma API ({url}): {e}. Response: {response.text[:200]}")
            raise Exception(f"JSON decode error: {e}")

async def _fetch_figma_file_data_async(file_key: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/files/{file_key}"
    return await _make_figma_api_request_async(url)

async def _fetch_node_details_async(file_key: str, node_ids: List[str]) -> Dict[str, Any]:
    if not node_ids:
        return {"nodes": {}}
    ids_param = ",".join(node_ids)
    url = f"{BASE_URL}/files/{file_key}/nodes?ids={ids_param}"
    return await _make_figma_api_request_async(url)

async def _fetch_figma_node_image_urls_async(
    file_key: str, node_ids: List[str], scale: float = 1.0,
    format_str: str = "png", use_absolute_bounds: bool = True
) -> Dict[str, str | None]:
    if not node_ids:
        return {}
    max_ids_per_request = 50
    image_urls_map: Dict[str, str | None] = {}
    for i in range(0, len(node_ids), max_ids_per_request):
        batch_ids = node_ids[i : i + max_ids_per_request]
        params = {
            "ids": ",".join(batch_ids), "scale": str(scale),
            "format": format_str, "use_absolute_bounds": "true" if use_absolute_bounds else "false",
        }
        url = f"{BASE_URL}/images/{file_key}"
        try:
            data = await _make_figma_api_request_async(url, params=params)
            if data.get("err"):
                logger.error(f"Figma image render error for {batch_ids}: {data['err']}")
                for node_id in batch_ids:
                    image_urls_map.setdefault(node_id, None)
            if "images" in data and data["images"]:
                image_urls_map.update(data["images"])
            for node_id in batch_ids:
                image_urls_map.setdefault(node_id, data.get("images", {}).get(node_id))
        except Exception as e:
            logger.error(f"Failed to fetch image batch {batch_ids}: {e}")
            for node_id in batch_ids:
                image_urls_map.setdefault(node_id, None)
    return image_urls_map

def _extract_top_level_frames_from_file_data(
    file_data: Dict[str, Any]
) -> Tuple[List[Dict[str, Any]], List[str]]:
    frames_meta: List[Dict[str, Any]] = []
    frame_ids: List[str] = []
    document = file_data.get("document", {})
    if not document or not isinstance(document.get("children"), list):
        logger.warning("Document data/children not found/invalid.")
        return frames_meta, frame_ids
    for page in document["children"]:
        if page.get("type") == "CANVAS" and isinstance(page.get("children"), list):
            for node in page["children"]:
                if node.get("type") == "FRAME":
                    bbox = node.get("absoluteBoundingBox", {})
                    frame_data = {
                        "name": node.get("name", "Unnamed Frame"),
                        "node_id": node.get("id", ""),
                        "type": "FRAME",
                        "page_name": page.get("name", "Unnamed Page"),
                        "page_id": page.get("id"),
                        "width": bbox.get("width"),
                        "height": bbox.get("height")
                    }
                    frames_meta.append(frame_data)
                    if node.get("id"):
                        frame_ids.append(node.get("id"))
    return frames_meta, frame_ids

def run_async_tool(async_function_to_call, *args, **kwargs):
    """
    Synchronously calls an async function, managing the event loop appropriately.
    """
    coroutine = async_function_to_call(*args, **kwargs)
    try:
        loop = asyncio.get_event_loop_policy().get_event_loop()
        if loop.is_running():
            logger.debug(f"Detected running event loop. Offloading {async_function_to_call.__name__} to thread pool.")
            future = _THREAD_POOL_EXECUTOR.submit(_run_coroutine_in_new_thread, coroutine)
            return future.result()
        else:
            logger.debug(f"Detected non-running event loop. Running {async_function_to_call.__name__} directly.")
            return loop.run_until_complete(coroutine)
    except RuntimeError as e:
        if "no current event loop" in str(e).lower():
            logger.debug(f"No event loop found. Running {async_function_to_call.__name__} with new loop via asyncio.run().")
            return asyncio.run(coroutine)
        else:
            logger.error(f"Unexpected RuntimeError in run_async_tool for {async_function_to_call.__name__}: {e}", exc_info=True)
            raise
    except Exception as e:
        logger.error(f"Generic error in run_async_tool for {async_function_to_call.__name__}: {e}", exc_info=True)
        raise

@mcp.tool()
def get_figma_file_json(figma_url: str) -> Dict[str, Any]:
    """
    Fetches the complete JSON representation of a Figma file.
    Args:
        figma_url: The URL of the Figma file (e.g., https://www.figma.com/file/FILE_KEY/...).
    Returns:
        A dictionary containing the Figma file's JSON data, or an error object.
    """
    try:
        logger.info(f"Tool 'get_figma_file_json' for URL: {figma_url}")
        return run_async_tool(_get_figma_file_json_async, figma_url)
    except Exception as e:
        logger.error(f"Error in 'get_figma_file_json' for {figma_url}: {e}", exc_info=True)
        return {"error": str(e), "details": "Failed to fetch Figma file JSON."}

async def _get_figma_file_json_async(figma_url: str) -> Dict[str, Any]:
    file_key = await _extract_file_key_from_url_async(figma_url)
    file_data = await _fetch_figma_file_data_async(file_key)
    logger.info(f"Successfully fetched JSON for Figma file key: {file_key}")
    return file_data

@mcp.tool()
def get_figma_screens_info(figma_url: str, scale: float = 1.0, image_format: str = "png") -> Dict[str, Any]:
    """
    Extracts top-level frames (screens) from a Figma file and retrieves their image URLs.
    Args:
        figma_url: The URL of the Figma file.
        scale: The scale factor for exported images (e.g., 1.0, 2.0). Defaults to 1.0.
        image_format: The image format ("png", "jpg", "svg", "pdf"). Defaults to "png".
    Returns:
        A dictionary with a "frames" key, or an error object.
    """
    try:
        logger.info(f"Tool 'get_figma_screens_info' for URL: {figma_url}")
        return run_async_tool(_get_figma_screens_info_async, figma_url, scale, image_format)
    except Exception as e:
        logger.error(f"Error in 'get_figma_screens_info' for {figma_url}: {e}", exc_info=True)
        return {"error": str(e), "frames": [], "details": "Failed to fetch screen info."}

async def _get_figma_screens_info_async(figma_url: str, scale: float, image_format: str) -> Dict[str, Any]:
    file_key = await _extract_file_key_from_url_async(figma_url)
    file_data = await _fetch_figma_file_data_async(file_key)
    frames_meta, frame_ids = _extract_top_level_frames_from_file_data(file_data)
    if not frame_ids:
        logger.info(f"No top-level frames in Figma file: {file_key}")
        return {"frames": []}
    logger.info(f"Found {len(frame_ids)} frames for {file_key}. Fetching images...")
    image_urls_map = await _fetch_figma_node_image_urls_async(file_key, frame_ids, scale, image_format)
    enriched_frames = []
    for frame in frames_meta:
        node_id = frame["node_id"]
        frame["image_url"] = image_urls_map.get(node_id)
        if frame["image_url"] is None:
            logger.warning(f"No image URL/error for frame {node_id} ('{frame['name']}') in {file_key}.")
        enriched_frames.append(frame)
    logger.info(f"Fetched screen info for Figma file: {file_key}")
    return {"frames": enriched_frames}

@mcp.tool()
def get_figma_node_details_json(figma_url: str, node_ids: str) -> Dict[str, Any]:
    """
    Fetches JSON for specific nodes in a Figma file.
    Args:
        figma_url: The URL of the Figma file.
        node_ids: Comma-separated string of node IDs (e.g., "1:2,3:4").
    Returns:
        A dictionary with node data, or an error object.
    """
    try:
        logger.info(f"Tool 'get_figma_node_details_json' for {figma_url}, nodes: {node_ids}")
        return run_async_tool(_get_figma_node_details_json_async, figma_url, node_ids)
    except Exception as e:
        logger.error(f"Error in 'get_figma_node_details_json' for {figma_url}, nodes {node_ids}: {e}", exc_info=True)
        return {"error": str(e), "details": "Failed to fetch node details."}

async def _get_figma_node_details_json_async(figma_url: str, node_ids_str: str) -> Dict[str, Any]:
    file_key = await _extract_file_key_from_url_async(figma_url)
    node_id_list = [nid.strip() for nid in node_ids_str.split(',') if nid.strip()]
    if not node_id_list:
        raise ValueError("node_ids parameter is empty or just commas.")
    nodes_data = await _fetch_node_details_async(file_key, node_id_list)
    logger.info(f"Fetched details for nodes: {node_ids_str} in file {file_key}")
    return nodes_data

@mcp.tool()
def get_figma_node_image_url(figma_url: str, node_id: str, scale: float = 1.0, image_format: str = "png") -> Dict[str, Any]:
    """
    Fetches the image URL for a specific node in a Figma file.
    Args:
        figma_url: The URL of the Figma file.
        node_id: The ID of the single node (e.g., "1:2").
        scale: Scale factor for export. Defaults to 1.0.
        image_format: Image format ("png", "jpg", "svg", "pdf"). Defaults to "png".
    Returns:
        Dict with "node_id" and "image_url", or an error object.
    """
    try:
        logger.info(f"Tool 'get_figma_node_image_url' for {figma_url}, node: {node_id}, format: {image_format}")
        return run_async_tool(_get_figma_node_image_url_async, figma_url, node_id, scale, image_format)
    except Exception as e:
        logger.error(f"Error in 'get_figma_node_image_url' for {figma_url}, node {node_id}: {e}", exc_info=True)
        return {"error": str(e), "node_id": node_id, "image_url": None, "details": "Failed to fetch node image URL."}

async def _get_figma_node_image_url_async(figma_url: str, node_id_str: str, scale: float, image_format: str) -> Dict[str, Any]:
    file_key = await _extract_file_key_from_url_async(figma_url)
    clean_node_id = node_id_str.strip()
    if not clean_node_id:
        raise ValueError("node_id parameter is empty.")
    image_urls_map = await _fetch_figma_node_image_urls_async(file_key, [clean_node_id], scale, image_format)
    img_url = image_urls_map.get(clean_node_id)
    if img_url is None and clean_node_id in image_urls_map:
        logger.warning(f"Figma render error for node {clean_node_id} in {file_key} (format: {image_format}).")
    elif img_url is None:
        raise Exception(f"Could not get image URL for node {clean_node_id} (format: {image_format}). Invalid ID or not renderable.")
    logger.info(f"Fetched image URL for node: {clean_node_id} in file {file_key}")
    return {"node_id": clean_node_id, "image_url": img_url}

def main():
    try:
        if not FIGMA_API_TOKEN:
            logger.critical("CRITICAL: FIGMA_API_TOKEN is not set. The Figma MCP server will not start.")
            raise ValueError("FIGMA_API_TOKEN environment variable is required")
        logger.info("Starting Figma MCP Server (FastMCP)...")
        mcp.run()
        logger.info("Figma MCP Server stopped.")
    except KeyboardInterrupt:
        logger.info("Figma MCP Server shutting down due to KeyboardInterrupt.")
    except Exception as e:
        logger.critical(f"Figma MCP Server crashed: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()