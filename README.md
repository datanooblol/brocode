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

When you run `brocode start`, BroCode creates a `brosession` directory in your current location and initiates an agentic workflow with two main modes:

### BroSession Directory Structure

BroCode organizes all session-related files in a `brosession` directory:

```
your-project/
├── brosession/
│   ├── brocode_config.yaml    # Model configurations
│   ├── session.db             # Session data
│   └── prompt_hub/            # Customizable prompts
│       ├── chat.md           # Chat assistant persona
│       └── code_generator.md  # Code generation guidelines
└── your-code-files...
```

### Session Management

- **Per-Directory Sessions**: Each directory gets its own `brosession` with independent configurations
- **Customizable Prompts**: Edit files in `brosession/prompt_hub/` to customize AI behavior
- **Portable Sessions**: Move or copy `brosession` folders to share configurations
- **Easy Cleanup**: Delete `brosession` folder to reset everything

### Workflow Overview

```
[Start] → [Setup BroSession] → [User Input] → [Route Decision]
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

- **`/agents`** - Enter agent selection mode with interactive menu
  - **Coder Agent**: Full-featured code operations with create and modify capabilities
    - **Create**: Generate new Python code with codebase reference and multi-file selection
    - **Modify**: Update existing Python code with preview-before-apply workflow
  - **Analyst Agent**: Data analysis capabilities (Coming in next release)
  
- **`/exit`** - Quit the session
- **`/clear`** - Clear chat history
- **Default input** - Enter chat mode for general conversation

### Coder Agent Features

#### Interactive CRUD Operations
- **Arrow Key Navigation**: Use ↑↓ keys to navigate all menus
- **Multi-Select File Reference**: When referencing codebase:
  - Select multiple files with Space bar
  - "✅ Select All" option for bulk selection
  - Visual file tree with 📄 icons
- **Visual Code Display**: All code shown with syntax highlighting and line numbers
- **Cross-Platform Clipboard**: Copy generated code to clipboard (when pyperclip available)

#### Create Workflow
1. **Task Description**: What you want to create
2. **Codebase Reference** (optional): 
   - y/n prompt for existing codebase
   - Folder path input
   - Multi-select files for reference
3. **Output Method**: Display in terminal or save to file
4. **Code Generation**: Always displays code first, then saves if requested
5. **Clipboard Copy**: Optional copy to clipboard

#### Modify Workflow
1. **Target File Selection**: Choose Python file to modify
2. **Modification Request**: Describe changes needed
3. **Codebase Reference** (optional): Reference additional files for context
4. **Preview Changes**: View proposed modifications before applying
5. **Accept/Reject**: Choose to apply changes or cancel
6. **No Backup Files**: Direct modification without .backup files

### Code Generation & Modification Features

- **Rich Visual Display**: All code shown with syntax highlighting, line numbers, and colored panels
- **AST-Based Analysis**: Intelligent parsing of existing Python codebases
- **Multi-File Context**: Reference multiple files simultaneously for better context
- **Interactive File Selection**: Visual file browser with multi-select capabilities
- **Clipboard Integration**: Copy generated code directly to system clipboard
- **Preview-Before-Apply**: See modifications before they're applied to files
- **Error Handling**: Comprehensive error handling with user choices (retry/skip/cancel)
- **File Support**: Works with both .py and .md files for codebase reference
- **PEP 8 Compliance**: Automatic style guideline following
- **Google Docstrings**: Standardized documentation format
- **Type Hints**: Full type annotation support

### Chat Mode

Provides general coding assistance, debugging help, and technical discussions using a knowledgeable coding assistant persona.

## Configuration

Models are stored in `brosession/brocode_config.yaml` in your current directory. Use `brocode model config` to see the exact location.

### Configuration File Structure

```yaml
models:
  llama3.2-11b: /path/to/mylocal.py
  gpt-4: /path/to/gpt4_model.py
default_model: llama3.2-11b
```

### Customizing Prompts

After running `brocode start` once, you can customize the AI behavior by editing:
- `brosession/prompt_hub/chat.md` - Chat assistant personality and instructions
- `brosession/prompt_hub/code_generator.md` - Code generation guidelines and style
- `brosession/prompt_hub/code_modifier.md` - Code modification guidelines and behavior

**Smart File Management**: BroCode only copies missing prompt files, preserving your customizations while ensuring all required files are present.

## Dependencies

- Python >=3.12
- click >=8.2.1
- brollm >=0.1.2
- broflow >=0.1.4
- broprompt >=0.1.5
- inquirerpy >=0.3.4
- rich >=14.1.0
- pyfiglet >=1.0.4