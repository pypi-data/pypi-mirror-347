# Chroma MCP Server

[![CI](https://github.com/djm81/chroma_mcp_server/actions/workflows/tests.yml/badge.svg)](https://github.com/djm81/chroma_mcp_server/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/djm81/chroma_mcp_server/branch/main/graph/badge.svg)](https://codecov.io/gh/djm81/chroma_mcp_server)
[![PyPI - Version](https://img.shields.io/pypi/v/chroma-mcp-server?color=blue)](https://pypi.org/project/chroma-mcp-server)

A Model Context Protocol (MCP) server integration for [Chroma](https://www.trychroma.com/), the open-source embedding database.

## Motivation: AI Development Working Memory

In AI-assisted development workflows, particularly when using tools like Cursor or GitHub Copilot over multiple sessions, maintaining context from previous interactions is crucial but often manual. Developers frequently resort to creating temporary markdown files or other artifacts simply to capture and reload context into a new chat session.

The Chroma MCP Server aims to streamline this process by providing a persistent, searchable "working memory":

- **Automated Context Recall:** Instead of manual context loading, AI assistants (guided by specific rules or instructions) can query this MCP server to retrieve relevant information from past sessions based on the current development task.
- **Developer-Managed Persistence:** Developers can actively summarize key decisions, code snippets, or insights from the current session and store them in ChromaDB via the MCP interface. This allows building a rich, task-relevant knowledge base over time.
- **Separation of Concerns:** This "working memory" is distinct from final user-facing documentation or committed code artifacts, focusing specifically on capturing the transient but valuable context of the development process itself.

By integrating ChromaDB through MCP, this server facilitates more seamless and context-aware AI-assisted development, reducing manual overhead and improving the continuity of complex tasks across multiple sessions.

Learn more about how this approach creates an integrated "Second Brain" in the [Getting Started with your Second Brain guide](docs/getting_started_second_brain.md).

## Overview

The Chroma MCP Server allows you to connect AI applications with Chroma through the Model Context Protocol. Beyond standard MCP interactions, this implementation emphasizes creating a persistent, automatically updated "Second Brain" for development by integrating:

- **Automated Codebase Indexing:** Tools and configurations (like Git hooks calling a dedicated `chroma-mcp-client`) enable automatic indexing of code changes into a designated Chroma collection.
- **Automated Chat Logging:** IDE rules (like `auto_log_chat` for Cursor) facilitate automatic summarization and logging of AI chat interactions into a separate Chroma collection.
- **Working Memory Tools:** Specialized MCP commands for capturing and retrieving structured thoughts and development context.

**Note on Ongoing Development:** The advanced features discussed in the "Second Brain" concept, particularly the later phases involving automated reinforcement learning and model fine-tuning (`Phase 2` and `Phase 3` of the `docs/refactoring/local_rag_pipeline_plan_v4.md`), are currently under active implementation. The foundational `Phase 1` features (automated indexing, chat logging, working memory) are largely complete and ready for use.

This enables AI models to:

- Store and retrieve embeddings
- Perform semantic search on vector data
- Manage collections of embeddings
- Support RAG (Retrieval Augmented Generation) workflows

See the [API Reference](docs/api_reference.md) for a detailed list of available tools and their parameters.

## Installation

Choose your preferred installation method:

### Standard Installation

```bash
# Using pip
pip install chroma-mcp-server

# Using UVX (recommended for Cursor)
uv pip install chroma-mcp-server
```

### Full Installation (with embedding models)

```bash
# Using pip
pip install chroma-mcp-server[full]

# Using UVX
uv pip install "chroma-mcp-server[full]"
```

### Via Smithery (for Local Execution)

[Smithery](https://smithery.ai/) acts as a registry and local launcher for MCP servers. AI clients like Claude Desktop can use Smithery to find, install, and run your server locally.

```bash
# Requires Node.js/npx
# Installs the package (usually via pip) into a Smithery-managed environment
npx -y @smithery/cli install chroma-mcp-server

# If the server requires an API key for installation via Smithery:
# npx -y @smithery/cli install chroma-mcp-server --key YOUR_API_KEY
```

*(Note: This method requires the package to be published on PyPI and registered with Smithery. The `--key` option usage depends on the specific server's registration settings on Smithery).*

## Usage

### Starting the server

```bash
# Using the command-line executable (after pip/uvx install)
chroma-mcp-server [OPTIONS]

# Or using the Python module (in an environment where it's installed)
python -m chroma_mcp.cli [OPTIONS]

# Or via Smithery CLI (after npx ... install)
# Example with config:
npx -y @smithery/cli run chroma-mcp-server --config '{ "clientType": "persistent", "dataDir": "./my_chroma_data" }'

# Example if the server requires an API key for running via Smithery:
# npx -y @smithery/cli run chroma-mcp-server --key YOUR_API_KEY --config '{...}'
```

### Checking the Version

```bash
chroma-mcp-server --version
```

### Configuration

Copy the example `.env.template` to `.env` and adjust values as needed:

```bash
cp .env.template .env
```

The server can be configured with command-line options or environment variables:

#### Command-line Options

```bash
# Example setting mode to stdio
chroma-mcp-server --mode stdio --client-type persistent --data-dir ./my_data
# Example using default http mode
chroma-mcp-server --client-type persistent --data-dir ./my_data --log-dir ./logs --embedding-function accurate
```

#### Environment Variables

```bash
export CHROMA_SERVER_MODE=stdio # Optional, defaults to http
export CHROMA_CLIENT_TYPE=persistent
export CHROMA_DATA_DIR=./my_data
export CHROMA_LOG_DIR=./logs
export CHROMA_EMBEDDING_FUNCTION=accurate
chroma-mcp-server
```

#### Available Configuration Options

- `--mode`: Server mode (`stdio` or `http`, default: `http`). Also configurable via `CHROMA_SERVER_MODE`.
- `--client-type`: Type of Chroma client (`ephemeral`, `persistent`, `http`, `cloud`). Also configurable via `CHROMA_CLIENT_TYPE`.
- `--data-dir`: Path to data directory for persistent client. Also configurable via `CHROMA_DATA_DIR`.
- `--log-dir`: Path to log directory. Also configurable via `CHROMA_LOG_DIR`.
- `--host`: Host address for HTTP client. Also configurable via `CHROMA_HOST`.
- `--port`: Port for HTTP client. Also configurable via `CHROMA_PORT`.
- `--ssl`: Whether to use SSL for HTTP client. Also configurable via `CHROMA_SSL`.
- `--tenant`: Tenant ID for Cloud client. Also configurable via `CHROMA_TENANT`.
- `--database`: Database name for Cloud client. Also configurable via `CHROMA_DATABASE`.
- `--api-key`: API key for Cloud client. Also configurable via `CHROMA_API_KEY`.
- `--cpu-execution-provider`: Force CPU execution provider for local embedding functions (`auto`, `true`, `false`). Also configurable via `CHROMA_CPU_EXECUTION_PROVIDER`.
- `--embedding-function`: Name of the embedding function to use. Choices: 'default'/'fast' (Local CPU, balanced), 'accurate' (Local CPU/GPU via sentence-transformers, higher accuracy), 'openai' (API, general purpose), 'cohere' (API, retrieval/multilingual focus), 'huggingface' (API, flexible model choice), 'jina' (API, long context focus), 'voyageai' (API, retrieval focus), 'gemini' (API, general purpose). API-based functions require corresponding API keys set as environment variables (e.g., OPENAI_API_KEY). Also configurable via `CHROMA_EMBEDDING_FUNCTION`.
  - **Important:** If you change this setting for a project with an existing ChromaDB collection, you might encounter an `Embedding function name mismatch` error. Use the `chroma-client update-collection-ef` command to update the collection's metadata. See the [chroma-client documentation](docs/scripts/chroma-client.md) for details.

See [Getting Started](docs/getting_started.md) for more setup details.

### Cursor Integration

To use with Cursor, add or modify the `.cursor/mcp.json` file in your project root. Here's an example configuration defining development (`chroma_dev`), testing (`chroma_test`), and production (`chroma_prod`) server setups:

```json
{
  "mcpServers": {
    "chroma_dev": {
      "command": "/path/to/project/scripts/run_chroma_mcp_server_dev.sh",
      "args": [],
      "env": {
        "CHROMA_CLIENT_TYPE": "persistent",
        "CHROMA_DATA_DIR": "/path/to/your/dev_data",
        "CHROMA_LOG_DIR": "/path/to/your/dev_logs",
        "LOG_LEVEL": "DEBUG",
        "MCP_LOG_LEVEL": "DEBUG"
      }
    },
    "chroma_test": {
      "command": "uvx",
      "args": [
        "--refresh",
        "--default-index", "https://test.pypi.org/simple/",
        "--index", "https://pypi.org/simple/",
        "--index-strategy", "unsafe-best-match",
        "chroma-mcp-server@latest"
      ],
      "env": {
        "CHROMA_CLIENT_TYPE": "persistent",
        "CHROMA_DATA_DIR": "/path/to/your/test_data",
        "CHROMA_LOG_DIR": "/path/to/your/test_logs",
        "LOG_LEVEL": "INFO",
        "MCP_LOG_LEVEL": "INFO"
      }
    },
    "chroma_prod": {
      "command": "uvx",
      "args": [
        "chroma-mcp-server"
      ],
      "env": {
        "CHROMA_CLIENT_TYPE": "persistent",
        "CHROMA_DATA_DIR": "/path/to/your/prod_data",
        "CHROMA_LOG_DIR": "/path/to/your/prod_logs",
        "LOG_LEVEL": "INFO",
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Notes:**

- Replace `/path/to/project/scripts/run_chroma_mcp_server_dev.sh` with the actual absolute path to the script in your development environment.
- Replace `/path/to/your/...` placeholders with actual paths for your data and log directories. It's recommended to use separate directories for dev, test, and prod to avoid data conflicts.
- The `chroma_dev` configuration uses the `run_chroma_mcp_server_dev.sh` script, which runs the server directly from your local source code using Hatch. This is ideal for rapid development and testing changes without reinstalling.
- The `chroma_test` configuration uses `uvx` to fetch and run the *latest* version available on TestPyPI. This is useful for testing release candidates.
- The `chroma_prod` configuration uses `uvx` to run the version of `chroma-mcp-server` that is currently installed globally via `uvx` (typically the latest stable release from PyPI).

See [Cursor Integration](docs/cursor_integration.md) for more details.

## Development

For instructions on how to set up the development environment, run tests, build the package, and contribute, please see the **[Developer Guide](docs/developer_guide.md)**.

Running the server during development is typically done using the `scripts/run_chroma_mcp_server_dev.sh` wrapper script, which leverages Hatch. See the Developer Guide for specifics.

**Important:** After modifying the code (server, client, etc.), you must rebuild and reinstall the package within the Hatch environment for changes to take effect:

```bash
# Replace <version> with the actual version built
hatch build && hatch run pip uninstall chroma-mcp-server -y && hatch run pip install 'dist/chroma_mcp_server-<version>-py3-none-any.whl[full,dev]'
```

## Working Memory and Thinking Tools

This server includes specialized tools for creating a persistent, searchable "working memory" to aid AI development workflows. Learn more about how these tools leverage embeddings to manage context across sessions in the **[Embeddings and Thinking Tools Guide](docs/thinking_tools/embeddings_and_thinking.md)**.

## Testing the Tools

A simulated workflow using the MCP tools is available in the **[MCP Test Flow](docs/mcp_test_flow.md)** document.

## License

MIT License (see [LICENSE](LICENSE))
