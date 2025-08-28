# BroCode

## Goal

BroCode is a study of agentic workflow and AI agents framework designed to solve coding problems. It's model-agnostic and aims to work with all files in a repository like Claude, Amazon Q Developer, and other AI coding tools. Future versions will include code acceptance/rejection capabilities.

## Overview

A CLI tool for managing and running LLM-based chat agents with support for multiple model backends. BroCode uses an agentic workflow system that combines code generation, chat capabilities, and codebase analysis in an interactive flow.

## Installation

Use this:  
```bash
pip install brocode  
```
Or this:  
```bash
uv add brocode  
```

## Quick Start

1. **Register a model**:
```bash
brocode register --path mylocal.py --model llama3.2-11b --default
```

2. **Start chatting**:
```bash
brocode start
```

## Commands

### Register Models

Register LLM models from Python files:

```bash
# Register and set as default
brocode register --path mylocal.py --model mymodel --default

# Register with auto-generated name
brocode register --path mylocal.py
```

### Start Chat

Start interactive chat sessions:

```bash
# Use default model
brocode start

# Use specific model
brocode start --llm mymodel
```

### Model Management

```bash
# List registered models
brocode model list

# Remove models interactively
brocode model remove
```

## Creating Custom Models

Create a Python file with your LLM class:

```python
# mylocal.py
from brollm import BaseLLM, BedrockChat
from brocode.register import register_llm

@register_llm("llama3.2-11b")
class MyLocalLLM(BedrockChat):
    def __init__(self):
        super().__init__(model_name="us.meta.llama3-2-11b-instruct-v1:0")
```

## How BroCode Works

When you run `brocode start`, BroCode initiates an agentic workflow that provides two main modes:

### Workflow Overview

```
[Start] → [User Input] → [Route Decision]
                ↓
        ┌─────────────────┐
        ↓                 ↓
   [Code Mode]      [Chat Mode]
        ↓                 ↓
   [Code Generator]  [Chat Agent]
        ↓                 ↓
        └─────────────────┘
                ↓
        [Back to User Input]
```

### Interactive Commands

- **`/code`** - Enter code generation mode
  - Prompts for coding task description
  - Optionally analyze existing codebase for context
  - Choose output format (terminal display or save to file)
  - Generates Python code following best practices
  
- **`/exit`** - Quit the session
- **`/clear`** - Clear chat history
- **Default input** - Enter chat mode for general conversation

### Code Generation Workflow

1. **Task Input**: Describe what you want to code
2. **Codebase Analysis** (optional): 
   - Provide folder or file path
   - BroCode analyzes Python files using AST parsing
   - Extracts classes, functions, imports, and structure
   - Maintains consistency with existing code patterns
3. **Output Selection**: Choose terminal display or file save
4. **Code Generation**: AI generates code following:
   - PEP 8 style guidelines
   - Google docstring format
   - Type hints and error handling
   - Consistency with existing codebase patterns

### Chat Mode

Provides general coding assistance, debugging help, and technical discussions using a knowledgeable coding assistant persona.

## Configuration

Models are stored in `.brocode_config.yaml` in your current directory.

### Configuration File Structure

```yaml
models:
  llama3.2-11b: /path/to/mylocal.py
  gpt-4: /path/to/gpt4_model.py
default_model: llama3.2-11b
```

## Dependencies

- Python >=3.12
- click >=8.2.1
- brollm >=0.1.2
- broflow >=0.1.4
- broprompt >=0.1.5