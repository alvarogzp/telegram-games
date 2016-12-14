#!/usr/bin/env python3

import logging

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, InlineQueryHandler

from game.api.server import start_api_server
from game.chooser import inline_query_game_chooser_handler
from game.launch import callback_query_game_launcher_handler
from tools import config, commands
from tools.logger import Logger

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater(token=config.Key.AUTH_TOKEN.read())
bot = updater.bot
bot.updater = updater
dispatcher = updater.dispatcher

logger = Logger(bot, "START", reuse_message=True)
logger.debug("Starting bot...")

dispatcher.add_handler(CommandHandler("config", commands.config_editor_command, pass_args=True, allow_edited=True))
dispatcher.add_handler(CommandHandler("restart", commands.restart_command, pass_args=True, allow_edited=True))

dispatcher.add_handler(CallbackQueryHandler(callback_query_game_launcher_handler))
dispatcher.add_handler(InlineQueryHandler(inline_query_game_chooser_handler))

updater.start_polling()

logger.debug("Starting api server...")
start_api_server()

logger.info("Running!")
