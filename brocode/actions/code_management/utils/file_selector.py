"""File selection and codebase reference functionality."""

from pathlib import Path
from InquirerPy import inquirer
from InquirerPy.base.control import Choice


class FileSelector:
    """Handles file discovery, selection, and codebase reference building."""
    
    def __init__(self, context_builder, error_handler):
        self.builder = context_builder
        self.error_handler = error_handler
    
    def discover_supported_files(self, path):
        """Discover all supported files in a directory."""
        py_files = list(path.rglob("*.py"))
        md_files = list(path.rglob("*.md"))
        return py_files + md_files, py_files, md_files
    
    def show_path_error_details(self, codebase_path):
        """Show detailed error information for path issues."""
        print(f"\n🔍 Detailed Error Information:")
        print(f"Path attempted: {codebase_path}")
        
        path = Path(codebase_path)
        if not path.exists():
            path = Path.cwd() / codebase_path
        
        if not path.exists():
            print(f"❌ Path does not exist: {path.absolute()}")
            print(f"💡 Current directory: {Path.cwd()}")
        elif not path.is_dir():
            print(f"❌ Path is not a directory: {path.absolute()}")
        else:
            py_files = list(path.rglob("*.py"))
            md_files = list(path.rglob("*.md"))
            print(f"📁 Directory exists: {path.absolute()}")
            print(f"   Python files found: {len(py_files)}")
            print(f"   Markdown files found: {len(md_files)}")
            if py_files or md_files:
                print(f"⚠️  Files found but processing failed")
        
        print(f"\n💡 Tip: Press Enter on next prompt to skip codebase")
        input("\nPress Enter to continue...")
    
    def select_files_from_list(self, supported_files, base_path):
        """Handle multi-select file selection."""
        choices = []
        for file in supported_files:
            rel_path = file.relative_to(base_path)
            icon = "📄" if file.suffix == ".py" else "📝"
            choices.append(Choice(str(file), f"{icon} {rel_path}"))
        
        choices.insert(0, Choice("__SELECT_ALL__", "✅ Select All"))
        
        selected_files = inquirer.checkbox(
            message="Select files to use as reference (Space to toggle, Enter to confirm):",
            choices=choices,
            pointer="👉",
            instruction="(Use arrow keys, Space to select/deselect)"
        ).execute()
        
        # Handle select-all
        if "__SELECT_ALL__" in selected_files:
            return [str(f) for f in supported_files]
        else:
            return [f for f in selected_files if not f.startswith("__")]
    
    def process_selected_files(self, selected_paths):
        """Process selected files and handle errors."""
        print(f"🔄 Processing {len(selected_paths)} selected files...")
        
        contexts = self.builder.build_contexts(selected_paths)
        
        # Show processing summary
        successful = sum(1 for v in contexts.values() if not v.startswith("ERROR:"))
        failed = len(contexts) - successful
        
        if failed > 0:
            print(f"⚠️  Processing summary: {successful} successful, {failed} failed")
            
            error_details = {}
            for file_path, context in contexts.items():
                if context.startswith("ERROR:"):
                    print(f"   ❌ {Path(file_path).name}: {context[:60]}...")
                    error_details[file_path] = context
            
            if successful == 0:
                print(f"❌ No files could be processed")
                
                if error_details:
                    show_details = inquirer.confirm(
                        message="Show detailed error information?",
                        default=False
                    ).execute()
                    
                    if show_details:
                        print(f"\n🔍 Detailed Error Information:")
                        for file_path, error in error_details.items():
                            print(f"\n--- {Path(file_path).name} ---")
                            print(error)
                        input("\nPress Enter to continue...")
                
                return {}
                
            elif successful < len(selected_paths):
                choices = [
                    Choice("continue", f"▶️ Continue with {successful} working files"),
                    Choice("details", "🔍 Show error details"),
                    Choice("cancel", "❌ Cancel operation")
                ]
                
                choice = inquirer.select(
                    message="Choose action:",
                    choices=choices
                ).execute()
                
                if choice == "details":
                    print(f"\n🔍 Detailed Error Information:")
                    for file_path, error in error_details.items():
                        print(f"\n--- {Path(file_path).name} ---")
                        print(error)
                    input("\nPress Enter to continue...")
                    
                    continue_choice = inquirer.confirm(
                        message=f"Continue with {successful} working files?",
                        default=True
                    ).execute()
                    if not continue_choice:
                        return {}
                elif choice == "cancel":
                    return {}
        else:
            print(f"✅ Successfully processed all {successful} files")
        
        return contexts
    
    def select_reference_files(self, codebase_path):
        """Main method to select reference files from codebase."""
        try:
            path = Path(codebase_path)
            
            if not path.exists():
                path = Path.cwd() / codebase_path
            
            if not path.exists():
                print(f"❌ Path not found: {codebase_path}")
                print(f"💡 Check if the path exists and is accessible")
                return {}
            
            if path.is_file():
                try:
                    return self.builder.build_contexts([path])
                except Exception as e:
                    print(f"❌ Error processing file {path.name}: {e}")
                    print(f"💡 File may be corrupted, binary, or have encoding issues")
                    return {}
            
            # Discover files
            print(f"🔍 Scanning {path} for supported files...")
            supported_files, py_files, md_files = self.discover_supported_files(path)
            
            print(f"   Found {len(py_files)} Python files")
            print(f"   Found {len(md_files)} Markdown files")
            
            if not supported_files:
                print(f"❌ No supported files (.py, .md) found in: {path}")
                print(f"💡 Try a different path or create some .py/.md files first")
                return {}
            
            # File selection
            selected_files = self.select_files_from_list(supported_files, path)
            
            if not selected_files:
                print("No files selected")
                return {}
            
            # Process selected files
            selected_paths = [Path(f) for f in selected_files]
            return self.process_selected_files(selected_paths)
            
        except KeyboardInterrupt:
            print("\nFile selection cancelled")
            return {}
        except Exception as e:
            self.error_handler.log_error("file_selection", e, codebase_path, "Unexpected error during file selection")
            print(f"❌ Unexpected error during file selection: {e}")
            show_details = inquirer.confirm(
                message="Show detailed error information?",
                default=False
            ).execute()
            
            if show_details:
                self.error_handler.show_detailed_error(e, codebase_path)
            
            return {}