import requests

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
