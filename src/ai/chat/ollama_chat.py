import ollama

def get_response(message:str) -> str:

    response = ollama.chat(
        model="mistral-small3.2", #qwen3.6:35b-mlx
        messages=[{"role": "user", "content": message}]
    )

    return response['message']['content']
