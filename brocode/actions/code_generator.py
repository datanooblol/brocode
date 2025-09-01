from . import Action, Shared
from brollm import BaseLLM
from brocode.code_analysis import MultiScriptContextBuilder
from pathlib import Path
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
# from broprompt import parse_codeblock_to_dict

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

console = Console()

class CodeGenerator(Action):
    def __init__(self, system_prompt:str, model:BaseLLM):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model
        self.builder = MultiScriptContextBuilder()

    def crud_menu(self):
        """Display CRUD menu for file operations."""
        choices = [
            Choice("create", "📝 Create - Generate new code"),
            Choice("read", "👀 Read - Display file content"),
            Choice("update", "✏️ Update - Modify existing code (Developing)"),
            Choice("delete", "🗑️ Delete - Remove file"),
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
    
    def handle_create_update(self, operation):
        """Handle create or update operations."""
        try:
            # For update, ask for filename first
            target_file = None
            if operation == "update":
                target_file = inquirer.text(
                    message="Enter filename to update:",
                    validate=lambda x: len(x.strip()) > 0
                ).execute()
                
                # Load existing file content
                file_path = Path(target_file)
                if not file_path.exists():
                    file_path = Path.cwd() / target_file
                
                if file_path.exists():
                    existing_content = file_path.read_text(encoding='utf-8')
                    preview_content = existing_content[:500] + "..." if len(existing_content) > 500 else existing_content
                    syntax = Syntax(preview_content, "python", theme="monokai", line_numbers=True)
                    console.print(Panel(syntax, title=f"📄 Current: {file_path.name}", border_style="yellow"))
                else:
                    print(f"⚠️ File not found: {target_file}. Will create new file.")
                    existing_content = ""
            
            task = inquirer.text(
                message=f"What do you want to {operation}?",
                validate=lambda x: len(x.strip()) > 0
            ).execute()
            
            # Ask for codebase reference with y/n input
            codebase_input = input("Reference existing codebase? (y/N): ").strip().lower()
            has_codebase = codebase_input == 'y'
            
            code_contexts = {}
            if has_codebase:
                codebase_path = inquirer.text(
                    message="Enter codebase folder path:",
                    validate=lambda x: len(x.strip()) > 0
                ).execute()
                code_contexts = self.select_reference_files(codebase_path)
            
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
            
            result = {
                'operation': operation,
                'task': task,
                'code_contexts': code_contexts,
                'return_type': output_choice,
                'output_path': output_path
            }
            
            # Add existing content for update operations
            if operation == "update" and target_file:
                result['target_file'] = target_file
                result['existing_content'] = existing_content if 'existing_content' in locals() else ""
            
            return result
        except KeyboardInterrupt:
            return None
    
    def handle_read(self):
        """Handle read operation."""
        try:
            file_path = inquirer.text(
                message="Enter file path to read:",
                validate=lambda x: len(x.strip()) > 0
            ).execute()
            
            path = Path(file_path)
            if not path.exists():
                path = Path.cwd() / file_path
            
            if path.exists():
                content = path.read_text(encoding='utf-8')
                syntax = Syntax(content, "python", theme="monokai", line_numbers=True)
                console.print(Panel(syntax, title=f"📄 {path.name}", border_style="blue"))
                
                # Ask if user wants to copy to clipboard (only if available)
                if CLIPBOARD_AVAILABLE:
                    copy_choice = inquirer.confirm(
                        message="Copy to clipboard?",
                        default=False
                    ).execute()
                    
                    if copy_choice:
                        try:
                            pyperclip.copy(content)
                            print("✅ Code copied to clipboard!")
                        except Exception as e:
                            print(f"❌ Failed to copy to clipboard: {e}")
            else:
                print(f"❌ File not found: {file_path}")
                
        except KeyboardInterrupt:
            print("\nRead cancelled")
        except Exception as e:
            print(f"❌ Error reading file: {e}")
    
    def handle_delete(self):
        """Handle delete operation."""
        try:
            file_path = inquirer.text(
                message="Enter file path to delete:",
                validate=lambda x: len(x.strip()) > 0
            ).execute()
            
            path = Path(file_path)
            if not path.exists():
                path = Path.cwd() / file_path
            
            if not path.exists():
                print(f"❌ File not found: {file_path}")
                return
            
            confirm_name = inquirer.text(
                message=f"Type filename '{path.name}' to confirm delete:",
                validate=lambda x: x == path.name
            ).execute()
            
            path.unlink()
            print(f"✅ File deleted: {path}")
            
        except KeyboardInterrupt:
            print("\nDelete cancelled")
        except Exception as e:
            print(f"❌ Error deleting file: {e}")
    
    def select_reference_files(self, codebase_path):
        """Select reference files from codebase folder."""
        try:
            path = Path(codebase_path)
            
            if not path.exists():
                path = Path.cwd() / codebase_path
            
            if not path.exists():
                print(f"❌ Path not found: {codebase_path}")
                return {}
            
            if path.is_file():
                return self.builder.build_contexts([path])
            
            # Get all Python files in the folder
            py_files = list(path.rglob("*.py"))
            if not py_files:
                print(f"❌ No Python files found in: {path}")
                return {}
            
            # Create choices for multi-select
            choices = []
            for py_file in py_files:
                rel_path = py_file.relative_to(path)
                choices.append(Choice(str(py_file), f"📄 {rel_path}"))
            
            # Add select-all option at the top
            choices.insert(0, Choice("__SELECT_ALL__", "✅ Select All"))
            
            selected_files = inquirer.checkbox(
                message="Select files to use as reference (Space to toggle, Enter to confirm):",
                choices=choices,
                pointer="👉",
                instruction="(Use arrow keys, Space to select/deselect)"
            ).execute()
            
            # Handle select-all
            if "__SELECT_ALL__" in selected_files:
                selected_files = [str(f) for f in py_files]
            else:
                # Filter out control options
                selected_files = [f for f in selected_files if not f.startswith("__")]
            
            if not selected_files:
                print("No files selected")
                return {}
            
            # Convert to Path objects and build contexts
            selected_paths = [Path(f) for f in selected_files]
            return self.builder.build_contexts(selected_paths)
            
        except KeyboardInterrupt:
            print("\nFile selection cancelled")
            return {}

        

    def parse_python_codeblock(self, response:str)->str:
        parsed = response.split("```python")[1]
        parsed = parsed.split("```")[0]
        return parsed.strip()

    def run(self, shared:Shared):
        while True:
            crud_choice = self.crud_menu()
            if crud_choice is None or crud_choice == "exit":
                break
            
            if crud_choice == "create":
                return_input = self.handle_create_update(crud_choice)
                if return_input is not None:
                    # Format code contexts properly
                    text_parts = []
                    
                    if return_input['code_contexts']:
                        code_str = "\n\n".join([
                            f"FILENAME: {filename}:\n{context}" 
                            for filename, context in return_input['code_contexts'].items()
                        ])
                        text_parts.append(f"CODEBASE (follow this codebase):\n\n{code_str}")
                    
                    text_parts.append(f"USER:\n\n{return_input['task']}")
                    text = "\n\n".join(text_parts)
                    
                    messages = [self.model.UserMessage(text=text)]
                    response = self.model.run(
                        system_prompt=self.system_prompt,
                        messages=messages
                    )
                    generated_code = self.parse_python_codeblock(response)
                    shared.response = response
                    shared.code_contexts = return_input['code_contexts']
                    
                    # Always display generated code first
                    syntax = Syntax(generated_code, "python", theme="monokai", line_numbers=True)
                    console.print(Panel(syntax, title="🚀 Generated Code", border_style="green"))
                    
                    # Save to file if requested
                    if return_input['return_type'] == "2" and return_input['output_path']:
                        output_path = Path(return_input['output_path'])
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        output_path.write_text(generated_code, encoding='utf-8')
                        print(f"✅ Code saved to {output_path}")
                    
                    # Offer clipboard copy if available
                    if CLIPBOARD_AVAILABLE:
                        copy_choice = inquirer.confirm(
                            message="Copy to clipboard?",
                            default=False
                        ).execute()
                        
                        if copy_choice:
                            try:
                                pyperclip.copy(generated_code)
                                print("✅ Code copied to clipboard!")
                            except Exception as e:
                                print(f"❌ Failed to copy to clipboard: {e}")
                    
            elif crud_choice == "update":
                print("📊 Update feature is under development. Coming in next release!")
                
            elif crud_choice == "read":
                self.handle_read()
                
            elif crud_choice == "delete":
                self.handle_delete()
        
        return shared