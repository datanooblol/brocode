# Version History

## 0.1.0 (Initial Release)

### Features
- **CLI Interface**: Command-line tool for LLM model management and chat sessions
- **Model Registration**: Register custom LLM models from Python files with `@register_llm` decorator
- **Interactive Chat**: Start chat sessions with registered models
- **Model Management**: List and remove registered models
- **Default Model Support**: Set and use default models for quick access
- **Persistent Configuration**: Models stored in `.brocode_config.yaml`

### Commands Added
- `brocode register --path <file> [--model <name>] [--default]` - Register LLM models
- `brocode start [--llm <model>]` - Start interactive chat sessions  
- `brocode model list` - List all registered models
- `brocode model remove` - Interactive model removal

### Technical Implementation
- **Click-based CLI**: Modern command-line interface using Python Click
- **Dynamic Module Loading**: Import and register models from arbitrary Python files
- **LLM Registry**: In-memory registry with persistent YAML storage
- **Chat Loop**: Interactive chat with `/exit` command support
- **Error Handling**: File existence checks and graceful error messages

### Dependencies
- Python >=3.12
- click >=8.2.1  
- brollm >=0.1.2
- broflow >=0.1.4
- broprompt >=0.1.5
- duckdb >=1.3.2