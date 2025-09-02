"""Main code agent that wraps generation and modification operations."""

from brocode.actions import Action, Shared
from brollm import BaseLLM
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

class CodeAgent(Action):
    """Main wrapper agent for code generation and modification operations."""
    
    def __init__(self, generator, modifier):
        super().__init__()
        self.generator = generator
        self.modifier = modifier
    
    def show_main_menu(self):
        """Display main code agent menu."""
        choices = [
            Choice("generate", "🚀 Generate - Create new code"),
            Choice("modify", "✏️ Modify - Update existing code"),
            Choice("exit", "❌ Exit Code Agent")
        ]
        
        try:
            return inquirer.select(
                message="Select code operation:",
                choices=choices,
                pointer="👉"
            ).execute()
        except KeyboardInterrupt:
            return "exit"
    
    def generate_code(self, shared: Shared) -> Shared:
        """Handle code generation operations."""
        return self.generator.run(shared)
    
    def modify_code(self, shared: Shared) -> Shared:
        """Handle code modification operations."""
        return self.modifier.run(shared)
    
    def run(self, shared: Shared) -> Shared:
        """Main run function that orchestrates code operations."""
        while True:
            choice = self.show_main_menu()
            if choice is None or choice == "exit":
                break
            
            if choice == "generate":
                shared = self.generate_code(shared)
            elif choice == "modify":
                shared = self.modify_code(shared)
        
        return shared