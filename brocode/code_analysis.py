import ast  # Import Abstract Syntax Tree module for parsing Python code
from pathlib import Path  # Import Path for cross-platform file path handling
from dataclasses import dataclass  # Import dataclass decorator for creating data classes
from typing import List, Optional, Dict  # Import type hints for better code documentation

@dataclass
class FunctionInfo:
    """Data class to store information about a function.
    
    Attributes:
        name: The name of the function.
        args: List of argument names for the function.
        return_type: The return type annotation if present, None otherwise.
        docstring: The function's docstring if present, None otherwise.
        line_start: The line number where the function starts.
        line_end: The line number where the function ends.
    """
    name: str  # Function name
    args: List[str]  # List of function argument names
    return_type: Optional[str]  # Return type annotation (if any)
    docstring: Optional[str]  # Function docstring (if any)
    line_start: int  # Starting line number
    line_end: int  # Ending line number

@dataclass
class ClassInfo:
    """Data class to store information about a class.
    
    Attributes:
        name: The name of the class.
        methods: List of method names in the class.
        inheritance: List of base classes this class inherits from.
        docstring: The class's docstring if present, None otherwise.
        line_start: The line number where the class starts.
        line_end: The line number where the class ends.
    """
    name: str  # Class name
    methods: List[str]  # List of method names in the class
    inheritance: List[str]  # List of base classes
    docstring: Optional[str]  # Class docstring (if any)
    line_start: int  # Starting line number
    line_end: int  # Ending line number

class ASTParser(ast.NodeVisitor):
    """AST visitor class to parse Python code and extract functions, classes, and imports.
    
    Inherits from ast.NodeVisitor to traverse the Abstract Syntax Tree.
    
    Attributes:
        functions: List to store FunctionInfo objects.
        classes: List to store ClassInfo objects.
        imports: List to store import statements.
    """
    
    def __init__(self):
        """Initialize the parser with empty lists for storing parsed elements."""
        self.functions = []  # Initialize empty list for functions
        self.classes = []  # Initialize empty list for classes
        self.imports = []  # Initialize empty list for imports
        
    def visit_FunctionDef(self, node):
        """Visit function definition nodes and extract function information.
        
        Args:
            node: The AST node representing a function definition.
        """
        func = FunctionInfo(  # Create FunctionInfo object
            name=node.name,  # Extract function name
            args=[arg.arg for arg in node.args.args],  # Extract argument names
            return_type=ast.unparse(node.returns) if node.returns else None,  # Extract return type if present
            docstring=ast.get_docstring(node),  # Extract docstring if present
            line_start=node.lineno,  # Get starting line number
            line_end=node.end_lineno or node.lineno  # Get ending line number or use start if not available
        )
        self.functions.append(func)  # Add function info to list
        self.generic_visit(node)  # Continue visiting child nodes
        
    def visit_ClassDef(self, node):
        """Visit class definition nodes and extract class information.
        
        Args:
            node: The AST node representing a class definition.
        """
        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]  # Extract method names from class body
        inheritance = [ast.unparse(base) for base in node.bases]  # Extract base class names
        cls = ClassInfo(  # Create ClassInfo object
            name=node.name,  # Extract class name
            methods=methods,  # Set extracted methods
            inheritance=inheritance,  # Set extracted base classes
            docstring=ast.get_docstring(node),  # Extract docstring if present
            line_start=node.lineno,  # Get starting line number
            line_end=node.end_lineno or node.lineno  # Get ending line number or use start if not available
        )
        self.classes.append(cls)  # Add class info to list
        self.generic_visit(node)  # Continue visiting child nodes
        
    def visit_Import(self, node):
        """Visit import nodes and extract import statements.
        
        Args:
            node: The AST node representing an import statement.
        """
        for alias in node.names:  # Iterate through imported names
            self.imports.append(alias.name)  # Add import name to list
            
    def visit_ImportFrom(self, node):
        """Visit 'from ... import ...' nodes and extract import statements.
        
        Args:
            node: The AST node representing a 'from import' statement.
        """
        module = node.module or ""  # Get module name or empty string if None
        for alias in node.names:  # Iterate through imported names
            self.imports.append(f"{module}.{alias.name}")  # Add qualified import name to list

