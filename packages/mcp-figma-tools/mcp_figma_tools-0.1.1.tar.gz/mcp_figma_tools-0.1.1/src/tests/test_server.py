import pytest
import asyncio
from mcp_figma_tools.server import _extract_file_key_from_url_async

@pytest.mark.asyncio
async def test_extract_file_key():
    # Valid Figma URLs
    urls = [
        "https://www.figma.com/file/abc123xyz/MyFile",
        "https://www.figma.com/design/abc123xyz/MyDesign",
        "https://www.figma.com/board/abc123xyz/MyBoard",
        "https://figma.com/file/abc123xyz",
    ]
    for url in urls:
        file_key = await _extract_file_key_from_url_async(url)
        assert file_key == "abc123xyz", f"Failed to extract file key from {url}"

    # Invalid URL
    with pytest.raises(ValueError):
        await _extract_file_key_from_url_async("https://example.com/invalid")

def test_sync_extract_file_key():
    # Test sync wrapper if needed
    from mcp_figma_tools.server import run_async_tool
    result = run_async_tool(_extract_file_key_from_url_async, "https://www.figma.com/file/abc123xyz/MyFile")
    assert result == "abc123xyz"