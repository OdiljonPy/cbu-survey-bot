from environs import Env
from utils.db_api.connect_backend import DatabaseRequest

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

NOTIFY_BOT_TOKEN = env.str("ERROR_NOTIFY_BOT_TOKEN")
NOTIFY_CHANNEL_ID = env.str("ERROR_NOTIFY_CHANNEL_ID")

BACKEND_URL = env.str("BACKEND_URL")

db = DatabaseRequest(url=BACKEND_URL)
