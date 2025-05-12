"""MCP-Reflect: A tool for model self-reflection and response improvement.

This package provides MCP tools for evaluating and improving model responses,
as well as structured meta-reflection capabilities.
"""

from mcp_reflect.models import (
    EvaluationDimension,
    Reflection,
    ReflectionResult,
    RType,
    Stage,
)
from mcp_reflect.server import (
    ReflectionStore,
    mcp,
    meta_reflect,
    meta_reflect_reset,
    meta_reflect_summary,
    reflect,
    reflection_store,
    run_server,
    sequential_reflect,
)

__all__ = [
    "mcp",
    "reflect",
    "sequential_reflect",
    "run_server",
    "EvaluationDimension",
    "ReflectionResult",
    # Meta-reflection functionality
    "Stage",
    "RType",
    "Reflection",
    "meta_reflect",
    "meta_reflect_summary",
    "meta_reflect_reset",
    "ReflectionStore",
    "reflection_store",
]
