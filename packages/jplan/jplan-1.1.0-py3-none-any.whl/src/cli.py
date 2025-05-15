"""Command-line interface for jplan."""

import argparse
import json
from pathlib import Path

from .cron import create_cron_job
from .executor import execute_notebook

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Schedule and execute Jupyter notebooks using cron"
    )
    parser.add_argument(
        "schedule",
        help="Cron schedule expression (e.g., '0 * * * *' for hourly)"
    )
    parser.add_argument(
        "notebook",
        help="Path to the Jupyter notebook to execute"
    )
    parser.add_argument(
        "log_file",
        nargs="?",
        help="Path to the log file (optional)"
    )
    parser.add_argument(
        "--output-dir",
        help="Directory to save executed notebooks (defaults to same directory as input)"
    )
    parser.add_argument(
        "--parameters",
        help="JSON string of parameters to pass to the notebook"
    )
    parser.add_argument(
        "--kernel",
        help="Name of the kernel to use for execution"
    )
    parser.add_argument(
        "--log-file",
        help="Path to the log file (alternative to positional argument)"
    )
    parser.add_argument(
        "--working-dir",
        help="Working directory for resolving relative paths (defaults to notebook directory)"
    )

    args = parser.parse_args()

    # Parse parameters if provided
    parameters = None
    if args.parameters:
        try:
            parameters = json.loads(args.parameters)
        except json.JSONDecodeError:
            parser.error("--parameters must be a valid JSON string")

    # Use log file from either positional or keyword argument
    log_file = args.log_file or args.log_file

    # Create cron job
    create_cron_job(
        notebook_path=args.notebook,
        schedule=args.schedule,
        output_dir=args.output_dir,
        parameters=parameters,
        kernel_name=args.kernel,
        log_file=log_file,
        working_dir=args.working_dir
    )

if __name__ == "__main__":
    main() 