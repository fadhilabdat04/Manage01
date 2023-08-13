import asyncio
import time
from inspect import getfullargspec
from os import path
from geezlibs import DEVS
from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pyrogram import Client
from pyrogram.types import Message
from pyromod import listen
from Python_ARQ import ARQ
from telegraph import Telegraph
from os import environ, path

from dotenv import load_dotenv

if path.exists("config.env"):
    load_dotenv("config.env")
    
BANNED_USER = environ.get("BANNED_USER" or None)  
BOT_TOKEN = environ.get("BOT_TOKEN", "6515197149:AAEicDMoVIsS5KfEPpIorYEsLyuuxX55xkk")
API_ID = int(environ.get("API_ID", 17896688))
API_HASH = environ.get("API_HASH", "947327cf5ff0053a66bf7951f9db5658")
SUDO_USERS_ID = [int(x) for x in environ.get("SUDO_USERS_ID", "1948147616").split()]
LOG_GROUP_ID = int(environ.get("LOG_GROUP_ID", "-1001795374467"))
GBAN_LOG_GROUP_ID = int(environ.get("GBAN_LOG_GROUP_ID", "-1001571197486"))
MESSAGE_DUMP_CHAT = int(environ.get("MESSAGE_DUMP_CHAT", "-1001795374467"))
WELCOME_DELAY_KICK_SEC = int(environ.get("WELCOME_DELAY_KICK_SEC", None))
MONGO_URL = environ.get("MONGO_URL", "mongodb+srv://doadmin:N5qU43b167EgJH89@db-mongodb-sgp1-31724-8b5ccdd0.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-sgp1-31724")
ARQ_API_URL = environ.get("ARQ_API_URL", None)
ARQ_API_KEY = environ.get("ARQ_API_KEY", None)
RSS_DELAY = int(environ.get("RSS_DELAY", None))
STRING_SESSION = environ.get("STRING_SESSION", "AQAP-GEAvqHAJqYa8_-ds2nJ-lZvNjUh3mGGn-xivHpoZ74F_vPpz21FiPswwZ8WWjZemJv1XK0kIBky_Yx6t0sJDPwiebTvuTErZU6tVk8n01TZudW2EthaW2htIpq4QRSo_WymL4Nsob3-Tkc5SM20i1AMCDU3ANpqnsB3H0zfHCBx7BDsOFmJpsrMGHdq1dA2JYlixTKaBu0ArNQghATh8sRBgVrawwopyTY552SgS45WTOVCH784CdILXorFzy3-jX4mwVB2DrRBPbSk0gOkISl3y9-JPenHMh-FHfFNVv_PX3jY5MtFS6Kv-RhdhmD7yS93F8Chz7zIYmM_02kSYjc0fwAAAAB1MYXEAA")
BLACKLIST_CHAT = environ.get("BLACKLIST_CHAT")
UPSTREAM_REPO = environ.get(
    "UPSTREAM_REPO", ""
)


ALIVE_LOGO = "https://te.legra.ph/file/d2f257710e964cd8aa0db.jpg"
GBAN_LOG_GROUP_ID = GBAN_LOG_GROUP_ID
SUDOERS = DEVS
WELCOME_DELAY_KICK_SEC = WELCOME_DELAY_KICK_SEC
LOG_GROUP_ID = LOG_GROUP_ID
MESSAGE_DUMP_CHAT = MESSAGE_DUMP_CHAT
MOD_LOAD = []
MOD_NOLOAD = []
bot_start_time = time.time()

# MongoDB client
print("[INFO]: INITIALIZING DATABASE")
mongo_client = MongoClient(MONGO_URL)
db = mongo_client.pitung


async def load_sudoers():
    global SUDOERS
    print("[INFO]: LOADING SUDOERS")
    sudoersdb = db.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [1948147616] if not sudoers else sudoers["sudoers"]
    for user_id in SUDOERS:
        if user_id not in sudoers:
            sudoers.append(user_id)
            await sudoersdb.update_one(
                {"sudo": "sudo"},
                {"$set": {"sudoers": sudoers}},
                upsert=True,
            )
    SUDOERS = (SUDOERS + sudoers) if sudoers else SUDOERS
    print("[INFO]: LOADED SUDOERS")


loop = asyncio.get_event_loop()
loop.run_until_complete(load_sudoers())

aiohttpsession = ClientSession()

arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

app = Client("sipitung", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

print("[INFO]: STARTING BOT CLIENT")
app.start()

print("[INFO]: GATHERING PROFILE INFO")
x = app.get_me()

bot1 = (
    Client(
        name="bot1",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING_SESSION,
    )
    if STRING_SESSION
    else None
)
print("[INFO]: STARTING ASSISTANT")
bot1.start()
y = bot1.get_me

BOT_ID = x.id
BOT_NAME = x.first_name + (x.last_name or "")
BOT_USERNAME = x.username
BOT_MENTION = x.mention
BOT_DC_ID = x.dc_id

telegraph = Telegraph()
telegraph.create_account(short_name=BOT_USERNAME)


async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})
