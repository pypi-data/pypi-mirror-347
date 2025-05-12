"""
Core evaluation logic for the MCP-reflect tool.

This module contains the functions responsible for analyzing model responses
and generating improved versions with detailed feedback.
"""

import asyncio
from collections.abc import Sequence

from pydantic import BaseModel

from mcp_reflect.models import (
    DimensionScore,
    EvaluationDimension,
    ReflectionInput,
    ReflectionResult,
)


class EvaluationPrompt(BaseModel):
    """Internal model for generating the evaluation prompt."""

    response: str
    query: str | None = None
    focus_dimensions: Sequence[EvaluationDimension] | None = None
    improvement_prompt: str | None = None


def _build_evaluation_prompt(input_data: ReflectionInput) -> str:
    """
    Build the full evaluation prompt from the input data.

    Args:
        input_data: The reflection input data

    Returns:
        Complete prompt string for the evaluator
    """
    prompt = "Evaluate and improve the following model response:\n\n"
    
    if input_data.query:
        prompt += f"ORIGINAL QUERY:\n{input_data.query}\n\n"
    
    prompt += f"RESPONSE TO EVALUATE:\n{input_data.response}\n\n"
    
    prompt += "Provide a comprehensive evaluation along these dimensions:\n"
    
    dimensions = input_data.focus_dimensions or list(EvaluationDimension)
    for dim in dimensions:
        prompt += f"- {dim.value.capitalize()}\n"
    
    prompt += "\nFor each dimension, provide:\n"
    prompt += "1. A score from 1-10\n"
    prompt += "2. Brief reasoning for the score\n"
    prompt += "3. Specific suggestions for improvement\n\n"
    
    prompt += "Then create an improved version of the response."
    
    if input_data.improvement_prompt:
        prompt += f"\n\nAdditional improvement instructions: {input_data.improvement_prompt}"
    
    return prompt


async def _parse_evaluation_response(raw_evaluation: str) -> ReflectionResult:
    """
    Parse the raw evaluation response into a structured format.

    Args:
        raw_evaluation: The raw string response from the evaluator

    Returns:
        Structured reflection result
    """
    # This is a simplified parsing implementation
    # In a real implementation, you would use more robust parsing
    
    sections = raw_evaluation.split("IMPROVED RESPONSE:")
    
    if len(sections) < 2:
        raise ValueError("Could not parse evaluation response")
    
    evaluation_text = sections[0].strip()
    improved_response = sections[1].strip()
    
    # Extract dimension scores
    scores = []
    for dim in EvaluationDimension:
        if dim.value.upper() in evaluation_text:
            dim_section = evaluation_text.split(dim.value.upper())[1].split("\n\n")[0]
            score_text = dim_section.split("Score:")[1].split("/10")[0].strip()
            score = float(score_text)
            
            reasoning = "See evaluation"
            if "Reasoning:" in dim_section:
                reasoning = dim_section.split("Reasoning:")[1].split("Improvement:")[0].strip()
            
            improvement = "See overall improvements"
            if "Improvement:" in dim_section:
                improvement = dim_section.split("Improvement:")[1].strip()
            
            scores.append(
                DimensionScore(
                    dimension=dim,
                    score=score,
                    reasoning=reasoning,
                    improvement_suggestion=improvement,
                )
            )
    
    # Extract overall assessment
    overall_assessment = "See evaluation details"
    if "OVERALL ASSESSMENT:" in evaluation_text:
        overall_assessment = evaluation_text.split("OVERALL ASSESSMENT:")[1].strip()
    
    return ReflectionResult(
        original_response=raw_evaluation,
        improved_response=improved_response,
        scores=scores,
        overall_assessment=overall_assessment,
    )


async def evaluate_response(input_data: ReflectionInput) -> ReflectionResult:
    """
    Evaluate a model response and provide improvement suggestions.

    This is a placeholder implementation. In a real-world scenario, you would:
    1. Send the evaluation prompt to an LLM
    2. Parse the response
    3. Return the structured result

    Args:
        input_data: The reflection input data

    Returns:
        Complete reflection result with scores and improved response
    """
    # Placeholder for API call to another model
    # In reality, you would use an API client here
    
    prompt = _build_evaluation_prompt(input_data)
    
    # Simulate API call delay
    await asyncio.sleep(0.1)
    
    # Placeholder response
    raw_evaluation = (
        "EVALUATION:\n\n"
        "ACCURACY: 7/10\n"
        "Reasoning: The response contains mostly accurate information but has a few minor errors.\n"
        "Improvement: Double-check factual claims and provide references where appropriate.\n\n"
        "CLARITY: 8/10\n"
        "Reasoning: The explanation is clear overall but could use better structure.\n"
        "Improvement: Use more headings and bullet points to organize information.\n\n"
        "COMPLETENESS: 6/10\n"
        "Reasoning: Some important aspects of the topic are not addressed.\n"
        "Improvement: Include information about X, Y, and Z to make the response more complete.\n\n"
        "OVERALL ASSESSMENT:\n"
        "The response is generally good but could be improved in terms of accuracy, "
        "clarity, and completeness. The improved version addresses these issues.\n\n"
        "IMPROVED RESPONSE:\n"
        f"Here is an improved version of the original response:\n\n{input_data.response}\n\n"
        "With improvements for clarity, accuracy, and completeness as identified in the evaluation."
    )
    
    return await _parse_evaluation_response(raw_evaluation)
