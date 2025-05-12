import requests
from datetime import datetime
from typing import Literal


class Sender:
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize the Sender with bot token and chat ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    def info(self, msg: str):
        message = self._format_message("info", msg)
        self._send_message(message)

    def error(self, msg: str):
        message = self._format_message("error", msg)
        self._send_message(message)

    def warn(self, msg: str):
        message = self._format_message("warn", msg)
        self._send_message(message)

    def log(self, msg: str):
        message = self._format_message("log", msg)
        self._send_message(message)

    def _send_message(self, text: str):
        try:
            url = f"{self.base_url}/sendMessage"
            response = requests.post(url, json={
                "chat_id": self.chat_id,
                "text": text
            })
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❗ Failed to send message: {e}")

    def _format_message(self, type_: Literal["info", "error", "warn", "log"], msg: str) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if type_ == "info":
            return f"ℹ️ {msg}\n\nTimestamp: {timestamp}"
        elif type_ == "error":
            return f"❌ {msg}\n\nTimestamp: {timestamp}"
        elif type_ == "warn":
            return f"⚠️ {msg}\n\nTimestamp: {timestamp}"
        return f"{msg}\n\nTimestamp: {timestamp}"