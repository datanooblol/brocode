"""Lightweight diff viewer for code modifications."""

import difflib
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

class DiffViewer:
    """Simple diff viewer with full file highlighting."""
    
    @staticmethod
    def show_diff(original_content: str, modified_content: str, filename: str):
        """Show full file with highlighted changes."""
        original_lines = original_content.splitlines()
        modified_lines = modified_content.splitlines()
        
        if original_lines == modified_lines:
            console.print("📄 No changes detected", style="yellow")
            return
        
        # Get line-by-line diff operations
        differ = difflib.SequenceMatcher(None, original_lines, modified_lines)
        
        # Build Rich Text with colored lines
        text = Text()
        line_num = 1
        additions = 0
        deletions = 0
        
        for tag, i1, i2, j1, j2 in differ.get_opcodes():
            if tag == 'equal':
                # Unchanged lines
                for line in modified_lines[j1:j2]:
                    text.append(f"{line_num:4d}  ", style="dim")
                    text.append(f"{line}\n")
                    line_num += 1
            elif tag == 'delete':
                # Deleted lines (red)
                for line in original_lines[i1:i2]:
                    text.append(f"{line_num:4d}- ", style="dim")
                    text.append(f"{line}\n", style="red")
                    line_num += 1
                    deletions += 1
            elif tag == 'insert':
                # Added lines (green)
                for line in modified_lines[j1:j2]:
                    text.append(f"{line_num:4d}+ ", style="dim")
                    text.append(f"{line}\n", style="green")
                    line_num += 1
                    additions += 1
            elif tag == 'replace':
                # Changed lines (show old as red, new as green)
                for line in original_lines[i1:i2]:
                    text.append(f"{line_num:4d}- ", style="dim")
                    text.append(f"{line}\n", style="red")
                    line_num += 1
                    deletions += 1
                for line in modified_lines[j1:j2]:
                    text.append(f"{line_num:4d}+ ", style="dim")
                    text.append(f"{line}\n", style="green")
                    line_num += 1
                    additions += 1
        
        # Display in panel
        console.print(Panel(text, title=f"🔄 Changes: {filename}", border_style="green"))
        console.print(f"📊 Summary: {deletions} deletions, {additions} additions", style="bold")