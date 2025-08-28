# Version History

## 0.1.0 (Current Release)

### Core Features
- **Agentic Workflow System**: Multi-mode interactive workflow using broflow framework
- **CLI Interface**: Command-line tool for LLM model management and chat sessions
- **Model Registration**: Register custom LLM models from Python files with `@register_llm` decorator
- **Dual-Mode Operation**: Code generation mode and chat mode in unified workflow
- **Codebase Analysis**: AST-based Python code analysis for context-aware generation
- **Model Management**: List and remove registered models
- **Default Model Support**: Set and use default models for quick access
- **Persistent Configuration**: Models stored in `.brocode_config.yaml`

### Workflow Components
- **UserInput Action**: Routes user input to appropriate workflow branches
- **CodeGenerator Action**: 
  - Interactive code generation with codebase context
  - AST parsing for existing code analysis
  - Multiple output formats (terminal/file)
  - Consistency with existing code patterns
- **Chat Action**: General coding assistance and conversation
- **Shared State**: Pydantic-based state management across workflow actions

### Commands
- `brocode register --path <file> [--model <name>] [--default]` - Register LLM models
- `brocode start [--llm <model>]` - Start agentic workflow session
- `brocode model list` - List all registered models
- `brocode model remove` - Interactive model removal

### Interactive Commands (within session)
- `/code` - Enter code generation mode
- `/exit` - Quit the session
- `/clear` - Clear chat history
- Default input - Enter chat mode

### Technical Architecture
- **broflow Integration**: Action-based workflow system with routing
- **AST Code Analysis**: `MultiScriptContextBuilder` for codebase understanding
- **Prompt Management**: Markdown-based system prompts via broprompt
- **Click-based CLI**: Modern command-line interface
- **Dynamic Module Loading**: Import and register models from arbitrary Python files
- **LLM Registry**: In-memory registry with persistent YAML storage
- **Error Handling**: Comprehensive file existence checks and graceful error messages

### Code Generation Features
- **PEP 8 Compliance**: Automatic style guideline following
- **Google Docstrings**: Standardized documentation format
- **Type Hints**: Full type annotation support
- **Codebase Consistency**: Matches existing patterns and conventions
- **SOLID Principles**: Object-oriented design best practices
- **Error Handling**: Proper exception management

### Dependencies
- Python >=3.12
- click >=8.2.1  
- brollm >=0.1.2 (LLM abstraction)
- broflow >=0.1.4 (Workflow framework)
- broprompt >=0.1.5 (Prompt management)
- pydantic >=2.11.7 (Data validation)
- duckdb >=1.3.2

### File Structure
```
brocode/
├── actions/           # Workflow action components
│   ├── chat.py       # Chat interaction action
│   ├── code_generator.py  # Code generation action
│   └── user_input.py # User input routing action
├── prompt_hub/       # System prompts
│   ├── chat.md       # Chat assistant persona
│   └── code_generator.md  # Code generation guidelines
├── cli.py           # Command-line interface
├── flow.py          # Workflow definition
├── register.py      # Model registration system
├── code_analysis.py # AST-based code analysis
└── chat.py          # Legacy chat functionality
```