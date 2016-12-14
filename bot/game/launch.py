import telegram

from game.api import auth
from tools import config
from tools.format import formatted_user
from tools.logger import Logger

PROD_GAME = "rock_paper_scissors"
DEV_GAME = "rock_paper_scissors_dev"
GAMES = (PROD_GAME, DEV_GAME)


def callback_query_game_launcher_handler(bot: telegram.Bot, update: telegram.Update):
    callback_query = update.callback_query
    game_short_name = callback_query.game_short_name
    if game_short_name in GAMES:
        url_data = _build_url_data(callback_query)
        callback_query_id = callback_query.id
        if game_short_name == DEV_GAME:
            base_url = "https://rawgit.com/alvarogzp/telegram-games/develop"
        else:
            base_url = "https://cdn.rawgit.com/alvarogzp/telegram-games/" + config.Key.PROD_GAME_TAG.read()
        url = base_url + "/games/rock-paper-scissors/game.html#" + url_data
        bot.answerCallbackQuery(callback_query_id, url=url)
        _log(bot, callback_query)


def _build_url_data(callback_query: telegram.CallbackQuery):
    data = {
        "u": callback_query.from_user.id,
        "i": callback_query.inline_message_id
    }
    return auth.encode(data)


def _log(bot, callback_query):
    user = formatted_user(callback_query.from_user)
    game = callback_query.game_short_name
    user_id = callback_query.from_user.id
    inline_message_id = callback_query.inline_message_id
    Logger(bot, tag="BOT").debug("Game '{}' launched by {} ({}, {})".format(game, user, user_id, inline_message_id))
