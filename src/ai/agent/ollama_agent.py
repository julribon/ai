
from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

class OllamaAgent():
    def __init__(self, base_url='http://localhost:11434/v1', model_name='mistral-small3.2', system_prompt=''):
        provider = OllamaProvider(base_url=base_url)
        model = OllamaModel(model_name, provider=provider)
        self.agent = Agent(model, system_prompt=system_prompt)
        self.messages = [] # mémoire


    def ask(self, user_prompt):
        #print(f'User: {user_prompt}')

        result = self.agent.run_sync(user_prompt, message_history=self.messages)
        response = result.output

        # Update whole history for next user prompt
        self.messages = result.all_messages()


        print(f'Agent: {response}')
        return response


    def reset(self):
        """Efface la mémoire de conversation (utile pour repartir sur une nouvelle discussion)."""
        self.messages = []