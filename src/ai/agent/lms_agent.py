from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from ai.agent.ai_agent import AIAgent

BASE_URL = 'http://localhost:1234/v1'
MODEL_NAME = 'mistralai/mistral-small-3.2'

class LMSAgent(AIAgent):

    def __init__(
            self,
            base_url=BASE_URL, 
            model_name=MODEL_NAME,
            system_prompt=''
    ):
        provider = OpenAIProvider(base_url=base_url)
        model = OpenAIChatModel(model_name, provider=provider)
        
        self.agent = Agent(model, system_prompt=system_prompt)
        self.messages = [] # mémoire
