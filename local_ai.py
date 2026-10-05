
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3.5:4b"


def ask_ai(prompt):
    print("Local AI is thinking... Please wait.")

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "think": False,
            "options": {
                "num_predict": 350,
                "temperature": 0.3
            }
        },
        timeout=(10, 600)
    )

    response.raise_for_status()

    data = response.json()
    return data["message"]["content"]