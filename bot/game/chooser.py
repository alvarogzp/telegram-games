import telegram

from tools.logger import Logger


def inline_query_game_chooser_handler(bot: telegram.Bot, update: telegram.Update):
    inline_query = update.inline_query
    result = [telegram.InlineQueryResultGame("rock_paper_scissors", "rock_paper_scissors")]
    bot.answerInlineQuery(inline_query.id, result)
    _log(bot, inline_query)


def _log(bot, inline_query):
    user = _formatted_user(inline_query.from_user)
    query = repr(inline_query.query)
    Logger(bot, tag="BOT").debug("Inline query from {}: {}".format(user, query))


def _formatted_user(user):
    if user.username is not None:
        formatted_user = "@" + user.username
    elif user.first_name is not None:
        formatted_user = user.first_name
        if user.last_name is not None:
            formatted_user += " " + user.last_name
    else:
        formatted_user = str(user.id)
    return formatted_user
