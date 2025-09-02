"""Code modifier for updating existing files."""

from pathlib import Path
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from brocode.actions import Action, Shared
from brollm import BaseLLM
from brocode.code_analysis import MultiScriptContextBuilder

# Import shared components from utils
from ..utils import ErrorHandler, FileSelector

console = Console()


class CodeModifier(Action):
    """Handles code modification and updates."""
    
    def __init__(self, system_prompt: str, model: BaseLLM):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model
        
        # Initialize shared components
        self.error_handler = ErrorHandler()
        self.context_builder = MultiScriptContextBuilder()
        self.file_selector = FileSelector(self.context_builder, self.error_handler)
    
    def get_target_file(self):
        """Get the file user wants to update."""
        while True:
            try:
                file_path = inquirer.text(
                    message="Enter file path to update:",
                    validate=lambda x: len(x.strip()) > 0
                ).execute()
                
                path = Path(file_path)
                if not path.exists():
                    path = Path.cwd() / file_path
                
                if not path.exists():
                    print(f"❌ File not found: {file_path}")
                    choice = inquirer.select(
                        message="Choose action:",
                        choices=[
                            Choice("retry", "🔄 Try different path"),
                            Choice("cancel", "❌ Cancel update")
                        ]
                    ).execute()
                    if choice == "cancel":
                        return None
                    continue
                
                # Show current file content
                try:
                    content = path.read_text(encoding='utf-8')
                    lang = "python" if path.suffix == '.py' else "markdown" if path.suffix == '.md' else "text"
                    icon = "📄" if path.suffix == '.py' else "📝" if path.suffix == '.md' else "📄"
                    
                    syntax = Syntax(content, lang, theme="monokai", line_numbers=True)
                    console.print(Panel(syntax, title=f"{icon} Current: {path.name}", border_style="blue"))
                    
                    return path, content
                    
                except Exception as e:
                    choice = self.error_handler.handle_error_choice(e, "read_target_file", str(path))
                    if choice == "cancel":
                        return None
                    elif choice == "details_shown":
                        continue
                    
            except KeyboardInterrupt:
                return None
    
    def get_update_request(self):
        """Get user's update/fix request."""
        return inquirer.text(
            message="What do you want to update or fix?",
            validate=lambda x: len(x.strip()) > 0
        ).execute()
    
    def get_codebase_reference(self):
        """Get optional codebase reference."""
        codebase_input = input("Reference existing codebase? (y/N): ").strip().lower()
        
        if codebase_input != 'y':
            return {}
        
        while True:
            codebase_path = inquirer.text(
                message="Enter codebase folder path (or press Enter to skip):",
                validate=lambda x: True
            ).execute()
            
            if not codebase_path.strip():
                print("⏭️ Skipping codebase reference")
                return {}
            
            code_contexts = self.file_selector.select_reference_files(codebase_path)
            
            if not code_contexts:
                choice = inquirer.select(
                    message="No files could be loaded. Choose action:",
                    choices=[
                        Choice("retry", "🔄 Try different path"),
                        Choice("skip", "⏭️ Continue without codebase"),
                        Choice("cancel", "❌ Cancel operation")
                    ]
                ).execute()
                
                if choice == "retry":
                    continue
                elif choice == "skip":
                    return {}
                else:
                    return None
            else:
                return code_contexts
    
    def generate_updated_code(self, original_content, update_request, code_contexts, file_path):
        """Generate updated code using LLM."""
        try:
            # Build prompt
            text_parts = []
            
            if code_contexts:
                code_str = "\n\n".join([
                    f"FILENAME: {filename}:\n{context}" 
                    for filename, context in code_contexts.items()
                ])
                text_parts.append(f"CODEBASE:\n\n{code_str}")
            
            text_parts.append(f"CURRENT_CODE:\n```python\n{original_content}\n```")
            text_parts.append(f"USER:\n\n{update_request}")
            
            text = "\n\n".join(text_parts)
            messages = [self.model.UserMessage(text=text)]
            
            print("🤖 Generating updated code...")
            response = self.model.run(
                system_prompt=self.system_prompt,
                messages=messages
            )
            
            # Extract code from response
            if "```python" in response:
                updated_code = response.split("```python")[1].split("```")[0].strip()
            elif "```" in response:
                updated_code = response.split("```")[1].split("```")[0].strip()
            else:
                updated_code = response.strip()
            
            return updated_code, response
            
        except Exception as e:
            self.error_handler.log_error("code_generation", e, str(file_path), "Failed to generate updated code")
            print(f"❌ LLM Error: {e}")
            print(f"💡 Possible causes: Network issues, API limits, model unavailable")
            return None, None
    
    def show_updated_code(self, updated_code, file_path):
        """Display the updated code for review."""
        lang = "python" if file_path.suffix == '.py' else "markdown" if file_path.suffix == '.md' else "text"
        syntax = Syntax(updated_code, lang, theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title="🚀 Updated Code", border_style="green"))
    
    def apply_update(self, file_path, updated_code):
        """Apply the update to the file."""
        try:
            file_path.write_text(updated_code, encoding='utf-8')
            print(f"✅ File updated: {file_path}")
            return True
            
        except Exception as e:
            self.error_handler.log_error("apply_update", e, str(file_path), "Failed to apply update")
            print(f"❌ Error updating file: {e}")
            return False
    
    def run(self, shared: Shared):
        """Main update workflow."""
        try:
            # Step 1: Get target file
            result = self.get_target_file()
            if result is None:
                return shared
            
            file_path, original_content = result
            
            # Step 2: Get update request
            update_request = self.get_update_request()
            
            # Step 3: Get codebase reference
            code_contexts = self.get_codebase_reference()
            if code_contexts is None:  # User cancelled
                return shared
            
            # Step 4: Generate updated code
            updated_code, response = self.generate_updated_code(
                original_content, update_request, code_contexts, file_path
            )
            
            if updated_code is None:
                choice = inquirer.select(
                    message="Code generation failed. Choose action:",
                    choices=[
                        Choice("retry", "🔄 Try again"),
                        Choice("exit", "❌ Exit updater")
                    ]
                ).execute()
                
                if choice == "retry":
                    return self.run(shared)  # Restart the process
                else:
                    return shared
            
            # Step 5: Show updated code
            self.show_updated_code(updated_code, file_path)
            
            # Step 6: Ask for confirmation
            accept = inquirer.confirm(
                message="Accept and apply this update?",
                default=False
            ).execute()
            
            if accept:
                success = self.apply_update(file_path, updated_code)
                if success:
                    shared.response = response
                    shared.code_contexts = code_contexts
            else:
                print("❌ Update rejected")
            
            return shared
            
        except KeyboardInterrupt:
            print("\nUpdate cancelled")
            return shared