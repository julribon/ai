
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

provider=OpenAIProvider(base_url='http://localhost:1234/v1')

model = OpenAIChatModel(
    'mistralai/mistral-small-3.2', 
    provider=provider
)

agent = Agent(model)

def ask(prompt):
    result = agent.run_sync(prompt)
    return result.output