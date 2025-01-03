from pyrogram.client import Client
from pyrogram import filters
import logging
import colorlog
from handlers.stt_handler import stt_handler
from handlers.ping_handler import ping_handler
from handlers.cat_handler import cat_handler
from handlers.sping_handler import sping_handler
from handlers.speedtest_handler import speedtest_handler
from handlers.eight_ball_handler import eight_ball_handler
from handlers.tracert_handler import tracert_handler
from handlers.calc_handler import calc_handler
from handlers.remote_handler import remote_handler
from config import API_ID, API_HASH, PHONE_NUMBER, PREFIXES
from pyrogram.handlers.message_handler import MessageHandler

# Налаштування логування
logger = logging.getLogger("pyrogram")
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Ініціалізація бота
app = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    phone_number=PHONE_NUMBER
)

app.add_handler(MessageHandler(stt_handler, filters.command("stt", prefixes=PREFIXES) & filters.me))
app.add_handler(MessageHandler(ping_handler, filters.command("ping", prefixes=PREFIXES) & filters.me))
app.add_handler(MessageHandler(cat_handler, filters.command("cat", prefixes=PREFIXES) & filters.me))
app.add_handler(MessageHandler(sping_handler, filters.command("sping", prefixes=PREFIXES) & filters.me))
app.add_handler(MessageHandler(speedtest_handler, filters.command("speedtest", prefixes=PREFIXES) & filters.me))
app.add_handler(MessageHandler(eight_ball_handler, filters.command("8ball", prefixes=PREFIXES)))
app.add_handler(MessageHandler(tracert_handler, filters.command("tracert", prefixes=PREFIXES) & filters.me))
app.add_handler(MessageHandler(calc_handler, filters.command("calc", prefixes=PREFIXES) & filters.me))
app.add_handler(MessageHandler(remote_handler, filters.command(["screen"], prefixes=PREFIXES)))
app.add_handler(MessageHandler(remote_handler, filters.command(["lock", "sleep", "hibernate"], prefixes=PREFIXES) & filters.me))
app.add_handler(MessageHandler(remote_handler, filters.command(["spotify"], prefixes=PREFIXES) & filters.me))

app.run()