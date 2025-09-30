"""
MCP Server implementation for Obsidian vault interaction using FastMCP
"""

import os
import sys
import json
import logging
import argparse
from typing import Optional, List, Dict, Any

from mcp.server.fastmcp import FastMCP
from obsidian import ObsidianVault

logger = logging.getLogger(__name__)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Obsidian MCP Server")
parser.add_argument("--readonly", action="store_true", help="Run server in readonly mode (disable write/delete operations)")
args = parser.parse_args()

# Initialize FastMCP server
mcp = FastMCP("obsidian-vault-server")

# Initialize Obsidian vault
vault = ObsidianVault(os.getenv("OBSIDIAN_VAULT_PATH"))


@mcp.tool()
def list_notes(folder: Optional[str] = None) -> str:
    """List all notes in the Obsidian vault

    Args:
        folder: Optional folder path to list notes from
    """
    notes = vault.list_notes(folder)
    return json.dumps(notes, indent=2)


@mcp.tool()
def read_note(path: str) -> str:
    """Read the content of a specific note

    Args:
        path: Path to the note relative to vault root
    """
    content = vault.read_note(path)
    if content is not None:
        return content
    else:
        return f"Note not found: {path}"


if not args.readonly:
    @mcp.tool()
    def write_note(path: str, content: str) -> str:
        """Create or update a note in the vault

        Args:
            path: Path where the note should be saved
            content: Content of the note in Markdown format
        """
        success = vault.write_note(path, content)
        if success:
            return f"Note saved successfully: {path}"
        else:
            return f"Failed to save note: {path}"


    @mcp.tool()
    def delete_note(path: str) -> str:
        """Delete a note from the vault

        Args:
            path: Path to the note to delete
        """
        success = vault.delete_note(path)
        if success:
            return f"Note deleted successfully: {path}"
        else:
            return f"Failed to delete note or note not found: {path}"


@mcp.tool()
def search_notes(query: str) -> str:
    """Search for notes containing specific text

    Args:
        query: Text to search for in notes
    """
    results = vault.search_notes(query)
    return json.dumps(results, indent=2)


@mcp.tool()
def get_metadata(path: str) -> str:
    """Get frontmatter metadata from a note

    Args:
        path: Path to the note
    """
    metadata = vault.get_note_metadata(path)
    if metadata is not None:
        return json.dumps(metadata, indent=2)
    else:
        return f"Note not found: {path}"


@mcp.resource("obsidian://note/{path}")
def read_note_resource(path: str) -> str:
    """Read a specific note as a resource

    Args:
        path: Path to the note
    """
    content = vault.read_note(path)
    if content:
        return content
    raise ValueError(f"Resource not found: {path}")


if __name__ == "__main__":
    mode = "readonly" if args.readonly else "read-write"
    logger.info(f"Starting Obsidian MCP Server ({mode}) with vault at: {vault.vault_path}")
    mcp.run(transport="stdio")
