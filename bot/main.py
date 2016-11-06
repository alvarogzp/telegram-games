#!/usr/bin/env python3

import logging

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from game.launch import callback_query_handler
from tools import config, commands
from tools.logger import Logger

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater(token=config.Key.AUTH_TOKEN.read())
bot = updater.bot
bot.updater = updater
dispatcher = updater.dispatcher

logger = Logger(bot)
logger.debug("Starting bot...")

dispatcher.add_handler(CommandHandler("config", commands.config_editor_command, pass_args=True, allow_edited=True))
dispatcher.add_handler(CommandHandler("restart", commands.restart_command, pass_args=True, allow_edited=True))

dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))

updater.start_polling()

logger.info("Bot started!")
