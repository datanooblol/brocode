# BroCode

## Goal

BroCode is a study of agentic workflow and AI agents framework designed to solve coding problems. It's model-agnostic and aims to work with all files in a repository like Claude, Amazon Q Developer, and other AI coding tools. Future versions will include code acceptance/rejection capabilities.

## Overview

A CLI tool for managing and running LLM-based chat agents with support for multiple model backends.

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

## Chat Commands

- Type `/exit` to quit the chat session
- All other input is sent to the LLM

## Configuration

Models are stored in `.brocode_config.yaml` in your current directory.

## Dependencies

- Python >=3.12
- click >=8.2.1
- brollm >=0.1.2
- broflow >=0.1.4
- broprompt >=0.1.5