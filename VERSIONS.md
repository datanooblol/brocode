# Version History

## Version 0.1.3 (Current)

### 🚀 Major Features
- **Code Modification System**: Complete code modification workflow with accept/reject flow
- **Modular Architecture**: Refactored monolithic code_generator.py into clean, modular components
- **Enhanced File Support**: Extended from Python-only to support both .py and .md files
- **Smart File Management**: Only copies missing prompt files, preserving user customizations
- **Debug Mode**: Added `--debug` flag to `brocode start` command

### 🔧 Technical Improvements
- **CodeAgent Wrapper**: Unified interface combining CodeGenerator and CodeModifier
- **Comprehensive Error Handling**: User-controlled error handling with retry/skip/cancel options
- **Shared Components**: Moved common functionality to utils/ directory
- **No Backup Files**: Direct file modification without creating .backup files
- **Streamlined UX**: CodeGenerator goes directly to code creation, bypassing CRUD menu

### 🎯 User Experience
- **Simple Modification Flow**: Ask filename → Ask codebase → Modify → Show result → Accept/Reject
- **Multi-File Context**: Reference multiple files for better code generation
- **Visual File Selection**: Interactive file browser with multi-select
- **Error Recovery**: Graceful handling of LLM errors with user choices

### 📋 CLI Enhancements
- **Debug Flag**: `brocode start --debug True/False` for debugging support
- **Enhanced Prompts**: All prompt files copied to brosession/prompt_hub/ for user customization
- **Template Consistency**: code_modifier.md prompt template added

### 🔄 Workflow Improvements
- **Direct Generation**: CodeGenerator bypasses CRUD menu, goes straight to creation
- **Unified Interface**: CodeAgent provides single entry point for all code operations
- **Session Management**: Improved brosession directory handling with smart file copying

---

## Version 0.1.2

### Features
- Initial code generation capabilities
- CRUD interface for code operations
- Basic file operations (Create, Read, Delete)
- Python-only file support

---

## Version 0.1.1

### Features
- Basic chat functionality
- Model registration system
- Session management
- Initial agentic workflow

---

## Version 0.1.0

### Features
- Initial release
- CLI interface
- Model management
- Basic chat capabilities