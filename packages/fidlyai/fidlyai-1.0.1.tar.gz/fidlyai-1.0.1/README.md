# 💬 fidlyai

**fidlyai** is a powerful and flexible Python package for interacting with Google's Gemini 2.0 Flash API. Built to support multiple users, handle bulk prompts, and maintain chat memory per user, it's the perfect AI companion for developers, researchers, and builders.

---

## ✨ Features

- 🔐 Support for multiple API keys (multi-user ready)
- 💬 Chat-like session handling with memory per user
- 📤 Send and process multiple prompts in one go
- ⚡ Fast single-prompt requests
- 📦 Lightweight with zero dependencies except `requests`
- 🧩 Easy integration into any Python project
- 💡 Great for AI chatbots, automation, assistants, and research

---

## 📦 Installation

Install directly from GitHub:

```bash
pip install fidlyai
```

---

## 💡 Basic Usage

```python
from fidlyai import gemini

api = gemini("YOUR_GEMINI_API_KEY")
response = api.ask("What is Artificial Intelligence?")
print(response)
```

---

## 🔁 Bulk Prompting

Send multiple prompts in a single session:

```python
prompts = ["What is AI?", "Explain Python.", "Uses of the internet."]
answers = api.bulk_ask(prompts)

for ans in answers:
    print(ans)
```

---

## 👥 Chat with User Memory

Each user gets isolated memory context:

```python
user = "user123"
print(api.chat(user, "Hey Gemini, who are you?"))
print(api.chat(user, "What did I just ask you?"))
```

This creates a memory-like flow for each user separately — ideal for chatbots or interactive tools.

---

## 🔑 Authentication

To use fidlyai, you need a Gemini API key:

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a project
3. Get your Gemini 2.0 Flash API key
4. Use it like: `gemini("YOUR_KEY")`

---

## 🧪 Use Cases

- AI-powered chat systems
- Educational tools
- Creative writing assistants
- Code generators
- Research projects
- Interactive Q&A bots
- Multi-user systems with context retention

---

## 🧑‍💻 Author

Developed with ❤️ by [Fidal PalamParambil (mr-fidal)](https://github.com/mr-fidal)  
Email: `mrfidal@proton.me`

---

## 📃 License

MIT License © 2025 Fidal

---