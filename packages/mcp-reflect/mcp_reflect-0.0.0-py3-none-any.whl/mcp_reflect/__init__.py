"""
MCP-Reflect: A tool for model self-reflection and response improvement.

This package provides MCP tools for evaluating and improving model responses.
"""

__version__ = "0.1.0"

from mcp_reflect.models import EvaluationDimension, ReflectionResult
from mcp_reflect.server import mcp, reflect, sequential_reflect, run_server

__all__ = [
    "mcp",
    "reflect",
    "sequential_reflect",
    "run_server",
    "EvaluationDimension",
    "ReflectionResult",
]
