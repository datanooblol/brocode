from broflow import Flow, Start, End
from brocode.actions.code_generator import CodeGenerator
from brocode.actions.user_input import UserInput
from brocode.actions.chat import Chat
from broprompt import Prompt

def get_flow(model):
    start_action = Start(message="Start Coding")
    end_action = End(message="End Coding")
    code_generator = CodeGenerator(
        system_prompt=Prompt.from_markdown("./prompt_hub/code_generator.md").str,
        model=model
    )
    user_input_action = UserInput()
    chat_action = Chat(
        system_prompt=Prompt.from_markdown("./prompt_hub/chat.md").str,
        model=model
    )
    start_action >> user_input_action
    user_input_action -"code">> code_generator
    code_generator >> user_input_action
    user_input_action >> chat_action
    chat_action >> user_input_action
    user_input_action -"exit">> end_action

    flow = Flow(start_action=start_action, name="BroCode")
    return flow