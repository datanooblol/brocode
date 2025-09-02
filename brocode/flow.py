from broflow import Flow, Start, End
from brocode.actions.code_management import CodeAgent
from brocode.actions.code_management.code_generator import CodeGenerator
from brocode.actions.code_management.code_modifier import CodeModifier
from brocode.actions.user_input import UserInput
from brocode.actions.chat import Chat
from broprompt import Prompt
from pathlib import Path
from broflow import state

def get_flow(model):
    start_action = Start(message="Start Coding")
    end_action = End(message="End Coding")
    
    # Use prompt files from brosession
    prompt_hub_dir = Path.cwd() / "brosession" / "prompt_hub"
    code_prompt = Prompt.from_markdown(str(prompt_hub_dir / "code_generator.md")).str
    chat_prompt = Prompt.from_markdown(str(prompt_hub_dir / "chat.md")).str
    
    code_generator = CodeGenerator(
        system_prompt=code_prompt,
        model=model
    )
    code_modifier = CodeModifier(
        system_prompt=code_prompt,
        model=model
    )
    code_agent = CodeAgent(
        generator=code_generator,
        modifier=code_modifier
    )
    user_input_action = UserInput()
    chat_action = Chat(
        system_prompt=chat_prompt,
        model=model
    )
    start_action >> user_input_action
    user_input_action -"code">> code_agent
    code_agent >> user_input_action
    user_input_action >> chat_action
    chat_action >> user_input_action
    user_input_action -"exit">> end_action

    flow = Flow(start_action=start_action, name="BroCode")
    return flow