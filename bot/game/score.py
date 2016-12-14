import telegram

from game.api import auth

MAX_SCORE = 999999


class ScoreUpdater:
    def __init__(self, bot: telegram.Bot):
        self.bot = bot

    def set_score(self, data, score):
        data = auth.decode(data)
        if data and score < MAX_SCORE:
            self._do_set_score(data["u"], data["i"], score)

    def _do_set_score(self, user_id, inline_message_id, score):
        self.bot.setGameScore(user_id, score, inline_message_id=inline_message_id)
