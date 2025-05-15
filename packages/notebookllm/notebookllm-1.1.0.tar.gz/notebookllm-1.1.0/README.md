# notebookllm : https://pypi.org/project/notebookllm


![PyPI](https://img.shields.io/pypi/v/notebookllm?label=pypi%20package)
![PyPI - Downloads](https://img.shields.io/pypi/dm/notebookllm)

A Python package to bridge the gap between Jupyter Notebooks and Large Language Models (LLMs). It reduces token usage,cost and makesit easy for llms to work with large notebooks by providing only the actual code omitting the cell metadata.

## Why this package?

Current Large Language Models (LLMs) struggles when working with `.ipynb` files. Working with raw `.ipynb` files with LLMs often leads to heavy token usage, increased costs, and challenges with context window limitations due to the verbose JSON structure and metadata. This package provides a solution by converting `.ipynb` files to a simplified plain text format that LLMs can easily understand, significantly reducing token count. It also allows converting Python files back to `.ipynb` files.

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
