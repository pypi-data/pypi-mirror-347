"""MCP server implementation for the mcp-reflect tool.

This module provides the FastMCP server and tool definitions for model
self-reflection capabilities and meta-reflection processes.
"""

# Package version
__version__ = "0.1.0"

__all__ = [
    "mcp",
    "reflect",
    "sequential_reflect",
    "meta_reflect",
    "meta_reflect_summary",
    "meta_reflect_reset",
    "run_server",
    "run_uvx_server",
    "ReflectionStore",
    "reflection_store",
]

from collections.abc import Sequence
from typing import Annotated, Any, Literal

from fastmcp import Context, FastMCP
from pydantic import Field

from mcp_reflect.evaluator import evaluate_response
from mcp_reflect.models import (
    EvaluationDimension,
    Reflection,
    ReflectionInput,
    ReflectionResult,
    RType,
    Stage,
)


class ReflectionStore:
    """Store and manage structured reflections."""

    def __init__(self, name: str) -> None:
        """Initialize a new reflection store.

        Args:
            name: A name for this reflection store

        """
        self.name = name
        self.store: list[Reflection] = []
        self._seq_counter = 0

    def add_reflection(
        self,
        content: str,
        stage: str,
        rtype: str,
        follows_from: list[int] | None = None,
    ) -> dict[str, Any]:
        """Add a new reflection to the store.

        Args:
            content: The content of the reflection
            stage: The stage of reflection (problem, analysis, etc.)
            rtype: The type of reflection (critical, creative, etc.)
            follows_from: Optional sequence IDs this reflection follows

        Returns:
            Dict with operation status and reflection ID

        """
        if follows_from is None:
            follows_from = []

        self._seq_counter += 1
        r = Reflection(
            content=content,
            seq=self._seq_counter,
            stage=Stage(stage),
            rtype=RType(rtype),
            follows_from=follows_from,
        )
        self.store.append(r)
        return {"ok": True, "id": r.id, "count": len(self.store)}

    def get_summary(self) -> list[dict[str, Any]]:
        """Get a summary of all reflections in the store.

        Returns:
            List of all reflections as dictionaries

        """
        return [r.model_dump() for r in sorted(self.store, key=lambda x: x.seq)]

    def reset(self) -> dict[str, Any]:
        """Reset the reflection store.

        Returns:
            Dict with operation status

        """
        self.store.clear()
        self._seq_counter = 0
        return {"ok": True, "msg": "Reflection store reset"}


# Create the MCP server
mcp: FastMCP = FastMCP(
    "Model Self-Reflection Tools",
    description="Tools for improving model self-reflection capabilities",
    dependencies=["fastmcp", "pydantic>=2.0.0", "async-lru"],
)

# Create reflection store instance
reflection_store = ReflectionStore("MetaReflect")


@mcp.tool()
async def reflect(
    response: Annotated[
        str,
        Field(..., description="The original model response to reflect upon and improve"),
    ],
    query: Annotated[
        str | None,
        Field(None, description="The original query that prompted the response"),
    ] = None,
    focus_dimensions: Annotated[
        list[EvaluationDimension] | None,
        Field(None, description="Specific dimensions to focus on during evaluation"),
    ] = None,
    improvement_prompt: Annotated[
        str | None,
        Field(
            None,
            description="Additional context or specific instructions for improvement",
        ),
    ] = None,
) -> ReflectionResult:
    """Reflect on and improve a model's response with structured evaluation.

    This tool analyzes the provided response against multiple quality dimensions,
    generates an improved version, and provides detailed feedback with specific
    suggestions for improvement.

    Returns
    -------
        A reflection result containing the improved response and detailed evaluation.

    """
    input_data = ReflectionInput(
        response=response,
        query=query,
        focus_dimensions=focus_dimensions or [],
        improvement_prompt=improvement_prompt,
    )

    return await evaluate_response(input_data)


