"""Module for managing cron jobs for notebook execution."""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

from .executor import execute_notebook

def create_cron_job(
    notebook_path: str | Path,
    schedule: str,
    output_dir: Optional[str | Path] = None,
    parameters: Optional[dict] = None,
    kernel_name: Optional[str] = None,
    log_file: Optional[str | Path] = None,
    working_dir: Optional[str | Path] = None,
) -> None:
    """
    Create a cron job to execute a Jupyter notebook at the specified schedule.

    Args:
        notebook_path: Path to the notebook to execute
        schedule: Cron schedule expression (e.g., "0 * * * *" for hourly)
        output_dir: Directory to save executed notebooks (defaults to same directory as input)
        parameters: Dictionary of parameters to pass to the notebook
        kernel_name: Name of the kernel to use for execution
        log_file: Path to the log file (defaults to output_dir/cron.log)
        working_dir: Working directory for resolving relative paths (defaults to notebook_path.parent)

    Raises:
        Exception: If cron job creation fails
    """
    # Convert all paths to absolute paths
    notebook_path = Path(notebook_path).resolve()
    if not notebook_path.exists():
        raise FileNotFoundError(f"Notebook not found: {notebook_path}")

    # Set working directory
    if working_dir is None:
        working_dir = notebook_path.parent
    else:
        working_dir = Path(working_dir).resolve()

    # Create output directory if specified
    if output_dir:
        output_dir = Path(output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{notebook_path.stem}_executed{notebook_path.suffix}"
    else:
        output_path = notebook_path.parent / f"{notebook_path.stem}_executed{notebook_path.suffix}"

    # Set default log file if not specified
    if log_file is None:
        log_file = output_path.parent / "cron.log"
    else:
        log_file = Path(log_file).resolve()

    # Get absolute path to Python executable
    python_path = Path(sys.executable).resolve()
    
    # Get absolute path to the package's executor module
    package_dir = Path(__file__).parent.resolve()
    
    # Create the Python command to execute with absolute paths
    python_cmd = (
        f"{python_path} -c 'import sys; sys.path.append(\"{package_dir.parent}\"); "
        f"from executor import execute_notebook; "
        f"execute_notebook(\"{notebook_path}\", \"{output_path}\", "
        f"{parameters or {}}, \"{kernel_name or ''}\", \"{log_file}\", \"{working_dir}\")'"
    )

    # Create the cron job command with absolute paths
    cron_cmd = f"{schedule} cd {working_dir} && {python_cmd}"

    try:
        # Get existing cron jobs
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True,
            check=True
        )
        existing_jobs = result.stdout

        # Add new cron job
        new_crontab = existing_jobs + cron_cmd + "\n"
        subprocess.run(
            ["crontab", "-"],
            input=new_crontab,
            text=True,
            check=True
        )
        print(f"Cron job created successfully. Schedule: {schedule}")
        print(f"Notebook will be executed and saved to: {output_path}")
        print(f"Working directory set to: {working_dir}")
        print(f"Logs will be written to: {log_file}")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to create cron job: {str(e)}") 