class MultiScriptContextBuilder:
    """Builder class for creating context from multiple Python script files.
    
    This class parses Python files and creates structured context information
    that can be used for code analysis or documentation purposes.
    """
    
    def __init__(self):
        """Initialize the context builder."""
        pass  # No initialization needed
    
    def parse_single_file(self, file_path: Path) -> Dict:
        """Parse a single Python file and extract its structure.
        
        Args:
            file_path: Path to the Python file to parse.
            
        Returns:
            Dictionary containing parsed functions, classes, imports, and source code.
        """
        with open(file_path, 'r', encoding='utf-8') as f:  # Open file with UTF-8 encoding
            content = f.read()  # Read entire file content
        
        tree = ast.parse(content)  # Parse content into AST
        parser = ASTParser()  # Create parser instance
        parser.visit(tree)  # Visit all nodes in the AST
        
        return {  # Return dictionary with parsed data
            'functions': parser.functions,  # List of FunctionInfo objects
            'classes': parser.classes,  # List of ClassInfo objects
            'imports': parser.imports,  # List of import statements
            'source_code': content  # Original source code
        }
    
    def create_context(self, parsed_data: Dict) -> str:
        """Create minimal context string with code and structure summary.
        
        Args:
            parsed_data: Dictionary containing parsed file data.
            
        Returns:
            Formatted string containing code and structure information.
        """
        
        context = f"CODE:\n```python\n{parsed_data['source_code']}\n```\n\n"  # Add source code section
        context += "STRUCTURE SUMMARY:\n"  # Add structure summary header
        
        # Classes with inheritance
        if parsed_data['classes']:  # Check if classes exist
            context += "Classes:\n"  # Add classes header
            for cls in parsed_data['classes']:  # Iterate through classes
                if cls.inheritance:  # Check if class has inheritance
                    inheritance = f" extends {', '.join(cls.inheritance)}"  # Format inheritance info
                else:
                    inheritance = ""  # No inheritance
                context += f"  - {cls.name}{inheritance} (methods: {', '.join(cls.methods)})\n"  # Add class info
        
        # Imports
        if parsed_data['imports']:  # Check if imports exist
            context += f"Imports: {', '.join(parsed_data['imports'])}\n"  # Add imports info
        
        return context  # Return formatted context string
    
    def build_contexts(self, file_paths: List[Path]) -> Dict[str, str]:
        """Build contexts for multiple files (.py and .md supported).
        
        Args:
            file_paths: List of Path objects pointing to supported files.
            
        Returns:
            Dictionary mapping file paths to their context strings.
        """
        contexts = {}  # Initialize empty dictionary for contexts
        
        for file_path in file_paths:  # Iterate through each file path
            try:
                if not file_path.exists():
                    contexts[str(file_path)] = f"ERROR: File not found - {file_path.name}"
                    continue
                    
                if file_path.suffix == '.py':
                    try:
                        # Use existing Python parsing
                        parsed_data = self.parse_single_file(file_path)  # Parse the file
                        context = self.create_context(parsed_data)  # Create context string
                    except SyntaxError as e:
                        # Python syntax error - offer fallback
                        try:
                            content = file_path.read_text(encoding='utf-8')
                            context = f"PYTHON FILE (Syntax Error - Using as Text):\nSyntax Error: {str(e)}\n\nCODE:\n```python\n{content}\n```"
                        except Exception:
                            context = f"ERROR: Python file has syntax errors and cannot be read - {str(e)}"
                    except Exception as e:
                        context = f"ERROR: Could not parse Python file {file_path.name} - {str(e)}"
                        
                elif file_path.suffix == '.md':
                    try:
                        # Simple content reading for markdown
                        content = file_path.read_text(encoding='utf-8')
                        context = f"MARKDOWN CONTENT:\n{content}"
                    except UnicodeDecodeError:
                        context = f"ERROR: Cannot decode {file_path.name} - file may be binary or use unsupported encoding"
                    except Exception as e:
                        context = f"ERROR: Could not read markdown file {file_path.name} - {str(e)}"
                        
                else:
                    context = f"ERROR: Unsupported file type {file_path.suffix} for {file_path.name}"
                    
                contexts[str(file_path)] = context  # Store context with file path as key
                
            except Exception as e:  # Handle unexpected errors
                contexts[str(file_path)] = f"ERROR: Unexpected error processing {file_path.name} - {str(e)}"  # Store error message
        
        return contexts  # Return dictionary of contexts