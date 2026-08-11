
from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

provider=OllamaProvider(base_url='http://localhost:11434/v1')
model = OllamaModel(
    'mistral-small3.2', 
    provider=provider
)

agent = Agent(model)

def ask(prompt):
    result = agent.run_sync(prompt)
    return result.output