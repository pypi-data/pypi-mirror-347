"""
MCP server implementation for the mcp-reflect tool.

This module provides the FastMCP server and tool definitions for model
self-reflection capabilities.
"""

from typing import Annotated, Literal, Optional, Sequence
from fastmcp import FastMCP, Context, Image
from pydantic import Field

from mcp_reflect.models import (
    EvaluationDimension,
    ReflectionInput, 
    ReflectionResult
)
from mcp_reflect.evaluator import evaluate_response

# Create the MCP server
mcp = FastMCP(
    "Model Self-Reflection Tools",
    description="Tools for improving model self-reflection capabilities",
    dependencies=["fastmcp", "pydantic>=2.0.0", "async-lru"]
)


@mcp.tool()
async def reflect(
    response: str = Field(
        description="The original model response to reflect upon and improve"
    ),
    query: Optional[str] = Field(
        None, description="The original query that prompted the response"
    ),
    focus_dimensions: Optional[Sequence[EvaluationDimension]] = Field(
        None, description="Specific dimensions to focus on during evaluation"
    ),
    improvement_prompt: Optional[str] = Field(
        None, description="Additional context or specific instructions for improvement"
    ),
) -> ReflectionResult:
    """
    Reflect on and improve a model's response with structured evaluation.
    
    This tool analyzes the provided response against multiple quality dimensions,
    generates an improved version, and provides detailed feedback with specific
    suggestions for improvement.
    
    Returns:
        A reflection result containing the improved response and detailed evaluation.
    """
    input_data = ReflectionInput(
        response=response,
        query=query,
        focus_dimensions=focus_dimensions,
        improvement_prompt=improvement_prompt,
    )
    
    return await evaluate_response(input_data)


@mcp.tool()
async def sequential_reflect(
    responses: Sequence[str] = Field(
        description="A sequence of model responses to analyze",
        min_items=1,
    ),
    mode: Annotated[
        Literal["independent", "iterative", "comparative"],
        Field(description="How to process multiple responses")
    ] = "independent",
    context: Optional[Context] = None,
) -> Sequence[ReflectionResult]:
    """
    Process multiple responses sequentially with different reflection strategies.
    
    Modes:
    - independent: Each response is analyzed separately
    - iterative: Each reflection builds upon previous improvements
    - comparative: Responses are evaluated against each other
    
    Returns:
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
                improvement_prompt=f"Iteration {i+1}/{len(responses)}"
            )
            result = await evaluate_response(input_data)
            results.append(result)
            current = result.improved_response
            
    elif mode == "comparative":
        # Compare responses against each other
        for i, response in enumerate(responses):
            others = [r for j, r in enumerate(responses) if j != i]
            input_data = ReflectionInput(
                response=response,
                improvement_prompt=f"Compare with other responses for improvement"
            )
            result = await evaluate_response(input_data)
            results.append(result)
    
    return results


def run_server(host: str = "0.0.0.0", port: int = 8080):
    """
    Start the MCP server with the defined tools.
    
    Args:
        host: Host address to bind the server to
        port: Port number to use
    """
    mcp.run(host=host, port=port)


if __name__ == "__main__":
    run_server()
