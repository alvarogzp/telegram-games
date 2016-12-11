import telegram

from game.api import api_data


def callback_query_game_launcher_handler(bot: telegram.Bot, update: telegram.Update):
    callback_query = update.callback_query
    game_short_name = callback_query.game_short_name
    if game_short_name == "rock_paper_scissors":
        callback_query_id = callback_query.id
        url_data = _build_url_data(callback_query)
        url = "https://rawgit.com/alvarogzp/telegram-games/develop/games/rock-paper-scissors/game.html#" + url_data
        bot.answerCallbackQuery(callback_query_id, url=url)


def _build_url_data(callback_query: telegram.CallbackQuery):
    data = {
        "u": callback_query.from_user.id,
        "i": callback_query.inline_message_id
    }
    return api_data.encode(data)
