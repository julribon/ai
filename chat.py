from src.ai.chat import ollama_chat, lmstudio_chat, huggingface_chat, request_chat


prompt = "Quelle est la capitale de la France?"
print(ollama_chat.get_response(prompt))
print(lmstudio_chat.get_response(prompt))
print(request_chat.get_response(prompt, backend="ollama"))
print(request_chat.get_response(prompt, backend="lmstudio"))

print(huggingface_chat.get_response(prompt))

