# TaskoraApi

---

```markdown
# taskoraapi Package

A modular Python library offering clients for chatbot interactions, Instagram APIs, quiz services, and reCAPTCHA v3 solving.

## 📦 Features

- **chatBot**: A customizable chatbot client for interacting with various AI services.
- **InstagramApi**: Asynchronous and synchronous clients to access Instagram-related APIs.
- **QuizApi**: Clients to fetch quizzes using different HTTP libraries.
- **reCaptchaV3Solver**: A client to interact with reCAPTCHA v3 solving services.

## 🛠️ Installation

```bash

pip install TaskoraApi

```

## 🧰 Modules & Usage

### 🔹 chatBot

```python
from TaskoraApi import AiohttpChatbotAPI

async def run_aiohttp():
    client = AiohttpChatbotAPI(apikey="your_api_key")
    response = await client.chatbot("Hello!")
    print("Bot:", response)
    await client.close()

```

### 🔹 InstagramApi

```python

from TaskoraApi import AiohttpInstagramAPI

async def run_aiohttp_example():
    client = AiohttpInstagramAPI(apikey="your_api_key")
    response = await client.get_profile("instagram_username")
    print("AiohttpClient response:", response)
    await client.close()

```

### 🔹 QuizApi

```python

from TaskoraApi import AiohttpClient

async def run_aiohttp_example():
    client = AiohttpClient(apikey="your_api_key")
    response = await client.get_random_quiz()
    print("AiohttpClient response:", response)
    await client.close()

```

### 🔹 reCaptchaV3Solver

```python

from TaskoraApi import AiohttpreChaptchaAPI


def main():
    api_key = "your_api_key"
    site_key = "site_key_here"
    url = "https://example.com"  # The page where the reCAPTCHA is implemented

    solver = AiohttpreChaptchaAPI(apikey=api_key)
    token = solver.rechaptcha_v3_solver(sitekey=site_key, url=url)

    print("Solved reCAPTCHA token:", token)

```

## 📁 Examples

Explore the `examples/` directory for complete demos:

- [`examples/chatBot/`](https://github.com/taskorabot/TaskoraApi/blob/main/examples/chatBot/main.py)
- [`examples/InstagramApi/`](https://github.com/taskorabot/TaskoraApi/blob/main/examples/InstagramApi/main.py)
- [`examples/QuizApi/`](https://github.com/taskorabot/TaskoraApi/blob/main/examples/QuizApi/main.py)
- [`examples/reCaptchaV3Solver/`](https://github.com/taskorabot/TaskoraApi/blob/main/examples/reCaptchaV3Solver/main.py)

Each folder includes sample scripts and explanations.


## 📄 License

MIT License

## 👨‍💻 Author

Your Name – [SAM](https://taskora.odoo.com)  
GitHub: [@taskorabot](https://github.com/taskorabot)
Discord: [@taskora discord ](https://discord.com/invite/wMkKzGtAuQ)
```

