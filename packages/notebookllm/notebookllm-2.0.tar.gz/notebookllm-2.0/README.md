# notebookllm

A Python package to bridge the gap between Jupyter Notebooks and Large Language Models (LLMs).

## Why this package?

Current Large Language Models (LLMs) cannot directly read or process `.ipynb` files. This package provides a solution by converting `.ipynb` files to a simplified plain text format that LLMs can easily understand. It also allows converting Python files to `.ipynb` files.

## Features

- Convert `.ipynb` files to a simplified plain text (.py, .txt or .r file) format.
- Convert Python or R (.py, .txt or .r files) to `.ipynb` files.
- The plain text (.py, .txt or .r) format preserves the structure of the notebook, including code and markdown cells, using `# %% [code]` and `# %% [markdown]` identifiers.
- The plain text (.py, .txt or .r) format can be easily parsed back into a `.ipynb` file.

## Installation

```bash
pip install notebookllm
```
or 

```bash
git clone https://github.com/yasirrazaa/notebookllm.git
cd notebookllm
pip install .  
```

## Usage
## CLI

### `to_text`

Converts a `.ipynb` file to a simplified plain text format.

Usage:

```bash
notebookllm to_text <ipynb_file> --output <output_file>
```

- `<ipynb_file>`: Path to the `.ipynb` file.
- `--output <output_file>`: Path to save the plain text output. If not provided, the output will be printed to the console.

Example:

```bash
notebookllm to_text my_notebook.ipynb --output my_notebook.txt
```

### `to_ipynb`

Converts a `.py` file to a `.ipynb` file.

Usage:

```bash
notebookllm to_ipynb <py_file> --output <output_file>
```

- `<py_file>`: Path to the `.py` file.
- `--output <output_file>`: Path to save the `.ipynb` output. If not provided, the output will be saved to `output.ipynb`.

Example:

```bash
notebookllm to_ipynb my_script.py --output my_notebook.ipynb
```

## API

