from . import Shared, Action
from brollm import BaseLLM

class Chat(Action):
    def __init__(self, system_prompt, model:BaseLLM):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model

    def run(self, shared:Shared):
        messages = shared.chat_messages
        messages.append(
            self.model.UserMessage(text=shared.user_input)
        )
        response = self.model.run(
            system_prompt=self.system_prompt,
            messages=messages
        )
        messages.append(
            self.model.AIMessage(text=response)
        )
        print("AI:", response)
        return shared