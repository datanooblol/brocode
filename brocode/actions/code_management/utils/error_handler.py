"""Error handling and debugging functionality."""

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import traceback


class ErrorHandler:
    """Handles error logging, inspection, and user error choices."""
    
    def __init__(self):
        self.last_error = None
    
    def log_error(self, operation, error, file_path=None, context=None):
        """Log error for later inspection."""
        self.last_error = {
            'operation': operation,
            'error_type': type(error).__name__,
            'message': str(error),
            'file_path': file_path,
            'context': context,
            'stack_trace': traceback.format_exc()
        }
    
    def inspect_last_error(self):
        """Inspect the last error that occurred."""
        if not self.last_error:
            print("📋 No recent errors to inspect")
            return
        
        error_info = self.last_error
        print(f"\n🔍 LATEST ERROR INSPECTION")
        print(f"Operation: {error_info.get('operation', 'Unknown')}")
        print(f"Error Type: {error_info.get('error_type', 'Unknown')}")
        print(f"Error Message: {error_info.get('message', 'No message')}")
        
        if error_info.get('file_path'):
            print(f"File: {error_info['file_path']}")
        
        if error_info.get('context'):
            print(f"Context: {error_info['context']}")
        
        if error_info.get('stack_trace'):
            show_trace = inquirer.confirm(
                message="Show full stack trace?",
                default=False
            ).execute()
            if show_trace:
                print(f"\nStack Trace:\n{error_info['stack_trace']}")
        
        input("\nPress Enter to continue...")
    
    def show_detailed_error(self, error, file_path=None):
        """Show detailed error information."""
        print(f"\n🔍 Detailed Error Information:")
        if file_path:
            print(f"File: {file_path}")
        print(f"Error type: {type(error).__name__}")
        print(f"Error message: {str(error)}")
        
        if file_path:
            from pathlib import Path
            path = Path(file_path)
            print(f"File exists: {path.exists()}")
            if path.exists():
                print(f"File size: {path.stat().st_size} bytes")
                print(f"File permissions: {oct(path.stat().st_mode)[-3:]}")
                if hasattr(path, 'is_dir'):
                    print(f"Is directory: {path.is_dir()}")
        
        input("\nPress Enter to continue...")
    
    def handle_error_choice(self, error, operation, file_path=None, extra_choices=None):
        """Handle user choice when error occurs."""
        self.log_error(operation, error, file_path, f"Error during {operation}")
        
        choices = [
            Choice("details", "🔍 Show detailed error"),
            Choice("retry", "🔄 Try again"),
            Choice("cancel", "❌ Cancel operation")
        ]
        
        if extra_choices:
            choices = extra_choices + choices[1:]  # Keep details first, add extra before retry/cancel
        
        choice = inquirer.select(
            message="Choose action:",
            choices=choices
        ).execute()
        
        if choice == "details":
            self.show_detailed_error(error, file_path)
            return "details_shown"
        
        return choice