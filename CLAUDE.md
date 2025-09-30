# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server implementation for interacting with Obsidian vaults. It provides programmatic access to Obsidian notes through a set of tools that enable reading, writing, searching, and managing markdown files.

## Architecture

The codebase consists of two main components:

1. **MCP Server** (`main.py`): FastMCP-based server that exposes tools and resources for vault interaction. It acts as the protocol layer, handling MCP requests and responses.

2. **Vault Abstraction** (`obsidian/vault.py`): `ObsidianVault` class that handles all file system operations. This layer is vault-aware and handles path resolution, markdown file filtering, and content operations.

The server depends on the vault path being set via the `OBSIDIAN_VAULT_PATH` environment variable. If not set, it defaults to `~/Documents/Obsidian`.

## Development Commands

### Running the Server
```bash
# Using the convenience script (defaults to ~/Documents/Obsidian if OBSIDIAN_VAULT_PATH not set)
./start_server.sh                    # Standard mode (read-write)
./start_server.sh --readonly         # Readonly mode

# Or run directly with custom vault path
OBSIDIAN_VAULT_PATH="/Users/mihai.neagu/Library/CloudStorage/OneDrive-DanteInternationalS.A(2)/Teams/SOLID" python3.11 main.py
OBSIDIAN_VAULT_PATH="/Users/mihai.neagu/Library/CloudStorage/OneDrive-DanteInternationalS.A(2)/Teams/SOLID" python3.11 main.py --readonly
```

The server runs in stdio transport mode for MCP communication.

#### Readonly Mode
When started with the `--readonly` flag, the server only exposes readonly tools (`list_notes`, `read_note`, `search_notes`, `get_metadata`). The write operations (`write_note`, `delete_note`) are not available.

### Environment Setup
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

### Required Environment Variables
- `OBSIDIAN_VAULT_PATH`: Path to the Obsidian vault directory

## Tools Provided

The MCP server exposes these tools:
- `list_notes(folder)`: List all notes, optionally filtered by folder
- `read_note(path)`: Read note content
- `write_note(path, content)`: Create or update notes
- `delete_note(path)`: Delete notes
- `search_notes(query)`: Case-insensitive full-text search
- `get_metadata(path)`: Extract YAML frontmatter

## Resources

- `obsidian://note/{path}`: URI-based note access pattern

## Notes

- All note paths are relative to the vault root
- The `.md` extension is automatically added if not provided when writing notes
- Search returns up to 5 matching lines per note
- Frontmatter parsing requires YAML but falls back to raw lines if parsing fails
