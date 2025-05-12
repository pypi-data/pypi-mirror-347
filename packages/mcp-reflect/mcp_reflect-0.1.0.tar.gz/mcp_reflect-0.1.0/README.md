# MCP-Reflect 🪞

[![PyPI version](https://img.shields.io/pypi/v/mcp-reflect.svg)](https://pypi.org/project/mcp-reflect/)
[![Python versions](https://img.shields.io/pypi/pyversions/mcp-reflect.svg)](https://pypi.org/project/mcp-reflect/)
[![Tests](https://github.com/JonesH/mcp-reflect/actions/workflows/test.yml/badge.svg)](https://github.com/JonesH/mcp-reflect/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**MCP-Reflect** is a Model Control Protocol (MCP) tool for enhancing model self-reflection capabilities. It helps improve AI responses through structured evaluation and feedback.

## 🌟 Features

- ✅ **Qualitative Response Improvement** - Transform model outputs into more accurate, clear, and complete versions
- ✅ **Structured Self-Evaluation** - Score responses across multiple quality dimensions
- ✅ **Concrete Improvement Suggestions** - Get actionable feedback for each dimension
- ✅ **Multiple Processing Modes** - Process responses independently, iteratively, or comparatively
- ✅ **MCP-Compatible** - Seamlessly integrates with Claude and other MCP-compatible assistants

## 📊 Evaluation Dimensions

MCP-Reflect evaluates model responses across these key dimensions:

- **Accuracy**: Factual correctness and absence of errors
- **Clarity**: How well-structured and easy to understand the response is
- **Completeness**: Whether all relevant aspects of the topic are addressed
- **Relevance**: How directly the response addresses the query
- **Coherence**: Logical flow and consistency of reasoning
- **Conciseness**: Appropriate length without unnecessary repetition
- **Helpfulness**: Practical value and actionability of the response
- **Reasoning**: Quality of logic, evidence, and argumentation
- **Safety**: Responsible handling of sensitive topics

## 🚀 Installation

### Using pip

```bash
# Install from PyPI (stable releases)
pip install mcp-reflect

# Install with all dependencies (including optional)
pip install "mcp-reflect[core]"

# Install latest development version from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ "mcp-reflect[core]"
```

### Using Poetry

```bash
# Install from PyPI (stable releases)
poetry add mcp-reflect

# Install from TestPyPI (development versions)
poetry source add --priority=supplemental test-pypi https://test.pypi.org/simple/
poetry add --source test-pypi mcp-reflect
```

### Using UV

UV is a fast Python package installer written in Rust. To install with UV:

```bash
# Install UV if you haven't already
curl -sSf https://install.ultraviolet.rs | sh

# Install the package globally as a tool
uv tool install mcp-reflect

# Or install the package with pip
uv pip install mcp-reflect

# Run the package without installing
uvx mcp-reflect
```

## 💡 Usage

### Starting the Server

Run the MCP server directly from the command line:

```bash
mcp-reflect
```

Or programmatically:

```python
from mcp_reflect.server import run_server

# Start on a custom host and port
run_server(host="127.0.0.1", port=9000)
```

### Running with HTTP Server

MCP-Reflect can provide an HTTP server for API access:

```bash
# Install with HTTP server support
pip install "mcp-reflect[all]"

# Install with UV (with HTTP server support)
uv tool install "mcp-reflect[all]"

# Run the HTTP server
mcp-reflect-uvx
```

You can customize the host and port using environment variables:

```bash
# Set custom host and port
export HOST=127.0.0.1
export PORT=8080
mcp-reflect-uvx
```

Or run it programmatically:

```python
from mcp_reflect.server import run_uvx_server

# This will start an HTTP server on the specified host and port
run_uvx_server()
```

Once running, the server provides the MCP tools via HTTP endpoints that can be accessed by API clients.

### Basic Reflection

The simplest way to use the tool is to pass a model response for reflection:

```python
import asyncio
from mcp_reflect.server import reflect

async def improve_response():
    result = await reflect(
        response="The Earth is approximately 6000 years old according to some estimates.",
        query="How old is the Earth?"
    )
    
    print(f"Improved response: {result.improved_response}")
    print(f"Overall assessment: {result.overall_assessment}")
    
    # Print scores for each dimension
    for score in result.scores:
        print(f"{score.dimension.value}: {score.score}/10 - {score.improvement_suggestion}")

asyncio.run(improve_response())
```

### Sequential Processing

Process multiple responses with different strategies:

```python
import asyncio
from mcp_reflect.server import sequential_reflect

async def process_multiple_responses():
    responses = [
        "The Earth is approximately 6000 years old according to some estimates.",
        "The Earth formed about 4.5 billion years ago, but there are different methods to determine this."
    ]
    
    # Process iteratively (each reflection builds on previous improvements)
    results = await sequential_reflect(responses=responses, mode="iterative")
    
    # Show the final improved response
    print(f"Final improved response: {results[-1].improved_response}")

asyncio.run(process_multiple_responses())
```

### Integration with Claude

MCP-Reflect is designed to work seamlessly with Claude and other MCP-compatible assistants. Here's how to use it with Claude:

1. Start the MCP server: `mcp-reflect`
2. Connect Claude to the server (usually handled by your client application)
3. Call the reflection tool directly from Claude:

```
I'd like to analyze and improve my previous response. Could you use the reflect tool for this?

<response>
The Earth is approximately 6000 years old according to some estimates.
</response>
```

## 🧠 Advanced Usage

### Custom Evaluation Focus

Focus on specific dimensions for targeted improvement:

```python
import asyncio
from mcp_reflect.models import EvaluationDimension
from mcp_reflect.server import reflect

async def focused_evaluation():
    result = await reflect(
        response="The Earth is approximately 6000 years old according to some estimates.",
        query="How old is the Earth?",
        focus_dimensions=[
            EvaluationDimension.ACCURACY,
            EvaluationDimension.REASONING
        ]
    )
    
    # Print focused evaluation results
    for score in result.scores:
        print(f"{score.dimension.value}: {score.score}/10")

asyncio.run(focused_evaluation())
```

### Custom Improvement Instructions

Provide specific guidance for improvement:

```python
import asyncio
from mcp_reflect.server import reflect

async def guided_improvement():
    result = await reflect(
        response="The Earth is approximately 6000 years old according to some estimates.",
        improvement_prompt="Add scientific consensus and methodologies used for dating."
    )
    
    print(result.improved_response)

asyncio.run(guided_improvement())
```

## 🔬 How It Works

MCP-Reflect uses a multi-stage process to evaluate and improve model responses:

1. **Analysis Phase**: The original response is analyzed across multiple quality dimensions
2. **Scoring Phase**: Each dimension receives a numerical score with specific reasoning
3. **Improvement Phase**: Concrete suggestions for improvement are generated
4. **Synthesis Phase**: An improved version of the response is created
5. **Packaging Phase**: All insights are structured into a comprehensive result

## 🛠️ Development

### Setup

```bash
# Clone the repository
git clone https://github.com/JonesH/mcp-reflect.git
cd mcp-reflect

# Install with Poetry
poetry install

# Run tests
poetry run pytest
```

### Project Structure

- `mcp_reflect/models.py` - Data models for evaluation
- `mcp_reflect/evaluator.py` - Core evaluation logic
- `mcp_reflect/server.py` - MCP server and tool definitions
- `tests/` - Test suite

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
