
import requests
import json
import sqlite3
from pathlib import Path
from datetime import datetime

BACKENDS = {
    "lmstudio": ("http://localhost:1234", "mistralai/mistral-small-3.2"),
    "ollama":   ("http://localhost:11434", "mistral-small3.2"),
}

def get_response(prompt, backend="ollama"):

    base_url, model = BACKENDS[backend]

    r = requests.post(f"{base_url}/v1/chat/completions", json={
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    })

    return r.json()["choices"][0]["message"]["content"]



##########################


#API_KEY = "ton-token-ici"
#headers = {"Authorization": f"Bearer {API_KEY}"}

def list_chats():
    headers = {"Authorization": "Bearer ton-token-ici"}
    response = requests.get("http://localhost:8080/api/v1/chats/", headers=headers)
    chats = response.json()
    return chats
    '''
    BASE_URL = "http://localhost:8080"
    API_KEY = "ton-token-ici"

    headers = {"Authorization": f"Bearer {API_KEY}"}
    chats = requests.get(f"{BASE_URL}/api/v1/chats/", headers=headers).json()

    for chat in chats:
        title = chat.get("title", "Sans titre")
        created_at = datetime.fromtimestamp(chat["created_at"])
        updated_at = datetime.fromtimestamp(chat["updated_at"])
        print(f"{title} | créé: {created_at:%Y-%m-%d %H:%M} | maj: {updated_at:%Y-%m-%d %H:%M}")
    '''


DB_PATH = Path.home() / "Library/Application Support/open-webui/data/webui.db"

def list_ollama_chats():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT id, title, created_at, updated_at FROM chat ORDER BY created_at DESC")

    chats = []
    for id, title, created_at, updated_at in cursor.fetchall():
        created = datetime.fromtimestamp(created_at)
        updated = datetime.fromtimestamp(updated_at)
        chats.append({
            "id": id,
            "title": title,
            "created": created,
            "updated": updated,
        })

    conn.close()
    chats.sort(key=lambda chat: chat["created"], reverse=True)
    
    return chats

def get_ollama_chat(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT chat FROM chat WHERE id = ?", (id,))
    chats = cursor.fetchall()
    data = json.loads(chats[0][0]) 
    conn.close()

    return data

##################################



CONVERSATIONS_DIR = Path.home() / ".lmstudio" / "conversations"

def list_lmstudio_chats():
    chats = []

    for filepath in CONVERSATIONS_DIR.glob("*.json"):
        with open(filepath) as f:
            data = json.load(f)

        title = data.get("name", "Sans titre")
        token_count = data["tokenCount"]
        created_at = datetime.fromtimestamp(data["createdAt"] / 1000)
        last_msg_at = datetime.fromtimestamp(data["assistantLastMessagedAt"] / 1000)

        chats.append({
            "title": title,
            "token_count": token_count,
            "created_at": created_at,
            "last_msg_at": last_msg_at,
            "id": filepath.name.split(".")[0],
        })
    
    chats.sort(key=lambda chat: chat["created_at"], reverse=True)
    return chats


def get_lmstudio_chat(id):
    filepath = CONVERSATIONS_DIR / f"{id}.conversation.json"
    data = None
    with open(filepath) as f:
        data = json.load(f)
    return data