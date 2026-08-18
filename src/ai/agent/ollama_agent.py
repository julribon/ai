from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

from ai.agent.ai_agent import AIAgent

BASE_URL = 'http://localhost:11434/v1'
MODEL_NAME = 'mistral-small3.2'

class OllamaAgent(AIAgent):

    def __init__(
            self, 
            base_url=BASE_URL, 
            model_name=MODEL_NAME, 
            system_prompt=''
    ):
        provider = OllamaProvider(base_url=base_url)
        model = OllamaModel(model_name, provider=provider)

        self.agent = Agent(model, system_prompt=system_prompt)
        self.messages = [] # mémoire

