#!/usr/bin/env python3
"""
Enhanced logging configuration for the autonomous threat modeling system.
"""

import logging
import sys
import threading
import time


class HeartbeatLogger(threading.Thread):
    """
    A thread that periodically logs a heartbeat message to show the system is still running.
    """
    
    def __init__(self, interval=60, logger_name="heartbeat"):
        """
        Initialize the heartbeat logger.
        
        Args:
            interval (int): Interval in seconds between heartbeat messages
            logger_name (str): Name of the logger to use
        """
        super().__init__(daemon=True)  # Daemon thread will exit when main thread exits
        self.interval = interval
        self.logger = logging.getLogger(logger_name)
        self.running = False
        self.start_time = time.time()
        
    def run(self):
        """Run the heartbeat logger thread."""
        self.running = True
        counter = 0
        
        while self.running:
            counter += 1
            elapsed = int(time.time() - self.start_time)
            hours, remainder = divmod(elapsed, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            self.logger.info(
                f"HEARTBEAT #{counter}: System running for {hours:02d}:{minutes:02d}:{seconds:02d}"
            )
            
            # Sleep in small increments to allow for clean shutdown
            for _ in range(self.interval):
                if not self.running:
                    break
                time.sleep(1)
                
    def stop(self):
        """Stop the heartbeat logger thread."""
        self.running = False


# Global heartbeat logger instance
_heartbeat_logger = None


def configure_logging(log_level=logging.DEBUG, verbose=False, log_file=None, heartbeat_interval=60):
    """
    Configure logging with detailed formatting and output to both console and file.

    Args:
        log_level (int): Logging level, defaults to DEBUG
        verbose (bool): If True, sets log_level to DEBUG
        log_file (str): Path to log file, defaults to threat_canvas_debug.log
        heartbeat_interval (int): Interval in seconds between heartbeat messages, 0 to disable
    """
    global _heartbeat_logger
    
    # If verbose is True, override log_level to DEBUG
    if verbose:
        log_level = logging.DEBUG

    # Use default log file if not specified
    if log_file is None:
        log_file = "threat_canvas_debug.log"

    # Configure the root logger
    handlers = [
        # Console handler
        logging.StreamHandler(sys.stdout),
        # File handler for comprehensive logging
        logging.FileHandler(log_file, mode="w"),
    ]

    # Configure the root logger with a more detailed format
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )
    
    # Create a more detailed formatter for agent logs
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - [%(threadName)s] - %(message)s"
    )
    
    # Apply the detailed formatter to the handlers
    for handler in handlers:
        handler.setFormatter(detailed_formatter)
        
    # Start heartbeat logger if interval > 0
    if heartbeat_interval > 0:
        # Stop existing heartbeat logger if running
        if _heartbeat_logger is not None and _heartbeat_logger.running:
            _heartbeat_logger.stop()
            
        # Create and start new heartbeat logger
        _heartbeat_logger = HeartbeatLogger(interval=heartbeat_interval)
        _heartbeat_logger.start()
        logging.getLogger("heartbeat").info(f"Heartbeat logger started with {heartbeat_interval}s interval")

    # Set specific loggers to DEBUG to capture detailed information
    loggers_to_debug = [
        # Agent modules
        "autothreats.agents",
        "autothreats.agents.code_ingestion",
        "autothreats.agents.orchestrator",
        "autothreats.agents.agentic_threat_detection",
        "autothreats.agents.threat_detection",
        "autothreats.agents.threat_model_assembler",
        "autothreats.agents.agentic_threat_model_assembler",
        "autothreats.agents.normalization",
        "autothreats.agents.code_graph",
        # "autothreats.agents.agentic_code_graph", # Removed
        "autothreats.agents.dependency",
        "autothreats.agents.language_id",
        "autothreats.agents.prioritization",
        "autothreats.agents.agentic_prioritization",
        "autothreats.agents.risk_scoring",
        "autothreats.agents.threat_scenario",
        "autothreats.agents.threat_validation",
        "autothreats.agents.threat_simulation",
        "autothreats.agents.commit_history",
        "autothreats.agents.context",
        "autothreats.agents.codeshield",
        "autothreats.agents.redflag",
        
        # Agentic modules
        "autothreats.agentic",
        "autothreats.agentic.base_agent",
        "autothreats.agentic.agent_integration",
        "autothreats.agentic.agent_monitor",
        "autothreats.agentic.agent_extension",
        "autothreats.agentic.continuous_learning",
        "autothreats.agentic.knowledge_sharing",
        "autothreats.agentic.multi_agent_planning",
        "autothreats.agentic.context_aware_analysis",
        "autothreats.agentic.context_aware_security",
        "autothreats.agentic.hierarchical_analysis",
        "autothreats.agentic.adaptive_prioritization",
        "autothreats.agentic.causal_reasoning",
        "autothreats.agentic.collaborative_reasoning",
        "autothreats.agentic.explainable_security",
        
        # Core modules
        "autothreats.base",
        "autothreats.workspace",
        "autothreats.system",
    ]

    for logger_name in loggers_to_debug:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

    # Reduce noise from external libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)


# Call this function to set up logging when the module is imported
configure_logging()
