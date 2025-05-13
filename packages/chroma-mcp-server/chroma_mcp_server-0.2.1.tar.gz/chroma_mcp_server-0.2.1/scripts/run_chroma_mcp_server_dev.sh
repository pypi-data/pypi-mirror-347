#!/bin/bash
# Add known location of user-installed bins to PATH
export PATH="/usr/local/bin:$PATH" # Adjust path as needed
set -euo pipefail
# Run chroma-mcp-server-dev using Hatch

# --- Define Project Root ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# --- Change to Project Root ---
cd "$PROJECT_ROOT"
# Don't print the working directory change as it will break the MCP server integration here
echo "{\"info\": \"Changed working directory to project root: $PROJECT_ROOT\"}" >> logs/run_chroma_mcp_server_dev.log

# Install hatch if not installed
if ! command -v hatch &> /dev/null; then
    echo "{\"warning\": \"Hatch not found. Installing hatch...\"}"
    # Remove output redirection to see installation results/errors
    pip install hatch 2>&1 | tee -a logs/run_chroma_mcp_server_dev.log
fi

# Print the PATH right before attempting to run hatch, redirecting to log
echo "{\"debug\": \"Current PATH before running hatch: $PATH\"}" >> logs/run_chroma_mcp_server_dev.log

hatch run chroma-mcp-server-dev "$@" 2>&1 | tee -a logs/run_chroma_mcp_server_dev.log