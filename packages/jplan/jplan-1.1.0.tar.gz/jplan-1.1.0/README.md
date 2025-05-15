# jplan

A command-line tool to schedule and execute Jupyter notebooks using cron.

## Installation

This package uses `uv` for package management. To install:

```bash
# Install uv if you haven't already
pip install uv

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

## Usage

### Command Line Interface

The simplest way to use jplan is through the command line:

```bash
# Run notebook every hour with default log file in notebook's directory
jplan "0 * * * *" input.ipynb

# Run notebook every hour with specific log file (positional argument)
jplan "0 * * * *" input.ipynb output.log

# Run notebook every hour with specific log file (keyword argument)
jplan "0 * * * *" input.ipynb --log-file output.log

# Run notebook every hour with specific kernel
jplan "0 * * * *" input.ipynb --kernel python3

# Run notebook every 15 minutes
jplan "*/15 * * * *" input.ipynb

# Run notebook with custom output directory
jplan "0 * * * *" input.ipynb --output-dir /path/to/output

# Run notebook with parameters
jplan "0 * * * *" input.ipynb --parameters '{"param1": "value1", "param2": 42}'

# Run notebook with custom working directory for relative paths
jplan "0 * * * *" input.ipynb --working-dir /path/to/data
```

The command takes the following arguments:
- `schedule`: Cron schedule expression (e.g., "0 * * * *" for hourly)
- `notebook`: Path to the input notebook file
- `log_file`: (Optional) Path to the log file (can be specified as positional or --log-file argument)
- `--output-dir`: (Optional) Directory to save executed notebooks
- `--parameters`: (Optional) JSON string of parameters to pass to the notebook
- `--kernel`: (Optional) Name of the kernel to use for execution
- `--working-dir`: (Optional) Working directory for resolving relative paths (defaults to notebook directory)

### Relative Path Handling

jplan automatically handles relative paths in your notebooks. When a notebook is executed:

1. The working directory is set to the notebook's location by default
2. You can specify a custom working directory using `--working-dir`
3. All relative paths in the notebook are resolved relative to the working directory
4. The original notebook is never modified (changes are made in a temporary copy)

Example notebook code:
```python
import pandas as pd

# These will all work correctly
df1 = pd.read_csv('data.csv')  # Resolves to working_dir/data.csv
df2 = pd.read_csv('./data.csv')  # Resolves to working_dir/data.csv
df3 = pd.read_csv('../data.csv')  # Resolves to working_dir/../data.csv

# You can also use the resolve_path helper
from pathlib import Path
file_path = resolve_path('data.csv')  # Gets absolute path
```

### Python API

You can also use the package programmatically:

```python
from jplan.executor import execute_notebook

# Execute a notebook with default settings
execute_notebook(
    input_path="path/to/input.ipynb"
)

# Execute a notebook with custom settings
execute_notebook(
    input_path="path/to/input.ipynb",
    output_path="path/to/output.ipynb",  # optional
    parameters={"param1": "value1", "param2": 42},  # optional
    kernel_name="python3",  # optional
    log_file="path/to/output.log",  # optional
    working_dir="path/to/data"  # optional
)

# Create a cron job
from jplan.cron import create_cron_job

create_cron_job(
    notebook_path="path/to/input.ipynb",
    schedule="0 * * * *",  # Run at the start of every hour
    output_dir="path/to/output",  # optional
    parameters={"param1": "value1"},  # optional
    kernel_name="python3",  # optional
    log_file="path/to/output.log",  # optional
    working_dir="path/to/data"  # optional
)
```

The schedule parameter uses standard cron syntax:
- `* * * * *` represents: minute hour day-of-month month day-of-week
- Examples:
  - `0 * * * *` - Run at the start of every hour
  - `0 0 * * *` - Run at midnight every day
  - `*/15 * * * *` - Run every 15 minutes

The executed notebooks will be saved with "_executed" appended to the filename, and a log file will be created in the output directory.

## Development

To install development dependencies:

```bash
uv pip install -e ".[dev]"
```

## License

MIT 