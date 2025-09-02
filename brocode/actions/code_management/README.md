# Code Management Module Specification

## Overview

The `code_management` module is the central hub for all code-related operations in BroCode. It provides a unified interface for code generation and modification through a wrapper agent architecture.

## Architecture

```
brocode/actions/code_management/
├── code_agent.py              # Main wrapper agent ✅ IMPLEMENTED
├── code_generator/            # Code generation functionality
│   ├── __init__.py
│   └── generate.py           # Main generator orchestrator
├── code_modifier/             # Code modification functionality
│   ├── __init__.py
│   └── modify.py             # Main modifier orchestrator
├── utils/                     # Shared utilities ✅ IMPLEMENTED
│   ├── __init__.py
│   ├── error_handler.py      # Error handling and debugging
│   ├── file_operations.py    # File CRUD operations
│   ├── file_selector.py      # File discovery and selection
│   ├── llm_handler.py        # LLM interaction and code parsing
│   └── ui_helper.py          # User interface helpers
└── README.md                 # This specification
```

## Components

### 1. Code Agent (`code_agent.py`)

**Purpose**: Main wrapper that orchestrates code generation and modification operations.

**Responsibilities**:
- Provide unified interface for code operations
- Route requests to appropriate sub-modules (generator/modifier)
- Handle high-level workflow coordination
- Manage shared state between operations

**Interface**:
```python
class CodeAgent(Action):
    def __init__(self, system_prompt: str, model: BaseLLM)
    def run(self, shared: Shared) -> Shared
    def generate_code(self, shared: Shared) -> Shared
    def modify_code(self, shared: Shared) -> Shared
```

### 2. Code Generator (`code_generator/generate.py`)

**Purpose**: Handle new code creation with codebase context.

**Current Functionality**:
- Interactive CRUD menu (Create, Read, Update, Delete, Debug)
- Multi-file codebase reference selection
- LLM-based code generation
- File operations with comprehensive error handling
- Syntax highlighting and rich display

**Key Features**:
- Support for `.py` and `.md` files
- Multi-select file reference with visual interface
- Automatic backup creation
- Clipboard integration
- Error inspection and debugging

### 3. Code Modifier (`code_modifier/modify.py`)

**Purpose**: Handle existing file updates and modifications.

**Current Functionality**:
- Target file selection with preview
- Update request specification
- Optional codebase reference
- Preview-before-apply workflow
- Automatic backup creation

**Workflow**:
1. Get target file to update
2. Get user's update/fix request
3. Get optional codebase reference
4. Generate updated code with LLM
5. Show updated code in terminal
6. User confirmation before applying
7. Apply update with backup

### 4. Shared Utilities (`utils/` - TO BE CREATED)

**Purpose**: Extract common functionality used by both generator and modifier.

#### Current Shared Components:
- `ErrorHandler` (from code_generator)
- `FileSelector` (from code_generator)
- File type detection logic
- LLM interaction patterns
- UI prompt patterns

#### Proposed Utils Structure:

**`file_utils.py`**:
- File type detection (`detect_file_language()`)
- Path resolution and validation
- Backup file creation
- File content reading with encoding handling

**`llm_utils.py`**:
- Code block parsing (`parse_python_codeblock()`, `parse_code_block()`)
- Common prompt building patterns
- Response validation and extraction
- Error handling for LLM operations

**`ui_utils.py`**:
- Common prompt templates
- File selection interfaces
- Confirmation dialogs
- Progress indicators
- Syntax highlighting helpers

## Current State Analysis

### Shared Functionality Identified:

1. **Error Handling**: Both modules use `ErrorHandler` from code_generator
2. **File Selection**: Both modules use `FileSelector` from code_generator  
3. **File Type Detection**: Duplicated logic in both modules
4. **LLM Interaction**: Similar patterns for code generation
5. **UI Patterns**: Common prompt and confirmation flows

### Refactoring Needed:

1. **Move Shared Classes to Utils**:
   - `ErrorHandler` → `utils/error_utils.py`
   - `FileSelector` → `utils/file_utils.py`
   - File type detection → `utils/file_utils.py`

2. **Extract Common LLM Patterns**:
   - Code parsing logic → `utils/llm_utils.py`
   - Prompt building → `utils/llm_utils.py`

3. **Create Code Agent Wrapper**:
   - Unified interface for both operations
   - Shared state management
   - Operation routing logic

## ✅ Implementation Status: COMPLETED

### Refactoring Completed:

1. **✅ Moved Shared Classes to Utils**:
   - `ErrorHandler` → `utils/error_handler.py`
   - `FileOperations` → `utils/file_operations.py`
   - `FileSelector` → `utils/file_selector.py`
   - `LLMHandler` → `utils/llm_handler.py`
   - `UIHelper` → `utils/ui_helper.py`

2. **✅ Created Code Agent Wrapper**:
   - `code_agent.py` implemented as main wrapper
   - Unified interface for both operations
   - Operation routing to generator/modifier
   - Clean separation of concerns

3. **✅ Updated Module Structure**:
   - `generate.py` uses shared utils
   - `modify.py` uses shared utils
   - Backward compatibility maintained
   - Clean import structure

## Usage Examples

### ✅ Current Code Agent Interface:
```python
# Via unified agent (RECOMMENDED)
agent = CodeAgent(system_prompt, model)
shared = agent.run(shared)  # Interactive menu with Generate/Modify options

# Direct operations
shared = agent.generate_code(shared)  # New code creation
shared = agent.modify_code(shared)    # Existing code updates
```

### Legacy Interface (Still Supported):
```python
# Code generation (backward compatibility)
generator = CodeGenerator(system_prompt, model)
shared = generator.run(shared)

# Code modification
modifier = CodeModifier(system_prompt, model)
shared = modifier.run(shared)
```

## Benefits of This Architecture

1. **Separation of Concerns**: Clear distinction between generation and modification
2. **Code Reuse**: Shared utilities eliminate duplication
3. **Maintainability**: Modular structure makes updates easier
4. **Extensibility**: Easy to add new code operations
5. **Testing**: Each component can be tested independently
6. **Consistency**: Unified interface and error handling patterns