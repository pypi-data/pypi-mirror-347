#!/usr/bin/env python3
"""
Message type definitions for the autonomous threat modeling system.
"""

from enum import Enum


class MessageType(Enum):
    """Enum for message types"""

    # System messages
    SYSTEM_INIT = "system_init"
    SYSTEM_SHUTDOWN = "system_shutdown"
    SYSTEM_ERROR = "system_error"

    # Job control
    JOB_START = "job_start"
    JOB_COMPLETE = "job_complete"
    JOB_ERROR = "job_error"
    JOB_CANCEL = "job_cancel"

    # Input layer
    CODE_INGESTION_START = "code_ingestion_start"
    CODE_INGESTION_COMPLETE = "code_ingestion_complete"
    CODE_INGESTION_ERROR = "code_ingestion_error"

    # Code understanding layer
    CODE_NORMALIZATION_START = "code_normalization_start"
    CODE_NORMALIZATION_COMPLETE = "code_normalization_complete"
    LANGUAGE_IDENTIFICATION_START = "language_identification_start"
    LANGUAGE_IDENTIFICATION_COMPLETE = "language_identification_complete"
    CODE_GRAPH_GENERATION_START = "code_graph_start"
    CODE_GRAPH_GENERATION_COMPLETE = "code_graph_complete"
    DEPENDENCY_EXTRACTION_START = "dependency_extraction_start"
    DEPENDENCY_EXTRACTION_COMPLETE = "dependency_extraction_complete"

    # Commit history analysis
    COMMIT_HISTORY_ANALYSIS_START = "commit_history_analysis_start"
    COMMIT_HISTORY_ANALYSIS_COMPLETE = "commit_history_analysis_complete"
    COMMIT_HISTORY_ANALYSIS_ERROR = "commit_history_analysis_error"

    # RedFlag analysis
    REDFLAG_ANALYSIS_START = "redflag_analysis_start"
    REDFLAG_ANALYSIS_COMPLETE = "redflag_analysis_complete"
    REDFLAG_ANALYSIS_ERROR = "redflag_analysis_error"

    # CodeShield analysis
    CODE_ANALYSIS_START = "code_analysis_start"
    CODE_ANALYSIS_COMPLETE = "code_analysis_complete"
    CODE_ANALYSIS_ERROR = "code_analysis_error"

    # Contextual analysis layer
    CONTEXT_ANALYSIS_START = "context_analysis_start"
    CONTEXT_ANALYSIS_COMPLETE = "context_analysis_complete"

    # Scenario generation layer
    THREAT_SCENARIO_START = "threat_scenario_start"
    THREAT_SCENARIO_COMPLETE = "threat_scenario_complete"
    THREAT_SIMULATION_START = "threat_simulation_start"
    THREAT_SIMULATION_COMPLETE = "threat_simulation_complete"

    # Threat identification layer
    THREAT_DETECTION_START = "threat_detection_start"
    THREAT_DETECTION_COMPLETE = "threat_detection_complete"
    THREAT_VALIDATION_START = "threat_validation_start"
    THREAT_VALIDATION_COMPLETE = "threat_validation_complete"
    VULNERABILITY_LOOKUP_START = "vulnerability_lookup_start"
    VULNERABILITY_LOOKUP_COMPLETE = "vulnerability_lookup_complete"

    # Risk assessment layer
    RISK_SCORING_START = "risk_scoring_start"
    RISK_SCORING_COMPLETE = "risk_scoring_complete"
    PRIORITIZATION_START = "prioritization_start"
    PRIORITIZATION_COMPLETE = "prioritization_complete"

    # Threat model synthesis layer
    THREAT_MODEL_ASSEMBLY_START = "threat_model_assembly_start"
    THREAT_MODEL_ASSEMBLY_COMPLETE = "threat_model_assembly_complete"
    ASSEMBLE_THREAT_MODEL = "assemble_threat_model"
    THREAT_MODEL_COMPLETE = "threat_model_complete"

    # Direct A2A messages
    A2A_REQUEST = "a2a_request"
    A2A_RESPONSE = "a2a_response"
    A2A_ERROR = "a2a_error"
