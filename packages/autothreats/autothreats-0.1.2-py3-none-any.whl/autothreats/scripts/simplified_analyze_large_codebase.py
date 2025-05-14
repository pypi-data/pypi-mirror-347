#!/usr/bin/env python3
"""
Script to analyze large codebases using hierarchical and context-aware analysis.
This script demonstrates how to use the enhanced capabilities for massive projects like Linux.
"""

import argparse
import asyncio
import logging
import os
import sys
from typing import Any, Dict

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from autothreats.agentic import (
    SimplifiedContextAwareSecurity,
    SimplifiedHierarchicalAnalysis,
)
from autothreats.simplified_orchestrator import SimplifiedOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


async def analyze_large_codebase(codebase_path: str, output_dir: str = None):
    """
    Analyze a large codebase using hierarchical and context-aware analysis.

    Args:
        codebase_path: Path to the codebase to analyze
        output_dir: Directory to store analysis results
    """
    logger.info(f"Starting analysis of large codebase: {codebase_path}")

    # Initialize the orchestrator
    config = {
        "output_dir": output_dir or "./output",
        "parallel_operations": 8,
        "enable_agentic": True,
        "enable_multi_stage": True,
        "llm": {
            "provider": "openai",  # or "anthropic"
            "fallback_providers": ["anthropic"],
        },
        "openai": {
            "api_key": os.environ.get("OPENAI_API_KEY"),
            "default_model": "gpt-4o-mini",
            "cache_enabled": True,
        },
        "anthropic": {
            "api_key": os.environ.get("ANTHROPIC_API_KEY"),
            "default_model": "claude-3-sonnet-20240229",
            "cache_enabled": True,
        },
        "agents": {
            "code_ingestion": {
                "max_files": 20000,  # Increased for large codebases
                "max_file_size": 100 * 1024,  # 100KB
            },
            "code_graph": {
                "enable_semantic_analysis": True,
            },
        },
    }

    orchestrator = SimplifiedOrchestrator(config)
    await orchestrator.initialize()

    try:
        # Create job data
        job_id = f"job_{os.path.basename(codebase_path)}_{int(asyncio.get_event_loop().time())}"
        job_data = {
            "job_id": job_id,
            "codebase_path": codebase_path,
            "output_dir": output_dir,
        }

        # Process the job
        logger.info(f"Starting job {job_id} for codebase {codebase_path}")
        result = await orchestrator.process_job(job_data)

        # Check if the job was successful
        if result["status"] == "success":
            logger.info(f"Job {job_id} completed successfully")

            # Get workspace
            workspace = orchestrator.workspace

            # Get codebase model
            codebase_id = f"codebase_{job_id}"
            codebase_model = workspace.get_data(codebase_id)

            if not codebase_model:
                logger.error(f"Codebase model not found for job {job_id}")
                return

            # Check if hierarchical analysis is recommended
            if workspace.get_data("recommend_hierarchical_analysis"):
                logger.info(
                    "Hierarchical analysis is recommended for this large codebase"
                )

                # Get or create hierarchical analysis component
                hierarchical_analysis = workspace.get_data("hierarchical_analysis")
                if not hierarchical_analysis:
                    logger.info("Creating hierarchical analysis component")
                    hierarchical_analysis = SimplifiedHierarchicalAnalysis(workspace)
                    workspace.store_data("hierarchical_analysis", hierarchical_analysis)

                # Perform hierarchical analysis
                logger.info("Starting hierarchical analysis")
                hierarchical_results = (
                    await hierarchical_analysis.analyze_large_codebase(
                        codebase_model, job_id
                    )
                )
                logger.info(
                    f"Hierarchical analysis complete: {len(hierarchical_results.get('subsystems_analyzed', []))} subsystems analyzed"
                )

                # Get or create context-aware analysis component
                context_aware_analysis = workspace.get_data("context_aware_security")
                if not context_aware_analysis:
                    logger.info("Creating context-aware analysis component")
                    context_aware_analysis = SimplifiedContextAwareSecurity(workspace)
                    workspace.store_data(
                        "context_aware_security", context_aware_analysis
                    )

                # Perform context-aware analysis
                logger.info("Starting context-aware analysis")
                context_model = await context_aware_analysis.analyze_security_context(
                    codebase_model, job_id
                )
                logger.info("Context-aware analysis complete")

                # Get vulnerabilities
                vulnerabilities = workspace.get_data(f"vulnerabilities_{job_id}")
                if vulnerabilities:
                    # Enhance vulnerabilities with context
                    enhanced_vulnerabilities = (
                        await context_aware_analysis.enhance_vulnerability_detection(
                            vulnerabilities, context_model
                        )
                    )
                    workspace.store_data(
                        f"enhanced_vulnerabilities_{job_id}", enhanced_vulnerabilities
                    )
                    logger.info("Vulnerabilities enhanced with context-aware analysis")

            # Generate reports
            output_dir = config["output_dir"]
            os.makedirs(output_dir, exist_ok=True)

            # Save vulnerabilities
            vulnerabilities = workspace.get_data(
                f"enhanced_vulnerabilities_{job_id}"
            ) or workspace.get_data(f"vulnerabilities_{job_id}")
            if vulnerabilities:
                import json

                with open(os.path.join(output_dir, "vulnerabilities.json"), "w") as f:
                    json.dump(vulnerabilities, f, indent=2)
                logger.info(
                    f"Saved {len(vulnerabilities)} vulnerabilities to {os.path.join(output_dir, 'vulnerabilities.json')}"
                )

            # Return the result
            return result
        else:
            logger.error(
                f"Job {job_id} failed: {result.get('message', 'Unknown error')}"
            )
            return None

    finally:
        # Clean up
        await orchestrator.shutdown()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Analyze large codebases using hierarchical and context-aware analysis"
    )
    parser.add_argument("codebase_path", help="Path to the codebase to analyze")
    parser.add_argument(
        "--output-dir", "-o", help="Directory to store analysis results"
    )
    args = parser.parse_args()

    asyncio.run(analyze_large_codebase(args.codebase_path, args.output_dir))


if __name__ == "__main__":
    main()
