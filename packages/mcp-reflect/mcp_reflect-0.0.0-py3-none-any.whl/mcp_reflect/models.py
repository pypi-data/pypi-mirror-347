"""
Data models for mcp-reflect.

This module contains the Pydantic models used for input and output validation
in the MCP-reflect tool.
"""

from enum import Enum
from collections.abc import Sequence
from pydantic import BaseModel, Field


class EvaluationDimension(str, Enum):
    """Dimensions for model response evaluation."""

    ACCURACY = "accuracy"
    CLARITY = "clarity"
    COMPLETENESS = "completeness"
    RELEVANCE = "relevance"
    COHERENCE = "coherence"
    CONCISENESS = "conciseness"
    HELPFULNESS = "helpfulness"
    REASONING = "reasoning"
    SAFETY = "safety"


class DimensionScore(BaseModel):
    """Score for a specific evaluation dimension."""

    dimension: EvaluationDimension
    score: float = Field(ge=1, le=10)
    reasoning: str
    improvement_suggestion: str


class ReflectionResult(BaseModel):
    """Complete result of the reflection process."""

    original_response: str
    improved_response: str
    scores: Sequence[DimensionScore]
    overall_assessment: str
    metadata: dict | None = None


class ReflectionInput(BaseModel):
    """Input for the reflection tool."""

    response: str = Field(
        description="The original model response to reflect upon and improve"
    )
    query: str | None = Field(
        None, description="The original query that prompted the response"
    )
    focus_dimensions: Sequence[EvaluationDimension] | None = Field(
        None,
        description="Specific dimensions to focus on during evaluation",
    )
    improvement_prompt: str | None = Field(
        None,
        description="Additional context or specific instructions for the improvement",
    )
