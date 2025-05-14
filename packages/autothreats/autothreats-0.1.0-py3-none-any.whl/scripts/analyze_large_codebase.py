#!/usr/bin/env python3
"""
Script to analyze large codebases using hierarchical and context-aware analysis.
This script demonstrates how to use the enhanced capabilities for massive projects like Linux.

This is a compatibility wrapper that redirects to the simplified version.
"""

import importlib.util
import logging
import os
import sys

# Check if the simplified version exists
simplified_path = os.path.join(os.path.dirname(__file__), "simplified_analyze_large_codebase.py")
if os.path.exists(simplified_path):
    # Import the simplified version
    spec = importlib.util.spec_from_file_location("simplified_analyze_large_codebase", simplified_path)
    simplified = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(simplified)
    
    # Re-export the functions from the simplified version
    analyze_large_codebase = simplified.analyze_large_codebase
    main = simplified.main
else:
    # Fallback implementation if the simplified version doesn't exist
    import asyncio
    from typing import Any, Dict
    
    async def analyze_large_codebase(codebase_path: str, output_dir: str = None):
        """
        Analyze a large codebase using hierarchical and context-aware analysis.
        
        Args:
            codebase_path: Path to the codebase to analyze
            output_dir: Directory to store analysis results
        """
        logging.warning("Using fallback implementation of analyze_large_codebase")
        logging.warning("Please create the simplified_analyze_large_codebase.py file")
        
        # Create a minimal result
        return {
            "status": "error",
            "message": "Simplified implementation not found",
            "codebase_path": codebase_path,
            "output_dir": output_dir or "./output",
        }
    
    def main():
        """Main entry point"""
        import argparse
        
        parser = argparse.ArgumentParser(
            description="Analyze large codebases using hierarchical and context-aware analysis"
        )
        parser.add_argument("codebase_path", help="Path to the codebase to analyze")
        parser.add_argument(
            "--output-dir", "-o", help="Directory to store analysis results"
        )
        args = parser.parse_args()
        
        asyncio.run(analyze_large_codebase(args.codebase_path, args.output_dir))

# If this script is run directly, call the main function
if __name__ == "__main__":
    main()
