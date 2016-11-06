import threading

import telegram

from bot import config
from bot.logger import Logger


def config_editor_command(bot, update, args):
    ConfigEditorCommand(bot, update, args).run()


def restart_command(bot, update, args):
    RestartCommand(bot, update, args).run()


class Command:
    def __init__(self, bot: telegram.Bot, update: telegram.Update, args):
        self.bot = bot
        message = update.message or update.edited_message
        self.chat_id = message.chat_id
        self.args = args

    def run(self):
        self.handle()

    def handle(self):
        pass

    def _send_message(self, text):
        self.bot.sendMessage(chat_id=self.chat_id, text=text)


class AdminCommand(Command):
    def run(self):
        if self.is_admin_chat():
            self.handle()

    def is_admin_chat(self):
        return str(self.chat_id) == config.Key.ADMIN_CHAT_ID.read()


class ConfigEditorCommand(AdminCommand):
    def handle(self):
        if len(self.args) == 0:
            self._send_message("Usage: /config key [value]")
        else:
            key = self.args[0].upper()
            config_object = config.Key.get_by_name(key)
            if config_object is None:
                self._send_message("Unknown config '{}'".format(key))
            else:
                if len(self.args) == 1:
                    config_value = config_object.read()
                    self._send_message("Current value of '{}':\n\n{}".format(key, config_value))
                elif len(self.args) == 2 and self.args[1] == "-":
                    config_object.delete()
                    self._send_message("Restored '{}' to default value.".format(key))
                else:
                    new_value = " ".join(self.args[1:])
                    try:
                        new_value = config_object.parse(new_value)
                    except Exception as e:
                        self._send_message("Error while trying to parse new value: " + str(e))
                    else:
                        config_object.write(new_value)
                        read_value = config_object.read()
                        self._send_message("Config '{}' set to:\n\n{}".format(key, read_value))


class RestartCommand(AdminCommand):
    def handle(self):
        threading.Thread(target=self.bot.updater.stop).start()
        Logger(self.bot).info("Restarting bot...")
