"""Data models for mcp-reflect.

This module contains the Pydantic models used for input and output validation
in the MCP-reflect tool.
"""

import uuid
from collections.abc import Sequence
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


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
        ...,
        min_length=1,
        description="The original model response to reflect upon and improve",
    )
    query: str | None = None
    focus_dimensions: list[EvaluationDimension] | None = Field(
        default=None, description="Specific dimensions to focus on during evaluation"
    )
    improvement_prompt: str | None = None

    @classmethod
    @field_validator("focus_dimensions", mode="before")
    def set_focus_dimensions(
        cls: type["ReflectionInput"], v: Sequence[EvaluationDimension] | None
    ) -> Sequence[EvaluationDimension] | None:
        """Convert empty list to None for focus_dimensions."""
        if v is None or v == []:
            return None
        return v


class Stage(str, Enum):
    """Stages for structured reflection process."""

    PROBLEM = "problem"
    ANALYSIS = "analysis"
    EXPLORATION = "exploration"
    SYNTHESIS = "synthesis"
    CONCLUSION = "conclusion"


class RType(str, Enum):
    """Types of reflection for different cognitive approaches."""

    CRITICAL = "critical"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    INTEGRATIVE = "integrative"
    META = "meta"


class Reflection(BaseModel):
    """A structured reflection model for meta-cognitive processes."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str = Field(..., min_length=1, description="Content of the reflection")
    seq: int
    stage: Stage
    rtype: RType
    follows_from: list[int] = Field(default_factory=list)
    ts: str = Field(default_factory=lambda: datetime.now().isoformat())

    @classmethod
    @field_validator("content")
    def validate_content(cls, v: str) -> str:
        """Ensure reflection content is not empty."""
        if not v or len(v.strip()) == 0:
            raise ValueError("Reflection content cannot be empty")
        return v

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}
