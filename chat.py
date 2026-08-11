import json
from src.ai.chat import ollama_chat, lmstudio_chat, huggingface_chat, request_chat


prompt = "Quelle est la capitale de la France?"
#print(ollama_chat.get_response(prompt))
#print(lmstudio_chat.get_response(prompt))
print(request_chat.get_response(prompt, backend="ollama"))
print(request_chat.get_response(prompt, backend="lmstudio"))
#print(huggingface_chat.get_response(prompt))

print("\nChats Ollama (API):")
chats = request_chat.list_chats()
print(chats)

print("\nChats Ollama:")
chats = request_chat.list_ollama_chats()
for c in chats:
    print(f"id:{c['id']}, created:{c['created']:%Y-%m-%d %H:%M}, updated: {c['updated']:%Y-%m-%d %H:%M}, title:{c['title']}")

conversation = request_chat.get_ollama_chat("fe17b4fa-1180-4d8b-b05e-0ed2e440613e")
print(json.dumps(conversation, indent=2, ensure_ascii=False, default=str))

'''
print("\nChats LMStudio:")
chats = request_chat.list_lmstudio_chats()
#print(chats)
for c in chats:
    print(f"id:{c['id']}, created:{c['created_at']:%Y-%m-%d %H:%M}, updated: {c['last_msg_at']:%Y-%m-%d %H:%M}, title:{c['title']}")

conversation = request_chat.get_lmstudio_chat("1786433293794")
print(json.dumps(conversation, indent=2, ensure_ascii=False, default=str))
'''