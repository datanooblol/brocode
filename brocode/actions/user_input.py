from . import Shared, Action

class UserInput(Action):
    def logic(self, user_input:str):
        if user_input.startswith("/exit"):
            return "exit"
        if user_input.startswith("/code"):
            return "code"
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