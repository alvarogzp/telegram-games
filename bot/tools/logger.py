import time

import telegram

from . import config


class Logger:
    def __init__(self, bot: telegram.Bot, tag=None, reuse_message=False):
        self.bot = bot
        self.tag = tag
        self.reuse_message = reuse_message
        self.chat_id = config.Key.LOG_CHAT_ID.read()
        self.log_enabled = bool(self.chat_id)
        self.message_text = ""
        self.first_send = True
        self.message_id = None

    def debug(self, text):
        self.send("D", text)

    def info(self, text):
        self.send("I", text)

    def warn(self, text):
        self.send("W", text)

    def err(self, text):
        self.send("E", text)

    def send(self, level, text):
        if self.log_enabled:
            if not self.reuse_message:
                self._new_message()
            self._update_message_text(level, text)
            if self.first_send:
                self._send_first_message()
            else:
                self._edit_message()

    def _new_message(self):
        self.message_text = ""
        self.first_send = True

    def _update_message_text(self, level, text):
        text_to_add = ""
        if self.message_text:
            text_to_add += "\n"
        text_to_add += self._get_formatted_text(level, text)
        self.message_text += text_to_add

    def _get_formatted_text(self, level, text):
        tag = ""
        if self.tag:
            tag = " #{} ".format(self.tag)
        return ">> #{}  [{}] {} {}".format(level, time.strftime("%X"), tag, text)

    def _send_first_message(self):
        message = self._do_api_call(self.bot.sendMessage)
        self.message_id = message.message_id
        self.first_send = False

    def _edit_message(self):
        self._do_api_call(self.bot.editMessageText, message_id=self.message_id)

    def _do_api_call(self, function, **additional_params):
        return function(text=self.message_text, chat_id=self.chat_id, disable_web_page_preview=True, **additional_params)
