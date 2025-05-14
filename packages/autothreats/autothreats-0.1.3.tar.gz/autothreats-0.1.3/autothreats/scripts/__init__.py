"""
Scripts package for the autonomous threat modeling system.
"""

# Import and expose script functions
from .generate_config import generate_default_config

# Import simplified components
from .simplified_analyze_large_codebase import analyze_large_codebase
from .simplified_analyze_large_codebase import main as run_analyze_large_codebase
from .test_config import validate_config
from .test_llm_service import test_llm_service

# For backward compatibility
try:
    from .threat_modeling_cli import main as run_threat_modeling_cli
except ImportError:
    # Create a dummy function for backward compatibility
    async def run_threat_modeling_cli(*args, **kwargs):
        import logging

        logging.warning(
            "threat_modeling_cli is not available in the simplified version"
        )
        return 0
