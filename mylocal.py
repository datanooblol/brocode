# mylocal.py
from brollm import BaseLLM, BedrockChat
from brocode.register import register_llm
import requests
from typing import Dict, Any

@register_llm("llama3.2-11b")
class MyLocalLLM(BedrockChat):
    def __init__(self):
        super().__init__(model_name="us.meta.llama3-2-11b-instruct-v1:0")


@register_llm("local-gpt")
class LocalLLM(BaseLLM):
    def __init__(self):
        self.model_name = "gpt-oss:latest"
        self.base_url = "http://localhost:11434"
        self.temperature = 0.8

    def UserMessage(self, text: str, **kwargs) -> Dict[str, Any]:
        return {"role": "user", "content": text}

    def AIMessage(self, text: str) -> Dict[str, Any]:
        return {"role": "assistant", "content": text}

    def SystemMessage(self, text: str) -> Dict[str, Any]:
        return {"role": "system", "content": text}    
    
    def run(self, system_prompt:str, messages:list[dict])->str:
        all_messages = [self.SystemMessage(system_prompt)] + messages
        response = requests.post(
            "{base_url}/api/chat".format(base_url=self.base_url), 
            json={
                "model": self.model_name,
                "messages": all_messages,
                "stream": False,
                "options": {"temperature": self.temperature}
            }
        )
        return response.json()['message']['content']