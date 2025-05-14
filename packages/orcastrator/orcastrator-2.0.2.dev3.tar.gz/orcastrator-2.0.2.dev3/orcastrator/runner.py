"""
This module is deprecated and will be removed in a future version.
Use orcastrator.engine.OrcaEngine instead.
"""

import warnings
from pathlib import Path
from typing import Optional
import subprocess

from orcastrator.engine import OrcaEngine

warnings.warn(
    "The OrcaRunner class is deprecated. Use OrcaEngine instead.",
    DeprecationWarning, 
    stacklevel=2
)

class OrcaRunner:
    """Legacy OrcaRunner class for backwards compatibility.
    
    This class is deprecated. Use OrcaEngine instead.
    """
    
    def __init__(self, orca_executable: Optional[Path] = None) -> None:
        """Initialize with the new OrcaEngine."""
        # Forward to the new implementation
        self.engine = OrcaEngine(orca_executable=orca_executable)
        self.orca_executable = self.engine.orca_executable

    def run(self, input_file: Path, output_file: Path) -> subprocess.CompletedProcess:
        """Run an ORCA calculation."""
        # Forward to the new implementation
        return self.engine.execute(
            input_file=input_file,
            output_file=output_file
        )
