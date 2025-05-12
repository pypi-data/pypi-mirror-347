# 📬 TellPy — Telegram Logging for Python

[![PyPI version](https://img.shields.io/pypi/v/tell-py.svg)](https://pypi.org/project/tell-py/)
[![Python versions](https://img.shields.io/pypi/pyversions/tell-py.svg)](https://pypi.org/project/tell-py/)

**TellPy** is a lightweight Python library for sending logs and notifications to a Telegram chat using a bot.  
It supports different log levels like `info`, `warning`, `error`, and general-purpose logs.

---

## 🚀 Features

- 📡 Send messages to Telegram directly from Python
- ✅ Supports `info`, `warn`, `error`, and `log` levels
- 🧩 Simple interface for integration with any app or script
- 🛠️ Built on top of `requests` and `python-dotenv`

---

## 📦 Installation

Install via [PyPI](https://pypi.org/project/tell-py/):

```bash
pip install tell-py
```

## 🔧 Basic Usage
```python

from tell_py import Tell

tell = Tell(
    bot_token="YOUR_BOT_TOKEN",
    chat_id="YOUR_CHAT_ID"
)

tell.info("Everything is working fine.")
tell.warn("This might be a warning.")
tell.error("An error occurred!")
tell.log("Just a normal log.")
```

## How to Get Your Bot Token and Chat ID
1. **Create a Bot**: Open Telegram and search for the BotFather. Use the `/newbot` command to create a new bot. Follow the instructions to get your bot token.
2. **Get Your Chat ID**: Start a chat with your bot and send any message. Then, use the following URL to get your chat ID:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
3. **Response**: Look for the `chat` object in the JSON response. The `id` field is your chat ID.

