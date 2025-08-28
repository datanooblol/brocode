from broflow import Action
from pydantic import BaseModel, Field
from typing import Any, Optional, List, Dict

class Shared(BaseModel):
    user_input:Optional[str] = None
    code_message:Optional[str] = None
    code_contexts:Optional[List[str]] = None
    response:Optional[Any] = None
    chat_messages:List[Dict[str, Any]] = Field(default_factory=list)