"""Type stubs for fastapi module."""

from typing import Any, Callable, Dict, List, Optional, Type, Union

class FastAPI:
    """FastAPI application."""

    def __init__(self, title: str = "", description: str = "", version: str = "0.1.0"):
        """Initialize the FastAPI application."""
        pass

    def get(self, path: str, **kwargs: Any) -> Callable:
        """Register a GET route."""
        pass

    def post(self, path: str, **kwargs: Any) -> Callable:
        """Register a POST route."""
        pass

    def put(self, path: str, **kwargs: Any) -> Callable:
        """Register a PUT route."""
        pass

    def delete(self, path: str, **kwargs: Any) -> Callable:
        """Register a DELETE route."""
        pass

class HTTPException(Exception):
    """HTTP exception."""

    def __init__(self, status_code: int, detail: str = ""):
        """Initialize the HTTP exception."""
        pass

class Depends:
    """Dependency injection."""

    def __init__(self, dependency: Callable):
        """Initialize the dependency."""
        pass
