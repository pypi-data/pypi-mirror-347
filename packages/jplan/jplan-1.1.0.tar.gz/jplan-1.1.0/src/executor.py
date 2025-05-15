"""Module for executing Jupyter notebooks using papermill."""

import logging
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

import papermill as pm
import nbformat as nbf

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def resolve_paths_in_notebook(notebook_path: Path, working_dir: Path) -> Path:
    """
    Pre-process the notebook to resolve relative paths.
    
    Args:
        notebook_path: Path to the notebook file
        working_dir: Working directory for resolving relative paths
        
    Returns:
        Path to the temporary processed notebook
    """
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)
    
    # Process each cell
    for cell in nb.cells:
        if cell.cell_type == 'code':
            # Look for file operations in the code
            code = cell.source
            if any(op in code for op in ['open(', 'pd.read_', 'with open']):
                # Add working directory setup at the start of the cell
                setup_code = f"""
import os
from pathlib import Path
# Set working directory to notebook location
os.chdir(r"{working_dir}")
# Helper function to resolve paths
def resolve_path(path):
    if isinstance(path, str):
        return str(Path(path).resolve())
    return path
"""
                cell.source = setup_code + "\n" + cell.source

    # Create a temporary file for the processed notebook
    temp_dir = tempfile.gettempdir()
    temp_notebook = Path(temp_dir) / f"jplan_{notebook_path.stem}_processed{notebook_path.suffix}"
    
    # Write the modified notebook to the temporary file
    with open(temp_notebook, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    
    return temp_notebook

def execute_notebook(
    input_path: str | Path,
    output_path: Optional[str | Path] = None,
    parameters: Optional[Dict[str, Any]] = None,
    kernel_name: Optional[str] = None,
    log_file: Optional[str | Path] = None,
    working_dir: Optional[str | Path] = None,
) -> None:
    """
    Execute a Jupyter notebook using papermill.

    Args:
        input_path: Path to the input notebook
        output_path: Path where the executed notebook will be saved (defaults to input_path with _executed suffix)
        parameters: Dictionary of parameters to inject into the notebook
        kernel_name: Name of the kernel to use for execution
        log_file: Path to the log file (defaults to output_path.parent/cron.log)
        working_dir: Working directory for resolving relative paths (defaults to input_path.parent)

    Raises:
        Exception: If notebook execution fails
    """
    try:
        # Convert paths to Path objects
        input_path = Path(input_path).resolve()
        if not input_path.exists():
            raise FileNotFoundError(f"Notebook not found: {input_path}")

        # Set working directory
        if working_dir is None:
            working_dir = input_path.parent
        else:
            working_dir = Path(working_dir).resolve()

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

        # Pre-process notebook to handle relative paths
        temp_notebook = resolve_paths_in_notebook(input_path, working_dir)

        logger.info(f"Executing notebook: {input_path}")
        logger.info(f"Working directory: {working_dir}")
        
        try:
            pm.execute_notebook(
                input_path=str(temp_notebook),
                output_path=str(output_path),
                parameters=parameters or {},
                kernel_name=kernel_name,
            )
            logger.info(f"Notebook execution completed. Output saved to: {output_path}")
        finally:
            # Clean up temporary notebook
            if temp_notebook.exists():
                temp_notebook.unlink()
                
    except Exception as e:
        logger.error(f"Failed to execute notebook: {str(e)}")
        raise 