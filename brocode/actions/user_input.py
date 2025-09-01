from . import Shared, Action
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

class UserInput(Action):
    def logic(self, user_input:str):
        if user_input.startswith("/exit"):
            return "exit"
        if user_input.startswith("/agents"):
            return self.agents_menu()
        return "default"
    
    def agents_menu(self):
        """Display agents menu with interactive selection."""
        choices = [
            Choice("code", "🤖 Coder - Generate and analyze code"),
            Choice("analyst", "📊 Analyst - Data analysis (Coming in next release)")
        ]
        
        try:
            result = inquirer.select(
                message="Select an agent:",
                choices=choices,
                pointer="👉"
            ).execute()
            
            if result == "analyst":
                print("📊 Analyst agent is under development. Coming in next release!")
                return "default"
            return result
        except KeyboardInterrupt:
            return "default"
    
    def run(self, shared:Shared):
        while True:
            user_input = input("YOU: ")
            if user_input.startswith("/clear"):
                shared.chat_messages = []
                user_input = None
            if user_input:
                break
        self.next_action = self.logic(user_input.lower())
        shared.user_input = user_input
        return shared