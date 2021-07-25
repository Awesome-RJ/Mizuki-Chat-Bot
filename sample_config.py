import os


class Config(object):
      BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
      BOT_ID = os.environ.get("BOT_ID", "")