```python
from notebookllm import Notebook

notebook = Notebook(filepath='notebook.ipynb')  # Load existing notebook or create a new one
notebook.add_code_cell('print("Hello, world!")') # Add a code cell
notebook.add_markdown_cell('# This is a markdown cell') # Add a markdown cell
notebook.execute_cell(0) # Execute a cell
notebook.delete_cell(1) # Delete a cell
notebook.add_raw_cell('{"data": {"text/plain": "This is a raw cell"}}') # Add a raw cell
notebook.save('new_notebook.ipynb') # Save the notebook
notebook.edit_cell(0, 'print("Hello, world!")') # Edit a cell
notebook.save() # Save the changes
````

## Using `notebookllm` as an MCP Server

The `notebookllm` package includes an MCP (Model Context Protocol) server (`mcp_server.py`) that exposes notebook conversion and manipulation functionalities as tools for Large Language Models (LLMs). This allows LLMs to programmatically interact with Jupyter notebooks in a way that is token-efficient, cost-effective, and fast by focusing on plain text representations of notebook content rather than full, verbose notebook metadata.

### Installation & Running the Server

Here’s how to install and run the `notebookllm` MCP server:

**1. Using `uvx` (Recommended for quick use)**

`uvx` allows you to run the server directly from its PyPI package without needing to install it into your global or project Python environment. This is ideal for quickly using the server with clients like Claude Desktop or VS Code.

*   To run the server (assuming `notebookllm` is published to PyPI and provides a `notebookllm-server` command):
    ```bash
    uvx notebookllm-server
    ```

**2. Using `pip` (Traditional installation)**

*   Install the package from PyPI:
    ```bash
    pip install notebookllm
    ```
*   Run the server using the installed command:
    ```bash
    notebookllm-server
    ```
    *(If the package installs `mcp_server.py` as a module within the `notebookllm` package but doesn't define a direct `notebookllm-server` script, you might run it as `python -m notebookllm.mcp_server`.)*

### Configuration with Clients

Once the server can be run using one of the methods above, you can configure various clients to use its tools.

**A. Claude Desktop**

Add the following to your `claude_desktop_config.json` file (typically found at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS, or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

*   **Using `uvx`:**
    ```json
    {
      "mcpServers": {
        "notebookllm": {
          "command": "uvx",
          "args": ["notebookllm-server"]
        }
      }
    }
    ```

*   **Using `pip` installation:**
    ```json
    {
      "mcpServers": {
        "notebookllm": {
          "command": "notebookllm-server", // Or full path if not in PATH, or 'python'
          "args": [] // If using 'python', args would be ['-m', 'notebookllm.mcp_server']
        }
      }
    }
    ```

**B. VS Code**

Add the following to your User Settings (JSON) file (`Ctrl + Shift + P` -> "Preferences: Open User Settings (JSON)") or to a `.vscode/mcp.json` file in your workspace (if using `.vscode/mcp.json`, omit the top-level `"mcp": { ... }` wrapper).

*   **Using `uvx`:**
    ```json
    {
      "mcp": {
        "servers": {
          "notebookllm": {
            "command": "uvx",
            "args": ["notebookllm-server"]
          }
        }
      }
    }
    ```

*   **Using `pip` installation:**
    ```json
    {
      "mcp": {
        "servers": {
          "notebookllm": {
            "command": "notebookllm-server", // Or 'python'
            "args": [] // If using 'python', args would be ['-m', 'notebookllm.mcp_server']
          }
        }
      }
    }
    ```

**C. Zed Editor**

Add the following to your Zed `settings.json` (accessible via `Zed > Settings > Open Settings (JSON)`):

*   **Using `uvx`:**
    ```json
    {
      "mcp_servers": {
        "notebookllm": {
          "command": "uvx",
          "args": ["notebookllm-server"]
        }
      }
    }
    ```

*   **Using `pip` installation:**
    ```json
    {
      "mcp_servers": {
        "notebookllm": {
          "command": "notebookllm-server", // Or 'python'
          "args": [] // If using 'python', args would be ['-m', 'notebookllm.mcp_server']
        }
      }
    }
    ```

### Available Tools

The MCP server exposes the following tools (refer to the `mcp_server.py` file within the `notebookllm` package for detailed descriptions and parameters):

*   `load_notebook(filepath: str)`: Loads a `.ipynb` file into memory for efficient operations.
*   `notebook_to_plain_text(input_filepath: str | None = None)`: Converts a notebook to token-efficient plain text.
*   `plain_text_to_notebook_file(plain_text_content: str, output_filepath: str)`: Converts plain text back to a `.ipynb` file.
*   `add_code_cell_to_loaded_notebook(code_content: str, position: int | None = None)`: Adds a code cell to the loaded notebook.
*   `add_markdown_cell_to_loaded_notebook(markdown_content: str, position: int | None = None)`: Adds a markdown cell to the loaded notebook.
*   `save_loaded_notebook(output_filepath: str | None = None)`: Saves the loaded notebook.

### Debugging the Server

You can use the MCP Inspector to debug the server.

*   **If using `uvx`:**
    ```bash
    npx @modelcontextprotocol/inspector uvx notebookllm-server
    ```

*   **If using a `pip` installed version (assuming `notebookllm-server` is the command):**
    ```bash
    npx @modelcontextprotocol/inspector notebookllm-server
    ```
    *(If running as a module: `npx @modelcontextprotocol/inspector python -m notebookllm.mcp_server`)*

Check the logs from your client application (e.g., Claude Desktop logs typically found in `~/Library/Logs/Claude/mcp*.log` on macOS or `%APPDATA%\Claude\mcp*.log` on Windows) for more detailed error messages from the server.

### Development & Local Testing

If you are developing `notebookllm` locally:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yasirrazaa/notebookllm.git # Or your fork
    cd notebookllm
    ```
2.  **Set up the environment using `uv`:**
    ```bash
    uv init  # If not already done for this project
    uv sync  # Installs dependencies from pyproject.toml, including mcp[cli]
    uv pip install -e . # Installs the notebookllm package in editable mode
    ```
3.  **Run the local server for testing:**
    *   Using `mcp dev` for the MCP Inspector (recommended for interactive testing):
        ```bash
        uv run mcp dev mcp_server.py
        ```
    *   Running the local `mcp_server.py` script directly:
        ```bash
        uv run python mcp_server.py
        ```
    *   If you've installed in editable mode and defined the `notebookllm-server` script in your `pyproject.toml`, you can also test it as if it were installed:
        ```bash
        uv run notebookllm-server
        ```

By providing these tools via MCP, `notebookllm` empowers LLMs to become more active participants in the notebook development and manipulation workflow, enhancing productivity and reducing manual effort by focusing on cost-effective, token-efficient operations.

