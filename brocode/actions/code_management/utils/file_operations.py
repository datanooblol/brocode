"""File CRUD operations with error handling."""

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


class FileOperations:
    """Handles file CRUD operations with comprehensive error handling."""
    
    def __init__(self, error_handler):
        self.error_handler = error_handler
    
    def detect_file_language(self, file_path):
        """Detect programming language from file extension."""
        suffix = Path(file_path).suffix
        if suffix == '.py':
            return "python", "📄"
        elif suffix == '.md':
            return "markdown", "📝"
        else:
            return "text", "📄"
    
    def handle_read(self):
        """Handle read operation with retry logic."""
        while True:
            try:
                file_path = inquirer.text(
                    message="Enter file path to read:",
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
                            Choice("cancel", "❌ Cancel read operation")
                        ]
                    ).execute()
                    if choice == "cancel":
                        return
                    continue
                
                try:
                    content = path.read_text(encoding='utf-8')
                except Exception as e:
                    choice = self.error_handler.handle_error_choice(
                        e, "read_file", str(path),
                        [Choice("different", "📁 Try different file")]
                    )
                    
                    if choice == "cancel":
                        return
                    elif choice == "different":
                        continue
                    elif choice == "retry":
                        try:
                            content = path.read_text(encoding='utf-8')
                        except Exception as retry_e:
                            print(f"❌ Still failed: {retry_e}")
                            continue
                    elif choice == "details_shown":
                        continue
                
                # Display file content
                lang, icon = self.detect_file_language(path)
                syntax = Syntax(content, lang, theme="monokai", line_numbers=True)
                console.print(Panel(syntax, title=f"{icon} {path.name}", border_style="blue"))
                
                # Clipboard copy option
                if CLIPBOARD_AVAILABLE:
                    try:
                        copy_choice = inquirer.confirm(
                            message="Copy to clipboard?",
                            default=False
                        ).execute()
                        
                        if copy_choice:
                            pyperclip.copy(content)
                            print("✅ Code copied to clipboard!")
                    except Exception as e:
                        print(f"❌ Failed to copy to clipboard: {e}")
                        print(f"💡 Clipboard functionality unavailable")
                
                return  # Success
                
            except KeyboardInterrupt:
                print("\nRead cancelled")
                return
            except Exception as e:
                choice = self.error_handler.handle_error_choice(e, "read_operation")
                if choice == "cancel":
                    return
                elif choice == "details_shown":
                    continue
    
    def handle_delete(self):
        """Handle delete operation with confirmation."""
        while True:
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
                    choice = inquirer.select(
                        message="Choose action:",
                        choices=[
                            Choice("retry", "🔄 Try different path"),
                            Choice("cancel", "❌ Cancel delete operation")
                        ]
                    ).execute()
                    if choice == "cancel":
                        return
                    continue
                
                try:
                    confirm_name = inquirer.text(
                        message=f"Type filename '{path.name}' to confirm delete:",
                        validate=lambda x: x == path.name
                    ).execute()
                    
                    path.unlink()
                    print(f"✅ File deleted: {path}")
                    return  # Success
                    
                except PermissionError as e:
                    choice = self.error_handler.handle_error_choice(
                        e, "delete_file", str(path),
                        [Choice("different", "📁 Try different file")]
                    )
                    if choice == "cancel":
                        return
                    elif choice == "different":
                        continue
                    elif choice == "details_shown":
                        continue
                        
                except Exception as e:
                    choice = self.error_handler.handle_error_choice(e, "delete_file", str(path))
                    if choice == "cancel":
                        return
                    elif choice == "details_shown":
                        continue
                
            except KeyboardInterrupt:
                print("\nDelete cancelled")
                return