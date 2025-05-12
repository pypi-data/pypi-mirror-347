from typing import Optional

from pydantic import BaseModel


class NPCUserConfig(BaseModel):
    model_name: str
    openai_api_key: str
    max_interaction_turn: Optional[int] = 5
    api_base_url: Optional[str] = 'https://api.openai.com/v1/chat/completions'
