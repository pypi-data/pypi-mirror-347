from tell_py.sender import Sender


class Tell:
    def __init__(self, bot_token: str, chat_id: str):
        self.logger = Sender(bot_token, chat_id)

    def info(self, msg: str):
        try:
            self.logger.info(msg)
        except Exception as e:
            print(f"Error sending info: {e}")

    def error(self, msg: str):
        try:
            self.logger.error(msg)
        except Exception as e:
            print(f"Error sending error: {e}")

    def warn(self, msg: str):
        try:
            self.logger.warn(msg)
        except Exception as e:
            print(f"Error sending warning: {e}")

    def log(self, msg: str):
        try:
            self.logger.log(msg)
        except Exception as e:
            print(f"Error sending log: {e}")