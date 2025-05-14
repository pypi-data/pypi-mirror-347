#!/usr/bin/env python3
"""
Feedback-Driven Agent Learning System for the autonomous threat modeling system.
Enables agents to learn from feedback and improve over time.
"""

import json
import logging
import os
import time
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


class AgentLearningSystem:
    """
    Enables agents to learn from feedback and improve over time.
    Collects performance metrics, analyzes trends, and suggests improvements.
    """

    def __init__(self, workspace):
        """
        Initialize the agent learning system.

        Args:
            workspace: The shared workspace instance
        """
        self.workspace = workspace
        self.performance_metrics = {}
        self.learning_models = {}
        self.feedback_history = {}
        self.improvement_suggestions = {}
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

        # Define task types and their metrics
        self.task_types = {
            "code_analysis": ["accuracy", "coverage", "processing_time"],
            "threat_detection": [
                "precision",
                "recall",
                "false_positives",
                "processing_time",
            ],
            "risk_scoring": ["accuracy", "consistency", "processing_time"],
            "threat_modeling": ["completeness", "relevance", "processing_time"],
            "dependency_analysis": ["accuracy", "coverage", "processing_time"],
            "context_analysis": ["relevance", "completeness", "processing_time"],
        }

        # Load existing metrics if available
        self._load_metrics()

    def _load_metrics(self):
        """Load existing metrics from workspace storage"""
        metrics_data = self.workspace.get_data("agent_performance_metrics")
        if metrics_data:
            self.performance_metrics = metrics_data
            self.logger.info(
                f"Loaded performance metrics for {len(self.performance_metrics)} agents"
            )

        feedback_data = self.workspace.get_data("agent_feedback_history")
        if feedback_data:
            self.feedback_history = feedback_data
            self.logger.info(
                f"Loaded feedback history for {len(self.feedback_history)} agents"
            )

        suggestions_data = self.workspace.get_data("agent_improvement_suggestions")
        if suggestions_data:
            self.improvement_suggestions = suggestions_data
            self.logger.info(
                f"Loaded improvement suggestions for {len(self.improvement_suggestions)} agents"
            )

    def _save_metrics(self):
        """Save metrics to workspace storage"""
        self.workspace.store_data("agent_performance_metrics", self.performance_metrics)
        self.workspace.store_data("agent_feedback_history", self.feedback_history)
        self.workspace.store_data(
            "agent_improvement_suggestions", self.improvement_suggestions
        )

    def record_performance(
        self, agent_id: str, task_type: str, metrics: Dict[str, Any]
    ):
        """
        Record performance metrics for an agent on a specific task.

        Args:
            agent_id: The ID of the agent
            task_type: The type of task performed
            metrics: The performance metrics
        """
        if agent_id not in self.performance_metrics:
            self.performance_metrics[agent_id] = {}

        if task_type not in self.performance_metrics[agent_id]:
            self.performance_metrics[agent_id][task_type] = []

        # Add timestamp and job_id if not present
        metrics["timestamp"] = time.time()
        if "job_id" not in metrics:
            metrics["job_id"] = metrics.get("job_id", "unknown")

        self.performance_metrics[agent_id][task_type].append(metrics)

        # Limit history to last 100 entries per task type
        if len(self.performance_metrics[agent_id][task_type]) > 100:
            self.performance_metrics[agent_id][task_type] = self.performance_metrics[
                agent_id
            ][task_type][-100:]

        self.logger.debug(f"Recorded {task_type} performance for agent {agent_id}")

        # Save metrics
        self._save_metrics()

        # Analyze performance and generate suggestions if needed
        if (
            len(self.performance_metrics[agent_id][task_type]) >= 5
        ):  # Need at least 5 data points
            self.analyze_performance(agent_id, task_type)

    def record_feedback(
        self,
        agent_id: str,
        feedback_type: str,
        feedback_data: Dict[str, Any],
        source_id: Optional[str] = None,
    ):
        """
        Record feedback for an agent.

        Args:
            agent_id: The ID of the agent receiving feedback
            feedback_type: The type of feedback (e.g., "accuracy", "usefulness")
            feedback_data: The feedback data
            source_id: Optional ID of the feedback source (e.g., another agent)
        """
        if agent_id not in self.feedback_history:
            self.feedback_history[agent_id] = []

        feedback_entry = {
            "id": str(uuid.uuid4()),
            "type": feedback_type,
            "data": feedback_data,
            "source": source_id or "system",
            "timestamp": time.time(),
        }

        self.feedback_history[agent_id].append(feedback_entry)

        # Limit history to last 100 entries
        if len(self.feedback_history[agent_id]) > 100:
            self.feedback_history[agent_id] = self.feedback_history[agent_id][-100:]

        self.logger.info(
            f"Recorded {feedback_type} feedback for agent {agent_id} from {source_id or 'system'}"
        )

        # Save metrics
        self._save_metrics()

    def analyze_performance(self, agent_id: str, task_type: str) -> Dict[str, Any]:
        """
        Analyze agent performance trends for a specific task type.

        Args:
            agent_id: The ID of the agent
            task_type: The type of task to analyze

        Returns:
            Analysis results
        """
        if (
            agent_id not in self.performance_metrics
            or task_type not in self.performance_metrics[agent_id]
        ):
            return {"trend": "insufficient_data"}

        metrics = self.performance_metrics[agent_id][task_type]

        # Need at least 2 data points for trend analysis
        if len(metrics) < 2:
            return {"trend": "insufficient_data"}

        # Get expected metrics for this task type
        expected_metrics = self.task_types.get(task_type, ["processing_time"])

        # Calculate trends for each metric
        trends = {}
        for metric_name in expected_metrics:
            if all(metric_name in m for m in metrics):
                values = [m[metric_name] for m in metrics if metric_name in m]

                if not values or not all(isinstance(v, (int, float)) for v in values):
                    trends[metric_name] = {"trend": "not_numeric"}
                    continue

                avg_value = sum(values) / len(values)

                # Calculate trend as percentage change from first to last
                if values[0] != 0:
                    trend_pct = (values[-1] - values[0]) / abs(values[0]) * 100
                else:
                    trend_pct = 0

                # Determine if trend is improving or worsening
                # For processing_time, lower is better; for others, higher is better
                is_improving = (metric_name == "processing_time" and trend_pct < 0) or (
                    metric_name != "processing_time" and trend_pct > 0
                )

                trends[metric_name] = {
                    "average": avg_value,
                    "trend_pct": trend_pct,
                    "is_improving": is_improving,
                    "samples": len(values),
                    "first_value": values[0],
                    "last_value": values[-1],
                }

        # Overall assessment
        improving_metrics = sum(
            1 for t in trends.values() if t.get("is_improving", False)
        )
        worsening_metrics = sum(
            1 for t in trends.values() if not t.get("is_improving", True)
        )

        overall_status = "stable"
        if improving_metrics > worsening_metrics:
            overall_status = "improving"
        elif worsening_metrics > improving_metrics:
            overall_status = "worsening"

        analysis = {
            "agent_id": agent_id,
            "task_type": task_type,
            "metrics_analyzed": len(trends),
            "overall_status": overall_status,
            "trends": trends,
            "timestamp": time.time(),
        }

        # Generate improvement suggestions if performance is worsening
        if overall_status == "worsening":
            self._generate_improvement_suggestions(agent_id, task_type, analysis)

        return analysis

    def _generate_improvement_suggestions(
        self, agent_id: str, task_type: str, analysis: Dict[str, Any]
    ):
        """
        Generate improvement suggestions based on performance analysis.

        Args:
            agent_id: The ID of the agent
            task_type: The type of task
            analysis: The performance analysis
        """
        if agent_id not in self.improvement_suggestions:
            self.improvement_suggestions[agent_id] = {}

        suggestions = []

        # Generate suggestions for each worsening metric
        for metric_name, trend in analysis["trends"].items():
            if not trend.get("is_improving", True):
                suggestion = self._get_suggestion_for_metric(
                    task_type, metric_name, trend
                )
                if suggestion:
                    suggestions.append(suggestion)

        if suggestions:
            self.improvement_suggestions[agent_id][task_type] = {
                "suggestions": suggestions,
                "generated_at": time.time(),
                "applied": False,
            }

            self.logger.info(
                f"Generated {len(suggestions)} improvement suggestions for agent {agent_id} on {task_type}"
            )

            # Save metrics
            self._save_metrics()

    def _get_suggestion_for_metric(
        self, task_type: str, metric_name: str, trend: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Get a specific improvement suggestion for a metric.

        Args:
            task_type: The type of task
            metric_name: The name of the metric
            trend: The trend data for the metric

        Returns:
            Suggestion data or None
        """
        # Define suggestions based on task type and metric
        suggestions = {
            "processing_time": {
                "title": "Optimize processing time",
                "description": f"Processing time has increased by {abs(trend['trend_pct']):.1f}%. Consider optimizing algorithms or reducing unnecessary operations.",
                "implementation_hints": [
                    "Use caching for repeated operations",
                    "Optimize data structures for faster access",
                    "Consider parallel processing for independent tasks",
                ],
            },
            "accuracy": {
                "title": "Improve accuracy",
                "description": f"Accuracy has decreased by {abs(trend['trend_pct']):.1f}%. Consider refining analysis algorithms or improving data quality.",
                "implementation_hints": [
                    "Validate input data more thoroughly",
                    "Refine pattern matching or detection rules",
                    "Consider ensemble approaches for critical decisions",
                ],
            },
            "precision": {
                "title": "Enhance precision",
                "description": f"Precision has decreased by {abs(trend['trend_pct']):.1f}%. Focus on reducing false positives.",
                "implementation_hints": [
                    "Increase confidence thresholds for detection",
                    "Add additional validation steps for potential findings",
                    "Refine pattern matching to be more specific",
                ],
            },
            "recall": {
                "title": "Improve recall",
                "description": f"Recall has decreased by {abs(trend['trend_pct']):.1f}%. Focus on reducing false negatives.",
                "implementation_hints": [
                    "Lower confidence thresholds for detection",
                    "Expand pattern matching to catch more variants",
                    "Add additional detection methods for edge cases",
                ],
            },
            "coverage": {
                "title": "Increase coverage",
                "description": f"Coverage has decreased by {abs(trend['trend_pct']):.1f}%. Ensure comprehensive analysis of all relevant components.",
                "implementation_hints": [
                    "Expand file selection criteria",
                    "Add support for additional file types or languages",
                    "Ensure all code paths are analyzed",
                ],
            },
        }

        if metric_name in suggestions:
            suggestion = suggestions[metric_name].copy()
            suggestion["metric"] = metric_name
            suggestion["trend_pct"] = trend["trend_pct"]
            suggestion["task_type"] = task_type
            return suggestion

        return None

    def get_performance_history(
        self, agent_id: str, task_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get performance history for an agent.

        Args:
            agent_id: The ID of the agent
            task_type: Optional task type to filter by

        Returns:
            Performance history data
        """
        if agent_id not in self.performance_metrics:
            return {"agent_id": agent_id, "history": {}}

        if task_type:
            history = {task_type: self.performance_metrics[agent_id].get(task_type, [])}
        else:
            history = self.performance_metrics[agent_id]

        return {"agent_id": agent_id, "history": history}

    def get_feedback_history(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Get feedback history for an agent.

        Args:
            agent_id: The ID of the agent

        Returns:
            List of feedback entries
        """
        return self.feedback_history.get(agent_id, [])

    def get_improvement_suggestions(
        self, agent_id: str, task_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get improvement suggestions for an agent.

        Args:
            agent_id: The ID of the agent
            task_type: Optional task type to filter by

        Returns:
            List of improvement suggestions
        """
        if agent_id not in self.improvement_suggestions:
            return []

        suggestions = []

        if task_type:
            if task_type in self.improvement_suggestions[agent_id]:
                suggestions.extend(
                    self.improvement_suggestions[agent_id][task_type].get(
                        "suggestions", []
                    )
                )
        else:
            for task_data in self.improvement_suggestions[agent_id].values():
                suggestions.extend(task_data.get("suggestions", []))

        return suggestions

    def mark_suggestions_applied(self, agent_id: str, task_type: str):
        """
        Mark improvement suggestions as applied.

        Args:
            agent_id: The ID of the agent
            task_type: The task type
        """
        if (
            agent_id in self.improvement_suggestions
            and task_type in self.improvement_suggestions[agent_id]
        ):
            self.improvement_suggestions[agent_id][task_type]["applied"] = True
            self.improvement_suggestions[agent_id][task_type][
                "applied_at"
            ] = time.time()

            self.logger.info(
                f"Marked improvement suggestions as applied for agent {agent_id} on {task_type}"
            )

            # Save metrics
            self._save_metrics()
