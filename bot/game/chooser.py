import telegram

from tools.format import formatted_user
from tools.logger import Logger

PROD_GAME = "rock_paper_scissors"
DEV_GAME = "rock_paper_scissors_dev"


def inline_query_game_chooser_handler(bot: telegram.Bot, update: telegram.Update):
    inline_query = update.inline_query
    if inline_query.query == DEV_GAME:
        result = [telegram.InlineQueryResultGame(DEV_GAME, DEV_GAME)]
    else:
        result = [telegram.InlineQueryResultGame(PROD_GAME, PROD_GAME)]
    bot.answerInlineQuery(inline_query.id, result)
    _log(bot, inline_query)


def _log(bot, inline_query):
    user = formatted_user(inline_query.from_user)
    query = repr(inline_query.query)
    Logger(bot, tag="BOT").debug("Inline query from {}: {}".format(user, query))
