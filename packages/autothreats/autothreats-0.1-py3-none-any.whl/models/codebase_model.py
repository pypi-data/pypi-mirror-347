#!/usr/bin/env python3
"""
Codebase model for the autonomous threat modeling system.
"""

import uuid
from typing import Any, Dict, Mapping, Optional


class CodebaseModel:
    """Model for codebase data"""

    def __init__(self, codebase_id: str):
        self.id = codebase_id
        self.files: Mapping[str, str] = {}  # path -> content
        self.metadata: Mapping[str, Any] = {}
        self.normalized_representation: Mapping[str, Any] = {}
        self.languages: Mapping[str, str] = {}  # path -> language
        self.dependencies: Mapping[str, str] = {}  # dependency -> version
        self.file_stats: Mapping[str, Mapping[str, int]] = (
            {}
        )  # Statistics about files (size, complexity, etc.)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CodebaseModel":
        """Create a CodebaseModel from a dictionary representation"""
        # Validate input
        if not isinstance(data, dict):
            raise ValueError("Input must be a dictionary")

        # Extract codebase_id, defaulting to a generated UUID if not provided
        codebase_id = data.get("id", str(uuid.uuid4()))

        # Create the CodebaseModel instance
        codebase_model = cls(codebase_id)

        # Populate files
        files = data.get("files", {})
        for path, content in files.items():
            codebase_model.add_file(path, content)

        # Populate languages
        languages = data.get("languages", {})
        for path, language in languages.items():
            codebase_model.set_language(path, language)

        # Populate dependencies
        dependencies = data.get("dependencies", {})
        for dep, version in dependencies.items():
            codebase_model.add_dependency(dep, version)

        # Populate metadata
        codebase_model.metadata = data.get("metadata", {})

        return codebase_model

    def to_dict(self) -> Dict[str, Any]:
        """Convert the CodebaseModel to a dictionary representation"""
        return {
            "id": self.id,
            "files": self.files,
            "languages": self.languages,
            "dependencies": self.dependencies,
            "metadata": self.metadata,
            "file_stats": self.file_stats,
            "normalized_representation": self.normalized_representation,
        }

    def add_file(self, path: str, content: str):
        """Add a file to the codebase"""
        self.files[path] = content
        # Calculate basic stats
        self.file_stats[path] = {"size": len(content), "lines": content.count("\n") + 1}

    def set_language(self, path: str, language: str):
        """Set the language for a file"""
        self.languages[path] = language

    def add_dependency(self, dependency: str, version: str):
        """Add a dependency"""
        self.dependencies[dependency] = version

    def get_file_content(self, path: str) -> Optional[str]:
        """Get file content if it exists"""
        return self.files.get(path)

    def get_files_by_extension(self, extension: str) -> Mapping[str, str]:
        """Get all files with a specific extension"""
        return {
            path: content
            for path, content in self.files.items()
            if path.endswith(extension)
        }
