from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

NOTIFY_BOT_TOKEN = env.str("ERROR_NOTIFY_BOT_TOKEN")
NOTIFY_CHANNEL_ID = env.str("ERROR_NOTIFY_CHANNEL_ID")
