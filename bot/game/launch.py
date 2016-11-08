import telegram


def callback_query_game_launcher_handler(bot: telegram.Bot, update: telegram.Update):
    callback_query = update.callback_query
    game_short_name = callback_query.game_short_name
    if game_short_name == "rock_paper_scissors":
        callback_query_id = callback_query.id
        bot.answerCallbackQuery(callback_query_id, url="https://rawgit.com/alvarogzp/telegram-games/develop/games/rock-paper-scissors/game.html")
