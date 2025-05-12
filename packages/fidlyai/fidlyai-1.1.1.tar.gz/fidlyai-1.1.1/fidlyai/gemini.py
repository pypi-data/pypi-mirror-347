import requests

class gemini:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}"
        self.headers = {"Content-Type": "application/json"}
        self.user_chats = {}

    def ask(self, prompt: str) -> str:
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            return "Unexpected response format."
        except requests.exceptions.RequestException as e:
            return f"HTTP error occurred: {e}"

    def bulk_ask(self, prompts: list) -> list:
        results = []
        for prompt in prompts:
            results.append(self.ask(prompt))
        return results

    def chat(self, user_id: str, prompt: str) -> str:
        history = self.user_chats.get(user_id, [])
        history.append({"role": "user", "text": prompt})
        parts = [{"text": entry["text"]} for entry in history if entry["role"] == "user"]
        payload = {"contents": [{"parts": parts}]}
        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            reply = data['candidates'][0]['content']['parts'][0]['text']
            history.append({"role": "bot", "text": reply})
            self.user_chats[user_id] = history
            return reply
        except (KeyError, IndexError):
            return "Unexpected response format."
        except requests.exceptions.RequestException as e:
            return f"HTTP error occurred: {e}"
