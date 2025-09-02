"""LLM interaction and code generation handling."""

from pathlib import Path
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

console = Console()


class LLMHandler:
    """Handles LLM interaction, code generation, and file saving."""
    
    def __init__(self, model, system_prompt, error_handler):
        self.model = model
        self.system_prompt = system_prompt
        self.error_handler = error_handler
    
    def parse_python_codeblock(self, response: str) -> str:
        """Extract Python code from LLM response."""
        parsed = response.split("```python")[1]
        parsed = parsed.split("```")[0]
        return parsed.strip()
    
    def generate_code(self, task, code_contexts):
        """Generate code using LLM with error handling."""
        try:
            # Format code contexts properly
            text_parts = []
            
            if code_contexts:
                code_str = "\n\n".join([
                    f"FILENAME: {filename}:\n{context}" 
                    for filename, context in code_contexts.items()
                ])
                text_parts.append(f"CODEBASE (follow this codebase):\n\n{code_str}")
            
            text_parts.append(f"USER:\n\n{task}")
            text = "\n\n".join(text_parts)
            
            messages = [self.model.UserMessage(text=text)]
            
            print("🤖 Generating code with LLM...")
            response = self.model.run(
                system_prompt=self.system_prompt,
                messages=messages
            )
            
            generated_code = self.parse_python_codeblock(response)
            
            # Display generated code
            syntax = Syntax(generated_code, "python", theme="monokai", line_numbers=True)
            console.print(Panel(syntax, title="🚀 Generated Code", border_style="green"))
            
            return generated_code, response
            
        except Exception as e:
            self.error_handler.log_error("llm_generation", e, context="Code generation with LLM failed")
            print(f"❌ LLM Error: {e}")
            print(f"💡 Possible causes: Network issues, API limits, model unavailable")
            
            choice = inquirer.select(
                message="Choose action:",
                choices=[
                    Choice("retry", "🔄 Try again"),
                    Choice("skip", "⏭️ Skip this task"),
                    Choice("exit", "❌ Exit coder")
                ]
            ).execute()
            
            return None, choice
    
    def save_code_to_file(self, generated_code, output_path):
        """Save generated code to file with error handling."""
        try:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(generated_code, encoding='utf-8')
            print(f"✅ Code saved to {path}")
            return True
            
        except Exception as e:
            self.error_handler.log_error("save_file", e, str(output_path), "Failed to save generated code to file")
            print(f"❌ Error saving file: {e}")
            print(f"💡 Check permissions and disk space")
            
            choice = inquirer.select(
                message="Choose action:",
                choices=[
                    Choice("retry", "🔄 Try saving again"),
                    Choice("different", "📁 Save to different path"),
                    Choice("skip", "⏭️ Skip saving (code shown above)")
                ]
            ).execute()
            
            if choice == "retry":
                try:
                    path.write_text(generated_code, encoding='utf-8')
                    print(f"✅ Code saved to {path}")
                    return True
                except Exception as retry_e:
                    print(f"❌ Still failed: {retry_e}")
                    return False
                    
            elif choice == "different":
                new_path = inquirer.text(
                    message="Enter new file path:",
                    validate=lambda x: len(x.strip()) > 0
                ).execute()
                return self.save_code_to_file(generated_code, new_path)
            
            return False
    
    def offer_clipboard_copy(self, generated_code):
        """Offer to copy generated code to clipboard."""
        if CLIPBOARD_AVAILABLE:
            try:
                copy_choice = inquirer.confirm(
                    message="Copy to clipboard?",
                    default=False
                ).execute()
                
                if copy_choice:
                    pyperclip.copy(generated_code)
                    print("✅ Code copied to clipboard!")
            except Exception as e:
                print(f"❌ Failed to copy to clipboard: {e}")
                print(f"💡 Clipboard functionality unavailable")