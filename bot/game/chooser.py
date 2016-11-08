import telegram


def inline_query_game_chooser_handler(bot: telegram.Bot, update: telegram.Update):
    inline_query = update.inline_query
    result = [telegram.InlineQueryResultGame("rock_paper_scissors", "rock_paper_scissors")]
    bot.answerInlineQuery(inline_query.id, result)