@mcp.tool()
async def sequential_reflect(
    responses: Annotated[
        Sequence[str],
        Field(..., description="A sequence of model responses to analyze", min_length=1),
    ],
    mode: Annotated[
        Literal["independent", "iterative", "comparative"],
        Field(description="How to process multiple responses"),
    ] = "independent",
    context: Annotated[Context | None, Field(default=None)] = None,
) -> Sequence[ReflectionResult]:
    """Process multiple responses sequentially with different reflection strategies.

    Modes:
    - independent: Each response is analyzed separately
    - iterative: Each reflection builds upon previous improvements
    - comparative: Responses are evaluated against each other

    Returns
    -------
        A list of reflection results for each input response.

    """
    results = []

    if mode == "independent":
        # Process each response independently
        for response in responses:
            input_data = ReflectionInput(response=response)
            result = await evaluate_response(input_data)
            results.append(result)

    elif mode == "iterative":
        # Each reflection builds on previous improvements
        current = responses[0]
        for i, _ in enumerate(responses):
            input_data = ReflectionInput(
                response=current,
                improvement_prompt=f"Iteration {i + 1}/{len(responses)}",
            )
            result = await evaluate_response(input_data)
            results.append(result)
            current = result.improved_response

    elif mode == "comparative":
        # Compare responses against each other
        for i, response in enumerate(responses):
            [r for j, r in enumerate(responses) if j != i]
            input_data = ReflectionInput(
                response=response,
                improvement_prompt="Compare with other responses for improvement",
            )
            result = await evaluate_response(input_data)
            results.append(result)

    return results


@mcp.tool()
def meta_reflect(
    content: Annotated[str, Field(..., description="Content of the reflection")],
    stage: Annotated[
        str,
        Field(
            ...,
            description="Stage of reflection (problem, analysis, exploration, synthesis, conclusion)",
        ),
    ],
    rtype: Annotated[
        str,
        Field(
            ...,
            description="Type of reflection (critical, creative, analytical, integrative, meta)",
        ),
    ],
    follows_from: (
        Annotated[list[int], Field(default_factory=list, description="Sequence IDs this reflection follows")] | None
    ) = None,
) -> dict[str, Any]:
    """🌠 Capture a structured reflection for meta-cognitive processes.

    This tool captures a structured reflection that can be part of a larger
    reflection sequence. Each reflection has a stage, type, and can reference
    previous reflections.

    Returns
    -------
        A result containing the reflection ID and count of stored reflections.

    """
    if follows_from is None:
        follows_from = []

    return reflection_store.add_reflection(content=content, stage=stage, rtype=rtype, follows_from=follows_from)


@mcp.tool()
def meta_reflect_summary() -> list[dict[str, Any]]:
    """🌌 Retrieve all stored reflections in sequence order.

    Returns
    -------
        A list of all stored reflections in sequence order.

    """
    return reflection_store.get_summary()


@mcp.tool()
def meta_reflect_reset() -> dict[str, Any]:
    """🌑 Reset the reflection store and sequence counter.

    Returns
    -------
        Confirmation of the reset operation.

    """
    return reflection_store.reset()


# Health check as a tool instead of a route
@mcp.tool()
def health_check() -> dict[str, Any]:
    """Health check endpoint for container environments."""
    return {"status": "ok", "service": "mcp-reflect", "version": __version__}


def run_server(transport: Literal["stdio", "streamable-http", "sse"] = "stdio") -> None:
    """Start the MCP server with the defined tools.

    Args:
        transport: The transport mechanism to use ("stdio", "streamable-http", or "sse")

    """
    mcp.run(transport=transport)


def run_uvx_server() -> None:
    """Start the MCP server with HTTP transport for UVX."""
    import os

    # Get port from environment or use default
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    # Using streamable-http instead of http as per FastMCP's supported transports
    mcp.run(
        transport="streamable-http",
        host=host,
        port=port,
    )


if __name__ == "__main__":
    import sys

    # If "uvx" is passed as an argument, run in HTTP mode
    if len(sys.argv) > 1 and sys.argv[1] == "uvx":
        run_uvx_server()
    else:
        run_server()
