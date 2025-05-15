"""Module for executing Jupyter notebooks using papermill."""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

import papermill as pm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def execute_notebook(
    input_path: str | Path,
    output_path: Optional[str | Path] = None,
    parameters: Optional[Dict[str, Any]] = None,
    kernel_name: Optional[str] = None,
    log_file: Optional[str | Path] = None,
) -> None:
    """
    Execute a Jupyter notebook using papermill.

    Args:
        input_path: Path to the input notebook
        output_path: Path where the executed notebook will be saved (defaults to input_path with _executed suffix)
        parameters: Dictionary of parameters to inject into the notebook
        kernel_name: Name of the kernel to use for execution
        log_file: Path to the log file (defaults to output_path.parent/cron.log)

    Raises:
        Exception: If notebook execution fails
    """
    try:
        # Convert paths to Path objects
        input_path = Path(input_path).resolve()
        if not input_path.exists():
            raise FileNotFoundError(f"Notebook not found: {input_path}")

        # Set default output path if not provided
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}_executed{input_path.suffix}"
        else:
            output_path = Path(output_path).resolve()

        # Configure logging to file if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(file_handler)

        logger.info(f"Executing notebook: {input_path}")
        pm.execute_notebook(
            input_path=str(input_path),
            output_path=str(output_path),
            parameters=parameters or {},
            kernel_name=kernel_name,
        )
        logger.info(f"Notebook execution completed. Output saved to: {output_path}")
    except Exception as e:
        logger.error(f"Failed to execute notebook: {str(e)}")
        raise 