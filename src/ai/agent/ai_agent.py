
class AIAgent():

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

