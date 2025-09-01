# Version History

## 0.1.2 (Current Release)

### Major Features
- **Interactive Agent System**: Refactored from `/code` to `/agents` with arrow key navigation
  - **Coder Agent**: Full CRUD operations for file management
  - **Analyst Agent**: Placeholder for future data analysis features
- **Rich Visual Interface**: Syntax highlighting and colored panels for all code displays
- **Multi-Select File Reference**: Choose multiple files when referencing existing codebase
- **Cross-Platform Clipboard**: Copy generated code to clipboard (requires pyperclip)
- **ASCII Banner**: Stylized startup banner with version display

### Interactive Workflow Improvements
- **CRUD Menu System**: Create, Read, Update, Delete operations with visual feedback
- **Arrow Key Navigation**: InquirerPy-based menus throughout the application
- **Visual Code Display**: All code shown with syntax highlighting, line numbers, and themed panels
- **Always-Show-Then-Save**: Generated code always displayed before saving to file
- **Confirmation Dialogs**: Type-to-confirm deletion for safety
- **Session Loop**: Return to agent menu after operations for continuous workflow

### Agent Features
#### Coder Agent
- **Create**: Generate new code with optional multi-file codebase reference
- **Read**: Display file content with rich syntax highlighting
- **Update**: Placeholder for future code modification features
- **Delete**: Safe file deletion with filename confirmation
- **Exit**: Clean exit from coder interface

#### Multi-File Reference System
- **y/n Codebase Prompt**: Simple yes/no for codebase reference
- **Folder Path Input**: Specify codebase directory
- **File Multi-Select**: Choose specific files with Space bar toggle
- **Select All Option**: Bulk select all Python files in directory
- **Visual File Tree**: Files displayed with 📄 icons and relative paths

### Visual Enhancements
- **Colored Panels**: Blue for file content, yellow for previews, green for generated code
- **Syntax Highlighting**: Python code with monokai theme
- **Line Numbers**: All code displays include line numbering
- **Rich Console**: Enhanced terminal output with icons and formatting
- **ASCII Art Banner**: pyfiglet-generated banner with version info

### Technical Improvements
- **Optional Dependencies**: Graceful fallback when pyperclip unavailable
- **Error Handling**: Comprehensive exception handling for file operations
- **Path Resolution**: Robust file path handling for cross-platform compatibility
- **Memory Management**: Efficient code context building and display

### Commands Updated
- **Removed**: `/code` command (replaced by `/agents` → Coder)
- **Added**: `/agents` command with interactive agent selection
- **Enhanced**: Banner display on `brocode` and `brocode start`

### Future Release Preview
- **Copy to Clipboard**: Full clipboard integration (partially implemented)
- **Update Code Functionality**: Intelligent code modification capabilities
- **Session State for Chat**: Persistent conversation history
- **Version Control**: Git integration for code changes

## 0.1.1

### New Features
- **BroSession Directory Structure**: All session files now organized in `brosession/` folder
  - `brosession/brocode_config.yaml` - Model configurations
  - `brosession/session.db` - Session data
  - `brosession/prompt_hub/` - Customizable prompt files
- **Per-Directory Sessions**: Each directory maintains independent configurations
- **Customizable Prompts**: Users can edit prompt files in `brosession/prompt_hub/`
- **Automatic Prompt Copying**: Prompt files copied from package to brosession on first run
- **Session Management**: `brocode model config` command to show config file location

### Bug Fixes
- **Fixed Prompt File Path Issues**: Resolved "can't find ./prompt_hub/*.md" errors
- **Fixed Configuration Location**: Config files now properly created in brosession directory
- **Improved Resource Management**: Uses `importlib.resources` instead of deprecated `pkg_resources`

### Technical Improvements
- **Package Resource Handling**: Proper bundling of prompt files with package
- **Path Resolution**: Robust file path handling for cross-platform compatibility
- **Session Isolation**: Each project directory maintains separate session state

### Commands Added
- `brocode model config` - Display configuration file location and status

## 0.1.0

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