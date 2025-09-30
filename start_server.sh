#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Set default vault path if not already set
if [ -z "$OBSIDIAN_VAULT_PATH" ]; then
    export OBSIDIAN_VAULT_PATH="$HOME/Documents/Obsidian"
fi

# Run the MCP server with all passed arguments
python3.11 main.py "$@"
