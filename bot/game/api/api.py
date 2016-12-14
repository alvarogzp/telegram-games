import itertools

from game.score import ScoreUpdater
from tools.logger import Logger


class BotApi:
    def __init__(self, bot, score: ScoreUpdater):
        self.logger = Logger(bot, "API", reuse_message=False)
        self.logger.info("Bot API started")
        self.score = score

    def set_score(self, data):
        self._log_call("set_score", data)
        try:
            auth, score = data.split("&", 1)
            score = int(score)
            self.score.set_score(auth, score)
        except:
            pass

    def _log_call(self, name, *args, **kwargs):
        log_call(self.logger.debug, name, args, kwargs)


class DummyApi:
    def __getattr__(self, item):
        return lambda *args, **kwargs: log_call(print, item, args, kwargs)


def log_call(log_func, call_name, args, kwargs):
    call_args = map(repr, args)
    call_kwargs = (k + "=" + repr(v) for k, v in kwargs.items())
    all_args = ", ".join(itertools.chain(call_args, call_kwargs))
    log_func(">> Called: " + call_name + "(" + all_args + ")")
