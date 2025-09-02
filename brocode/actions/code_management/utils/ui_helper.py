"""UI helper functions for user interaction and prompts."""

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()


class UIHelper:
    """Handles user interface interactions and prompts."""
    
    def __init__(self, file_selector):
        self.file_selector = file_selector
    
    def show_crud_menu(self):
        """Display CRUD menu for file operations."""
        choices = [
            Choice("create", "📝 Create - Generate new code"),
            Choice("read", "👀 Read - Display file content"),
            Choice("update", "✏️ Update - Modify existing code (Developing)"),
            Choice("delete", "🗑️ Delete - Remove file"),
            Choice("debug", "🔍 Inspect last error"),
            Choice("exit", "❌ Exit Coder")
        ]
        
        try:
            return inquirer.select(
                message="Select operation:",
                choices=choices,
                pointer="👉"
            ).execute()
        except KeyboardInterrupt:
            return "exit"
    
    def get_codebase_reference(self):
        """Handle codebase reference selection with skip option."""
        codebase_input = input("Reference existing codebase? (y/N): ").strip().lower()
        has_codebase = codebase_input == 'y'
        
        code_contexts = {}
        if has_codebase:
            while True:
                codebase_path = inquirer.text(
                    message="Enter codebase folder path (or press Enter to skip):",
                    validate=lambda x: True  # Allow empty input
                ).execute()
                
                # If empty input, skip codebase
                if not codebase_path.strip():
                    print("⏭️ Skipping codebase reference")
                    break
                
                code_contexts = self.file_selector.select_reference_files(codebase_path)
                
                # If no contexts returned due to errors, let user choose
                if not code_contexts:
                    choice = inquirer.select(
                        message="No files could be loaded. Choose action:",
                        choices=[
                            Choice("details", "🔍 Show error details"),
                            Choice("retry", "🔄 Try different path"),
                            Choice("skip", "⏭️ Continue without codebase"),
                            Choice("cancel", "❌ Cancel operation")
                        ]
                    ).execute()
                    
                    if choice == "details":
                        self.file_selector.show_path_error_details(codebase_path)
                        continue  # Show menu again
                    elif choice == "retry":
                        continue  # Ask for path again
                    elif choice == "skip":
                        break  # Continue without codebase
                    else:  # cancel
                        return None
                else:
                    break  # Success, continue with contexts
        
        return code_contexts
    
    def get_task_description(self, operation):
        """Get task description from user."""
        return inquirer.text(
            message=f"What do you want to {operation}?",
            validate=lambda x: len(x.strip()) > 0
        ).execute()
    
    def get_output_method(self):
        """Get output method choice from user."""
        output_choice = inquirer.select(
            message="Output method:",
            choices=[
                Choice("1", "📺 Display in terminal"),
                Choice("2", "💾 Save to file")
            ],
            pointer="👉"
        ).execute()
        
        output_path = None
        if output_choice == "2":
            output_path = inquirer.text(
                message="File path to save:",
                validate=lambda x: len(x.strip()) > 0
            ).execute()
        
        return output_choice, output_path
    
    def handle_update_preview(self, target_file):
        """Handle update operation file preview."""
        file_path = Path(target_file)
        if not file_path.exists():
            file_path = Path.cwd() / target_file
        
        if file_path.exists():
            existing_content = file_path.read_text(encoding='utf-8')
            preview_content = existing_content[:500] + "..." if len(existing_content) > 500 else existing_content
            
            # Detect file type for syntax highlighting
            if file_path.suffix == '.py':
                lang = "python"
            elif file_path.suffix == '.md':
                lang = "markdown"
            else:
                lang = "text"
                
            syntax = Syntax(preview_content, lang, theme="monokai", line_numbers=True)
            console.print(Panel(syntax, title=f"📄 Current: {file_path.name}", border_style="yellow"))
            return existing_content
        else:
            print(f"⚠️ File not found: {target_file}. Will create new file.")
            return ""
    
    def get_update_target_file(self):
        """Get target file for update operation."""
        return inquirer.text(
            message="Enter filename to update:",
            validate=lambda x: len(x.strip()) > 0
        ).execute()