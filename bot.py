import io
import pyromod.listen
from ydb import manag_db
from telegraph import upload_file
from pyrogram import Client, filters, idle
from pyrogram.errors import FloodWait, UserIsBlocked, PeerIdInvalid, InputUserDeactivated
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
import os
from time import time, strftime, gmtime
import traceback
import logging
import shutil
from config import Config
from db import manage_db
from datetime import datetime
import json
from subprocess import run as sub_run
from pytz import timezone
from psutil import virtual_memory, cpu_percent
from drive import GoogleDriveHelper
from util import *
from ripper import *
from logging.handlers import RotatingFileHandler
from expiringdict import ExpiringDict
from time import time
import random
#from uvloop import install
from urllib.parse import quote

# the logging things
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "log.txt", maxBytes=50000000, backupCount=10
        ),
        logging.StreamHandler(),
    ],
)

log = logging.getLogger(__name__)


BLACKLISTED_EXTENSIONS = (".PY",".ENV", ".CPY", ".PYC", "YML", ".TXT", ".SH", "DOCKERFILE", "CACHE", "SESSION", "JOURNAL", "TOOLS", "CONFIGS", "__")
mydb = manage_db()
db = manag_db()
gb = "True"
CHECK_ONCE = []
Bot = Client("PaidBot",
               api_id=Config.API_ID,
               api_hash=Config.API_HASH,
               bot_token=Config.BOT_TOKEN,
               workers=300,
               max_concurrent_transmissions=200)

if Config.SESSION_STRING:
    User = Client(
        "UserClient",
        session_string=Config.SESSION_STRING,
        api_id = Config.API_ID,
        api_hash = Config.API_HASH,
        sleep_threshold = 30,
        no_updates = True,
        workers=300,
        max_concurrent_transmissions=200
    )
else:
    User = None

USER_DATA = ExpiringDict(max_len=1000, max_age_seconds=60*60)
# Bot stats
BOT_UPSTATE = datetime.now(timezone('Asia/Kolkata')).strftime("%d/%m/%y %I:%M:%S %p")
BOT_START_TIME = time()
ST1 = [ 
    [
        InlineKeyboardButton(text="Updates Channel", url="https://t.me/AntoniBots"),
        InlineKeyboardButton(text="Support Grp", url="https://t.me/tony_091")
    ],
    [
        InlineKeyboardButton(f"About", callback_data="About"),
        InlineKeyboardButton(f"Help", callback_data="Help"),
        InlineKeyboardButton(f"Contact Us", callback_data="ContactUs"),
    ],
    [
        InlineKeyboardButton(f"Usage", callback_data="usage"),
        InlineKeyboardButton(f"Plans", callback_data="plans"),   
    ]
]

async def OpenSettings(m: Message, userid):
    try:
        userdata = await db.get_user(userid)
        SET = [
                [
                    InlineKeyboardButton(f"Upload As", callback_data="triggerUploadMod"),
                    InlineKeyboardButton(f"{'Video' if userdata['as_stream'][0] == 't' else 'Document'}", callback_data="triggerUploadMode")
                ],
                [
                    InlineKeyboardButton(f"Upload Mode", callback_data="Uode"),
                    InlineKeyboardButton(f"{'Telegram' if userdata['ul_mode'][0] == 't' else 'Google Gdrive'}", callback_data="UMode")
                ],
                [
                    InlineKeyboardButton("Set Thumbnail", callback_data="setThumbnail"),
                    InlineKeyboardButton(f"{'MP4' if userdata['mkv'] == 'mp4' else 'MKV'}", callback_data="MKV")
                ],
                [
                    InlineKeyboardButton("Show Thumbnail", callback_data="showThumbnail"),
                    InlineKeyboardButton("Delete Thumbnail", callback_data="deleteThumbnail")
                ],
                [
                    InlineKeyboardButton("Close", callback_data="closeMessage"),
                    InlineKeyboardButton(f"{'Detailed Caption ✅' if userdata['format'][0] == 'f' else 'Detailed Caption ✖️'}", callback_data="caption_format")
                ],
                [
                    InlineKeyboardButton(f"{'Custom Drive ✅' if userdata['cs_drive'][0] == 't' else 'Custom Drive ✖️'}", callback_data="csdrive"),
                    InlineKeyboardButton("Set Custom Drive", callback_data="setdrive")
                ]
        ]
        await m.edit(text="Here You Can Change or Configure Your Settings:",
            reply_markup=InlineKeyboardMarkup(SET))
            
    except MessageNotModified:
        pass
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await m.edit("You Are Spamming!")
    except Exception as err:
        raise err
        
@Bot.on_callback_query(filters.regex(pattern="^(triggerUploadMode|caption_format|MKV|csdrive|closeMessage|showSettings|showThumbnail|deleteThumbnail|setThumbnail|CallbackQuery|UMode|setdrive)$"))
async def callback(c: Client, CallbackQuery):
            
    if CallbackQuery.data == "triggerUploadMode":
        await CallbackQuery.answer()
        userdata = await db.get_user(CallbackQuery.from_user.id)
        as_stream = userdata["as_stream"]
        if as_stream == 'f':
            await db.set_stream(CallbackQuery.from_user.id, "t")
        else:
            await db.set_stream(CallbackQuery.from_user.id, "f")
        await OpenSettings(CallbackQuery.message, CallbackQuery.from_user.id)

    elif CallbackQuery.data == "csdrive":
        await CallbackQuery.answer()
        userdata = await db.get_user(CallbackQuery.from_user.id)
        csdrive = userdata["cs_drive"]
        if csdrive == 't':
            await db.cs_drive(CallbackQuery.from_user.id, "f")
        else:
            await db.cs_drive(CallbackQuery.from_user.id, "t")
        await OpenSettings(CallbackQuery.message, CallbackQuery.from_user.id)

    elif CallbackQuery.data == "caption_format":
        await CallbackQuery.answer()
        userdata = await db.get_user(CallbackQuery.from_user.id)
        as_stream = userdata["format"]
        if as_stream == 'f':
            await db.set_caption(CallbackQuery.from_user.id, "t")
        else:
            await db.set_caption(CallbackQuery.from_user.id, "f")
        await OpenSettings(CallbackQuery.message, CallbackQuery.from_user.id)
 
    elif CallbackQuery.data == "UMode":
        await CallbackQuery.answer()
        userdata = await db.get_user(CallbackQuery.from_user.id)
        ulmode = userdata["ul_mode"]
        if ulmode == 'g':
            await db.set_ul_mode(CallbackQuery.from_user.id, "t")
        else:
            await db.set_ul_mode(CallbackQuery.from_user.id, "g")
        await OpenSettings(CallbackQuery.message, CallbackQuery.from_user.id)
 
    elif CallbackQuery.data == "showSettings":
        await CallbackQuery.answer()
        await OpenSettings(CallbackQuery.message, CallbackQuery.from_user.id)
 
    elif CallbackQuery.data == "showThumbnail":
        userdata = await db.get_user(CallbackQuery.from_user.id)
        thumbnail = userdata["thumb"]
        if thumbnail == "":
            await CallbackQuery.answer("You didn't set any custom thumbnail!", show_alert=True)
        else:
            await CallbackQuery.answer()      
            await CallbackQuery.message.edit(f"**Your Custom Thumbnail:** **{thumbnail}**", reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton("Delete Thumbnail", callback_data="deleteThumbnail")],
                                [InlineKeyboardButton("Close", callback_data="closeMessage")]]))
    
    elif CallbackQuery.data == "deleteThumbnail":
        await db.set_thumb(CallbackQuery.from_user.id, "")
        await CallbackQuery.answer("Okay, I deleted your custom thumbnail. Now I will apply default thumbnail.", show_alert=True)
        await CallbackQuery.message.delete(True)
    
    elif CallbackQuery.data == "setdrive":
        await CallbackQuery.answer()
        await CallbackQuery.message.edit("Send me Drive Folder Id to set that as custom Drive.\n\n"
                              "Press /cancel to cancel process.")
        drive_id = await c.listen(CallbackQuery.message.chat.id)
        drive_id = drive_id.text.strip()
        await db.set_drive(CallbackQuery.from_user.id, drive_id)
        await CallbackQuery.message.edit("Okay!\n"
                                  "Now I will apply this Drive to next uploads.",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton("Show Settings",
                                                                   callback_data="showSettings")]]
                                  ))
        
    elif CallbackQuery.data == "setThumbnail":
        await CallbackQuery.answer()
        await CallbackQuery.message.edit("Send me any photo to set that as custom thumbnail.\n\n"
                              "Press /cancel to cancel process.")
        from_user_thumb = await c.listen(CallbackQuery.message.chat.id)
        if not from_user_thumb.photo:
            await CallbackQuery.message.edit("Process Cancelled!")
            return await from_user_thumb.continue_propagation()
        else:
            try:
                filepath = await from_user_thumb.download()
                telegra_ph = upload_file(filepath)
                thumbpath = "https://telegra.ph" + telegra_ph[0]
            except Exception as e:
                await CallbackQuery.message.edit("Failed to save custome thumbnail")
                return await from_user_thumb.continue_propagation()
            await db.set_thumb(CallbackQuery.from_user.id, thumbpath)
            await CallbackQuery.message.edit("Okay!\n"
                                  "Now I will apply this thumbnail to next uploads.",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[InlineKeyboardButton("Show Settings",
                                                                   callback_data="showSettings")]]
                                  ))
            
    elif CallbackQuery.data == "closeMessage":
        await CallbackQuery.message.delete()
    elif CallbackQuery.data == "MKV":
        await CallbackQuery.answer()
        userdata = await db.get_user(CallbackQuery.from_user.id)
        MKV = userdata["mkv"]
        if MKV == 'mkv':
            await db.set_for(CallbackQuery.from_user.id, "mp4")
        else:
            await db.set_for(CallbackQuery.from_user.id, "mkv")
        await OpenSettings(CallbackQuery.message, CallbackQuery.from_user.id)

@Bot.on_message(filters.command(["settings"]))
async def remove_all(bot, message):
    await db.add_user(message.from_user.id)
    t = await message.reply_text("Getting your current settings ...")
    await OpenSettings(t, message.from_user.id)

async def OpenTokens(m: Message, userid):
    try:
        SET = [
                [
                    InlineKeyboardButton("Set HS Token", callback_data="seths"),
                    InlineKeyboardButton("Set Zee5 Token", callback_data="setz5"),
                    InlineKeyboardButton("Set Tentakotta Token", callback_data="settk")
                ]
        ]
        await m.edit(text="**Here You Can Change or Configure Your Settings:**",
            reply_markup=InlineKeyboardMarkup(SET))            
    except MessageNotModified:
        pass
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await m.edit("You Are Spamming!")
    except Exception as err:
        raise err
    
@Bot.on_callback_query(filters.regex(pattern="^(seths|setz5|settk)$"))
async def callback(c: Client, CallbackQuery):
    if CallbackQuery.data == "seths":
        await CallbackQuery.answer()
        await CallbackQuery.message.edit("`send me new hs token`")
        message = await c.listen(CallbackQuery.from_user.id)
        token = message.text.strip()
        await db.set_hs(token)
        await CallbackQuery.answer("**HotStar Token Updated!**")
    elif CallbackQuery.data == "setz5":
        await CallbackQuery.answer()
        await CallbackQuery.message.edit("`send me new Zee5 token`")
        message = await c.listen(CallbackQuery.from_user.id)
        token = message.text.strip()
        await db.set_z5(token)
        await CallbackQuery.message.delete()
        await CallbackQuery.answer("**Token Updated!**")  
    elif CallbackQuery.data == "settk":
        await CallbackQuery.answer()
        await CallbackQuery.message.edit("`send me new tentakotta token`")
        message = await c.listen(CallbackQuery.from_user.id)
        token = message.text.strip()
        await db.set_tk(token)
        await CallbackQuery.message.delete()
        await CallbackQuery.answer("**Token Updated!**")
    
@Bot.on_message(filters.command(["tokens"]))
async def removell(bot, message):
    t = await message.reply_text("Getting your current settings ...")
    await OpenTokens(t, message.from_user.id)

@Bot.on_message(filters.command(["getall"]) & filters.user(Config.OWNER_ID))
async def getpeall(bot: Client, message):
    users = await mydb.get_premium_users()
    msg = "**✅ List of premium Users of this bot: ** \n\n"
    async for i in users:
        expiry = i.get('expiry')
        balance = i.get('balance')
        user_id = i.get('_id')
        row_number = "==>"
        try:
            from_user = await bot.get_users(int(user_id))
            if expiry is not None and balance is not None:
                if expiry <= 0 or balance <= 0:
                    continue 
                else:
                    msg += f' **{row_number} {from_user.mention}**\n' # Corrected line
        except Exception as e:
            continue
    await message.reply_text(msg)
    
async def is_subscribed(user_id):
    chkUser = await mydb.get_user(user_id)
    if user_id in Config.OWNER_ID:
        return True
    if chkUser:
        expiryDate = chkUser.get("expiry")
        balance = chkUser.get("balance")
        start_date = chkUser.get("start")
        #start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S.%f") 
        now_date = datetime.now()
        if (now_date-start_date).days < expiryDate:
            if balance > 0:
                return True

@Bot.on_message(filters.command("clean") & filters.user(Config.OWNER_ID))
async def cleanHandler(bot: Client, message: Message):
    global USER_DATA, BOT_UPSTATE, BOT_START_TIME
    os.system("rm -rf downloads/*")
    os.system("rm -rf output/*")
    os.system(f"rm -rf {Config.TEMP_DIR}/*")
    USER_DATA = ExpiringDict(max_len=1000, max_age_seconds=60*60)
    BOT_UPSTATE = datetime.now(timezone('Asia/Kolkata')).strftime("%d/%m/%y %I:%M:%S %p")
    BOT_START_TIME = time()
    await message.reply_text("**Cache cleaned ✅**")

async def filter_subscription(_, __, m):
    chkUser = await is_subscribed(m.from_user.id)
    if m.from_user.id in Config.OWNER_ID:
        return True
    if chkUser:
        return True
    await mydb.add_user(m.from_user.id)
    await m.reply_text("You haven't subscribed yet, check using /plans\n\ncontact owner to get subscription")
    return False

static_auth_filter = filters.create(filter_subscription)

@Bot.on_message(filters.command("plans"))
async def start_handler(bot: Client, message: Message):
    await message.reply_text(text="""**
    👇INDIVIDUAL PLANS(All OTTs)👇

1. 99Rs/- Unlimited Downloads/1 Day 
2. 499Rs/- Unlimited Downloads/28 Days
3. 2000Rs/- Unlimited Downloads/365 Days[Limited]

⚠️Term and Conditions⚠️

• Payments are non-refundable, and we do not provide refunds. 
• If the service ceases to function, no compensation is provided.
•Payments Methods of Pakistan , Bangladesh , India are accepted.
• Other methods :- Paypal, Binance , crypto 

Contact to buy Subscription: [Tony](https://t.me/tony_091)**""")
    
@Bot.on_message(filters.command("otts"))
async def start_handler(bot: Client, message: Message):
  await message.reply_text(text="""**Here I support Direct DRM links of
  OTT  -
   
Sunnxt
Sonyliv
Jio cinema
HotStar
Zee5
Lionsgatlay
Primevideo[down]
MX player
Manoramamax
Aha video
Amazon mini tv
Tentakotta
Dangal Play
Discovery Plus  
RajDigitalTv
ETVWIN
ULLU
CRUNCHYROLL
More OTTs Soon!

Thanks For Using ANToNi Bot ❤️**""")
    
@Bot.on_message(filters.command("sub") & filters.user(Config.OWNER_ID))
async def tg_subget_Handler(bot: Client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.text.split(" ", 1)[1]
    msg_ = await get_subscription(user_id, message)
    await message.reply_text(msg_)                              
    
@Bot.on_message(filters.command(["myplan"]))
async def tg_infoget_Handler(bot: Client, message: Message):
    user_id = message.from_user.id
    await mydb.add_user(user_id)
    await db.add_user(message.from_user.id)
    msg_ = await get_subscription(user_id, message)
    await message.reply_text(msg_)

@Bot.on_message(filters.command("tk_movies"))
async def tk_list(bot: Client, message: Message):
    resp1 = requests.get('https://api.tentkotta.com/tkapi/v6/tkapi/generateToken')
    token = resp1.json()['response']
    headers = {'token' : token}
    resp2 = requests.get('https://api.tentkotta.com/tkapi/v6/viewAll/1',headers=headers)
    response = resp2.json()['response']['items']
    y = []
    for x in response:
        k = ("title : " + x['title'] + " Link: " + "https://www.tentkotta.com/content/" +  str(x['contentId']))
        y.append(k)
    y_str = '\n'.join(map(str, y))
    with open('movies_list.txt', 'w') as file:
            file.write(y_str)
    with open('movies_list.txt', 'rb') as doc:
         await message.reply_document(
                document=doc,
                caption=f"**Tentkotaa Movies List**")
         await message.delete()
    
async def get_subscription(user_id, message):
    if user_id in Config.OWNER_ID:
        return "No limit for this user, infinite downloads allowed"
    chkUser = await mydb.get_user(user_id)
    if chkUser:
        expiryDate = chkUser.get("expiry")
        balance = chkUser.get("balance")
        start_date = chkUser.get("start")
        #start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S.%f") 
        now_date = datetime.now()
        msg = f"""**Hello {message.from_user.mention} Here is your Subscription info:- 
        User Name:- `{message.from_user.mention}`
        User ID:- `{user_id}`
        Plan Name - `Active`
        Is Premium - `True`
        Videos Left - `{balance}`
        Validity - `{expiryDate - (now_date-start_date).days} days`

        Please look on our plans by sending /plans. If you want to subscribe our plan please contact [Support](https://t.me/tony_rd_jrr) with your user id

        Have a Nice day 😊**"""
    else:
        msg = "No Subscription found...\n\ncheck /plans to get your subscription now..."
    return msg

async def send_msg(user_id, message):
    try:
        await message.copy(user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        log.exception(e)
        return 500, f"{user_id} : {traceback.format_exc()}\n"

@Bot.on_message(filters.command(["b", "broad"]) & static_auth_filter)
async def broadcasthandler(bot: Client, message: Message):
    try:
        broadcast_msg = message.reply_to_message
        if not broadcast_msg:
            return await message.reply_text("Please reply to message for broadcasting...")
        await message.reply_text("broadcast request recived, you will be notified once broadcast done", quote=True)
        some_users = await mydb.get_all_users()
        total_users = await mydb.total_users_count()
        broadcast_filename = "".join([random.choice(string.ascii_letters) for i in range(5)])
        broadcast_log = ""
        done = 0
        failed = 0
        success = 0
        log_file = io.BytesIO()
        log_file.name = f"broadcast_{broadcast_filename}.txt"
        async for user in some_users:
            sts, msg = await send_msg(
                user_id = user['_id'],
                message = broadcast_msg
            )
            if msg is not None:
                broadcast_log += msg
            if sts == 200:
                success += 1
            else:
                failed += 1
            done += 1
        log_file.write(broadcast_log.encode())
        if failed == 0:
            await message.reply_text(
            text=f"Broadcast completed`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True,
        )
        else:
            await message.reply_document(
            document=log_file,
            caption=f"Broadcast completed\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True,
        )
    except Exception as erro:
        log.exception(erro)
        pass

@Bot.on_message(filters.command(["status", "stats"]) & static_auth_filter)
async def status_msg(bot, update):
  await mydb.add_user(update.from_user.id)
  currentTime = strftime("%H:%M:%S", gmtime(time() - BOT_START_TIME)) 
  total, used, free = shutil.disk_usage(".")
  total, used, free = humanbytes(total), humanbytes(used), humanbytes(free)
  cpu_usage = cpu_percent()
  ram_usage = f"{humanbytes(virtual_memory().used)}/{humanbytes(virtual_memory().total)}"
  msg = f"**Bot Current Status**\n\n**Bot Uptime:** {currentTime} \n\n**Total disk space:** {total} \n**Used:** {used} \n**Free:** {free} \n**CPU Usage:** {cpu_usage}% \n**RAM Usage:** {ram_usage}\n**Restarted on** `{BOT_UPSTATE}`"
  await update.reply_text(msg, quote=True)


@Bot.on_message(filters.command("auth") & filters.user(Config.OWNER_ID))
async def tg_auth_Handler(bot: Client, message: Message):
    if message.reply_to_message:
        _, balance, days = message.text.split(" ")
        expiryDate = int(days)
        balance = int(balance)
        from_user = message.reply_to_message.from_user
    else:
        try:
            user_id, balance, days = message.text.split(" ")
            from_user = await bot.get_users(int(user_id))
            expiryDate = int(days)
            balance = int(balance)
        except:
            return await message.reply_text("send along with proper format or reply to user msg")
    await mydb.set_user(from_user.id, expiryDate, balance)
    await message.reply_text(f"""**New User added**
    **expiry**: {expiryDate} days
    **Videos**: {balance} videos
    **User Details:**
        user: {from_user.mention}
        id: `{from_user.id}`""")
    msg = f"""**Thanks For Subscribing To Our Bot. Wish You happy day ahead. 

    👤 User: {from_user.mention}
    🪪 User ID: {from_user.id}
    ⬇️ Max. Downloads: {balance}
    ⏳ Validity: {expiryDate} days

    🤖 Bot: ANToNi Bots**"""
    user_id = f"{from_user.id}"
    await bot.send_message(user_id, msg)

about = f"""**🤖 My Name - [ANToNi](https://t.me/Antonitheottbot)
🏷️ Bot Version - v4.2.8-prerelease
📝 Language - [Python](https://python.org/)
📚 Library - [Pyrogram](http://Pyrogram.org/)
📡 Hosted on - [Google Cloud](https://console.cloud.google.com)
👨‍💻 Developer - [Iron Man](https://www.youtube.com/shorts/rxqAKn_VMXk)
📢 Updates Channel - [Tony](https://t.me/tony_091)
🕵️ Buy SubscriPtion - [Tony](https://t.me/tony_091)**"""

@Bot.on_callback_query(filters.regex(pattern="^(Help|usage|ContactUs|About|plans)$"))
async def callback(Client, CallbackQuery):
    if CallbackQuery.data == "About":
       await CallbackQuery.edit_message_text(text=about, reply_markup=InlineKeyboardMarkup(ST1), disable_web_page_preview=True)
    if CallbackQuery.data == "usage":
       user_id = CallbackQuery.from_user.id
       msg = await get_subscription(user_id, CallbackQuery)
       await CallbackQuery.edit_message_text(text=msg, reply_markup=InlineKeyboardMarkup(ST1), disable_web_page_preview=True)
    if CallbackQuery.data == "Help":
       await CallbackQuery.edit_message_text(text= f"""**Hi {CallbackQuery.from_user.mention} Here You Can Find All Available Commands →

/start - To start the bot
/help - To know how to use bot
/features - To see available features
/plans - To see available plans
/usage - To see your current usage
/otts - To know available otts**

`1. Send url (example.domain/File.mp4 | New Filename.mp4).
2. Send Image As Custom Thumbnail (Optional).
3. Select the button (Quality).`

**Just send me any DRM links from supported Otts to download that I can also upload to [Google Drive](https://drive.google.com/) or [Telegram](https://telegram.org/).

If bot didn't respond contact [Tony](https://t.me/tony_091)**""", reply_markup=InlineKeyboardMarkup(ST1), disable_web_page_preview=True)
 
    if CallbackQuery.data == "plans":
       await CallbackQuery.edit_message_text(text=f"""**🔰DRM WebDl Bot Plans🔰

👇INDIVIDUAL PLANS(All OTTs)👇

1. 99Rs/- Unlimited Downloads/1 Day 
2. 499Rs/- Unlimited Downloads/28 Days
3. 2000Rs/- Unlimited Downloads/365 Days[Limited]

⚠️Term and Conditions⚠️

• Payments are non-refundable, and we do not provide refunds. 
• If the service ceases to function, no compensation is provided.
•Payments Methods of Pakistan , Bangladesh , India are accepted.
• Other methods :- Paypal, Binance , crypto 

Contact to buy Subscription: [Tony](https://t.me/tony_091)**""", reply_markup=InlineKeyboardMarkup(ST1), disable_web_page_preview=True)
    if CallbackQuery.data == "ContactUs":
       await CallbackQuery.edit_message_text(text=f"**📞 Contact [Tony](https://t.me/tony_rd_jrr)**", reply_markup=InlineKeyboardMarkup(ST1), disable_web_page_preview=True)
        
@Bot.on_message(filters.command("start"))
async def start_handler(bot: Client, message: Message):
    await mydb.add_user(message.from_user.id)
    await db.add_user(message.from_user.id)
    IN = f"""**Hi {message.from_user.mention}! I am one and only DRM Downloader Bot on [Telegram](https://telegram.org/).

I can help you to download content from OTT Platforms

You can use me to Download DRM protected links to [Telegram](https://telegram.org/) & [Google Drive](https://drive.google.com/)

Here I support a vast number of otts from where you can download Drm or non-drm videos easily..

If You Found Any Issue Contact Support**"""
        
    await message.reply_text(text=IN, reply_markup=InlineKeyboardMarkup(ST1), disable_web_page_preview=True)                  

async def upload_to_gdrive(bot, input_str, sts_msg, message, userid):
    if os.path.isdir(input_str) and len(getListOfFiles(input_str)) == 0:
        return
    up_dir, up_name = input_str.rsplit('/', 1)
    userdata = await db.get_user(userid)
    cs_drive = userdata["cs_drive"]
    if cs_drive == "t":
        DRIVE_ID = userdata["Drive"]
    else:
        DRIVE_ID = Config.GDRIVE_FOLDER_ID
    print(DRIVE_ID)
    gdrive = GoogleDriveHelper(DRIVE_ID, up_name, up_dir, bot.loop, sts_msg)
    size = get_path_size(input_str)
    success = await sync_to_async(bot.loop, gdrive.upload, up_name, size)
    msg = sts_msg.reply_to_message if sts_msg.reply_to_message else sts_msg
    if success and isinstance(success, str):
        return
    if success:
        url_path = quote(f'{up_name}')
        share_url = f'{Config.INDEX_LINK}/{url_path}'
        if success[3] == "Folder":
            share_url += '/'
        sent = await msg.reply_text(
            f"""**File Name:** `{success[4]}`
**Size:** `{humanbytes(success[1])}`
**Type:** `{success[3]}`
**Total Files:** `{success[2]}`

**CC**: {message.from_user.mention}
""",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(text="🍺 Cloud Link", url=success[0]),
                InlineKeyboardButton(text="⚡ Index Link", url=share_url)]]
                                ),
            disable_web_page_preview=True
          )
        await sent.copy(chat_id=Config.LOG_CHANNEL)
    else:
        await msg.reply_text("Upload failed to gdrive")


@Bot.on_message(filters.command("gdrive") & static_auth_filter)
async def gdrive_Uploader_Handler(bot: Client, message: Message):
    try:
        input_str = message.text.split(" ", 1)[1]
        log.info("Gdrive UL request by " + str(message.from_user.id) + " for " + input_str)
        input_str = os.path.join(os.getcwd(), input_str)
    except:
        await message.reply_text("send along with file path")
        return
    userid = message.from_user.id
    userdata = await db.get_user(userid)
    cs_drive = userdata["cs_drive"]
    print(cs_drive)
    if cs_drive == "t":
        DRIVE_ID = userdata["Drive"]
    else:
        DRIVE_ID = Config.GDRIVE_FOLDER_ID
    await upload_to_gdrive(bot, input_str, message, message, DRIVE_ID)
        
@Bot.on_message(filters.command("unauth") & filters.user(Config.OWNER_ID))
async def tg_unauth_Handler(bot: Client, message: Message):
    if message.reply_to_message:
         user_id = message.reply_to_message.from_user.id
         from_user = message.reply_to_message.from_user
    else:
        try:
            user_id = message.text.split(" ", 1)[1]
            from_user = await bot.get_users(int(user_id))
        except:
            return await message.reply_text("send along with I'd or reply to user msg")
    try:
        user_id = int(user_id)
    except:
        return await message.reply_text("send along with I'd or reply to user msg")
    await mydb.delete_user(user_id)
    await message.reply_text(f"Now {from_user.id} can not use me")

@Bot.on_message(filters.command(["logs", "log"]) & filters.user(Config.OWNER_ID))
async def tg_unauth_Handler(bot: Client, message: Message):
    if os.path.exists("log.txt"):
        await message.reply_document("log.txt")
        return

@Bot.on_callback_query(filters.regex(pattern="^video"))
async def video_handler(bot: Client, query: CallbackQuery):
    global CHECK_ONCE
    _, key, video = query.data.split("#", 2)
    if query.from_user.id not in USER_DATA:
        await query.answer("You are not authorized to use this button.", show_alert=True)
        return
    check_user = await is_subscribed(query.from_user.id)
    if not check_user:
        await query.answer("You are not subscribed to use this bot.", show_alert=True)
        return
    if key not in USER_DATA[query.from_user.id]:
        await query.answer("Session expired, please try again.", show_alert=True)
        return 
    if key in USER_DATA[query.from_user.id]:
        if len(USER_DATA[query.from_user.id][key]["audios"]) == 0 and USER_DATA[query.from_user.id][key]["audios_count"] >= 2:
            await query.answer("No audio streams found, please try again.", show_alert=True)
            return
        drm_client = USER_DATA[query.from_user.id][key]
        if drm_client:
            list_audios = USER_DATA[query.from_user.id][key]["audios"]
            drm_client = USER_DATA[query.from_user.id][key]["client"]
            jvname = USER_DATA[query.from_user.id][key]["jvname"]
            file_pth = USER_DATA[query.from_user.id][key]["folder"]
            file_pth = os.path.join(Config.TEMP_DIR, file_pth)
            await query.message.edit("Please wait downloading in progress")
            rcode = await drm_client.downloader(video.strip(), list_audios, query.message)
            #await sts_.edit(f"Video downloaded in {file_pth}")
            upload_mode = await db.get_user(query.from_user.id)
            UL = upload_mode["ul_mode"]
            if UL == "t":
               mode = "telegram"
            else:
                mode = "Gdrive"
            
            try:
                await query.message.edit(f"Please wait starting **{mode}** upload of `{jvname}`")
                sts = query.message
            except:
                sts = await query.message.reply_text(f"**Please wait starting {mode} upload of** `{jvname}`")
            if UL == "g":
                for fileP in os.listdir(file_pth):
                    if "_jv_drm" in fileP or "srt" in fileP or "_jv_" in fileP:
                        os.remove(fileP)
                        continue
                    else:
                        await upload_to_gdrive(bot, os.path.join(file_pth, fileP), sts, query, query.from_user.id)
                try:
                    await sts.delete()
                except:
                    pass
            else:
                await upload_handler(file_pth, query.from_user.id, sts, query)
                try:
                    await sts.delete()
                except:
                    pass
            await mydb.set_user(user_id=query.from_user.id, balance = 0 - drm_client.COUNT_VIDEOS)
            if os.path.exists(file_pth):
                shutil.rmtree(file_pth)
            #await query.message.edit("Error occured, contact @Jigarvarma2005 for fixing.")
        else:
            await query.answer("Session expired, please try again.", show_alert=True)
        try:
            CHECK_ONCE.remove(query.from_user.id)
        except:
            pass

@Bot.on_message(filters.command("js"))
async def js(bot, msg):
    await msg.reply_text(msg.reply_to_message)

@Bot.on_callback_query(filters.regex(pattern="^audio"))
async def audio_handler(bot: Client, query: CallbackQuery):
    _, key, audio = query.data.split("#", 2)
    if query.from_user.id not in USER_DATA:
        await query.answer("You are not authorized to use this button.", show_alert=True)
        return
    if key not in USER_DATA[query.from_user.id]:
        await query.answer("Session expired, please try again.", show_alert=True)
        return 
    if audio=="process":
        if key in USER_DATA[query.from_user.id]:
            videos_q = await USER_DATA[query.from_user.id][key]["client"].get_videos_ids()
            markup = create_buttons(list([key]+videos_q), True)
            #log.info(str(markup))
            await query.edit_message_text(f"**Choose Quality:**", reply_markup=markup)
    else:
        audio, coice = audio.split("|", 1)
        if coice == "1":
            USER_DATA[query.from_user.id][key]["audios"].append(audio.strip())
            markup = MakeCaptchaMarkup(query.message.reply_markup.inline_keyboard, query.data, f"✓{LANGUAGE_SHORT_FORM.get(audio.lower(), audio)}")
        if coice == "0":
            USER_DATA[query.from_user.id][key]["audios"].remove(audio.strip())
            markup = MakeCaptchaMarkup(query.message.reply_markup.inline_keyboard, query.data, f"{LANGUAGE_FULL_FORM.get(audio.lower(), audio)}")
        await query.message.edit_reply_markup(InlineKeyboardMarkup(markup))

async def drm_dl_client(update, MpdUrl, command, sts_msg):
    try:
        user_fol = str(time())
        xcodec = ""
        met = ""
        msg = update.from_user.id
        MpdUrl = MpdUrl.replace(" -s ", ":", 1).replace(" -e ", ":", 1)
        if " " in MpdUrl:
            M = MpdUrl.split()
            MpdUrl = M[0]
            xcodec = M[1]
        xcodec = xcodec.lower()
        if "jiocinema" in MpdUrl or "jc" in command:
            if xcodec == "":
                xcodec = "dolby"
            drm_client: JioCinema = JioCinema(MpdUrl, user_fol, msg, xcodec)
        elif "hotstar" in MpdUrl or "hs" in command:
            available_xcodec = ["x264", "x265", "4k", ""]
            if met == "":
                met = "aria"
            if xcodec.split("-", 1)[0] not in available_xcodec:
                return await sts_msg.edit(f"{xcodec} not found, please send cmd with correct codec\n\n{', '.join(available_xcodec)}\n\nAdd -a in codec for dolby5.1\nadd -d in codec for atmos\n\neg: x265-a")
            token = await db.get_hstoken()
            drm_client: HotStar = HotStar(MpdUrl, user_fol, msg, token, xcodec, met)
        elif "sonyliv" in MpdUrl or "sl" in command:
            available_xcodec = ["dolby", "x264", "x265", ""]
            if xcodec not in available_xcodec:
                return await sts_msg.edit(f"{xcodec} not found, please send cmd with correct codec\n\n{', '.join(available_xcodec)}")
            drm_client: SONYLIV = SONYLIV(MpdUrl, user_fol, msg, xcodec)
        elif "sunnxt" in MpdUrl or "sn" in command:
            if xcodec == "":
                xcodec = "dolby"
            drm_client: SUNNXT = SUNNXT(MpdUrl, user_fol, msg, xcodec)
        elif "dangalplay" in MpdUrl:
            drm_client: DANGALPLAY = DANGALPLAY(MpdUrl, user_fol, msg)
        else:
            if xcodec == "":
                xcodec = "x264"
            token = await db.get_z5token()
            drm_client: Zee5 = Zee5(MpdUrl, user_fol, msg, token, xcodec)
        title = await drm_client.get_input_data()
        if isinstance(title, tuple):
            title, is_done = title
            if not is_done:
                return await sts_msg.edit(title)
        randStr = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
        #passing the randStr to use it as a key for the USER_DATA dict
        user_choice_list = await drm_client.get_audios_ids(randStr)
        USER_DATA[update.from_user.id] = {}
        USER_DATA[update.from_user.id][randStr] = {}
        USER_DATA[update.from_user.id][randStr]["client"] = drm_client
        USER_DATA[update.from_user.id][randStr]["audios"] = []
        USER_DATA[update.from_user.id][randStr]["audios_count"] = len(user_choice_list)
        USER_DATA[update.from_user.id][randStr]["folder"] = user_fol
        USER_DATA[update.from_user.id][randStr]["jvname"] = title
        my_buttons = create_buttons(user_choice_list)
        await update.reply_text(f"**Choose Audios for `{title}`: **", reply_markup=my_buttons)
        await sts_msg.delete()
    except Exception as e:
        log.exception(e)
        await sts_msg.edit("`Failed to fetch data from server.`")
    finally:
        try:
            CHECK_ONCE.remove(update.from_user.id)
        except:
            pass

@Bot.on_message(filters.command(["dl", "jc"], prefixes=["/", "."]) & static_auth_filter)
async def main_handler(bot: Client, m: Message):
    global CHECK_ONCE
    await db.add_user(m.from_user.id)
    if m.from_user.id in CHECK_ONCE:
        return await m.reply_text("Your a task already going on, so please wait....\n\nThis method was implemented to reduce the overload on bot. So please cooperate with us.")
    command, user_iput = m.text.split(" ", 1) 
  #  CHECK_ONCE.append(m.from_user.id)
    #print(CHECK_ONCE)
    sts_msg = await m.reply_text(f"`[+]` **Extracting Data ⌛ ...**\n`[+]` URL: `{user_iput}`")
    if "zee5" in user_iput or "zee5" in command or "dl" in command or "jiocinema" in user_iput or "jiocinema.com" in user_iput or "hotstar" in user_iput or "hs" in command or "pv" in command or "primevideo" in user_iput or "sonyliv" in user_iput or "sl" in command or "sn" in command or "sunnxt" in user_iput or "lionsgateplay" in user_iput or "lpg" in command or "manoramamax" in user_iput or "mxplayer" in user_iput or "aha" in user_iput or "minitv" in user_iput or "tentkotta" in user_iput or "dangalplay" in user_iput or "discoveryplus" in user_iput or "atrangii" in user_iput or "tataplay" in user_iput or "hulu" in user_iput or "simplysouth" in user_iput or "shemaroome" in user_iput:
        return await drm_dl_client(m, user_iput.strip(), command, sts_msg)
    else:
        m.reply_text("** Error NOT FOUND**")

def DownLoadFile(url):
    if not os.path.exists("Thumbs"):
        os.makedirs("Thumbs", exist_ok=True)
    n = str(time()) + ".jpg"
    file_name = os.path.join("Thumbs", n)
    r = requests.get(url, allow_redirects=True, stream=True)
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    return file_name

async def get_user_thumb(user_data, stream=False):
    if user_data["thumb"] != "":
        return DownLoadFile(user_data["thumb"])
    else:
         return None
        
async def upload_handler(file_path:str, user_id, sts_msg, message):
    user_id = str(user_id)
    if os.path.isdir(file_path):
        all_files = getListOfFiles(file_path)
        for filePath in all_files:
            await upload_handler(filePath, user_id, sts_msg, message)
        try:
            #try to remove dir
            shutil.rmtree(file_path)
        except:
            pass
    if os.path.exists(file_path):
        file_name_ = os.path.basename(file_path)
        if os.path.getsize(file_path) > Config.TG_SPLIT_SIZE:
            d_f_s = humanbytes(os.path.getsize(file_path))
            await sts_msg.edit(
                "Telegram does not support uploading this file.\n"
                f"Detected File Size: {d_f_s}\n"
                "\n🤖 trying to split the file\n\n"
                f"File: `{file_name_}`"
            )
            splitted_dir = await split_large_files(file_path)
            listOfFile = os.listdir(splitted_dir)
            listOfFile.sort()
            num_of_files = len(listOfFile)
            await sts_msg.edit(
                f"Detected File Size: {d_f_s}\n"
                f"File: `{file_name_}`\n"
                f"Splited into {num_of_files} parts."
            )
            for entry in listOfFile:
                fullPath = os.path.join(splitted_dir, entry)
                await tg_uploader(fullPath, user_id, sts_msg, message)
            try:
                #try to remove dir
                shutil.rmtree(splitted_dir)
            except:
                pass
        else:
            await tg_uploader(file_path, user_id, sts_msg, message)
        #await sts_msg.delete()

async def tg_uploader(input_str, user_id, sts_msg, message):
    #block drm video
    if "_jv_drm" in input_str or ".srt" in input_str or "_jv" in input_str:
        try:
            os.remove()
        except:
            pass
        return
    current_time = time()
    if get_path_size(input_str) > 2147483648:
        client = User
    else:
        client = Bot
    userdata = await db.get_user(user_id)
    if userdata["as_stream"] == "t":
        as_stream = True
    else:
        as_stream = False
    thumb = await get_user_thumb(user_data=userdata, stream=as_stream)
    file_name = os.path.basename(input_str)
    my_caption = f"**Filename**: `{file_name}`"
   # my_caption += f"\n**CC**: {message.from_user.mention}"
    if check_is_streamable(file_name) and as_stream:
        try:
            duration = await get_video_duration(input_str)
        except:
            duration = None
     #   my_caption += f"\n**Duration**: `{TimeFormatter(duration)}`"
        if thumb is None:
            thumb = await take_ss(input_str)
        sent_msg = await client.send_video(chat_id=Config.LOG_CHANNEL,
                                video=input_str,
                                  thumb=thumb,
                                  caption=my_caption,
                                  duration=duration,
                                  progress=progress_for_pyrogram,
                                  progress_args=("Uploading",
                                                 sts_msg,
                                                 current_time,
                                                 file_name))
    elif check_is_audio(file_name) and as_stream:
        try:
            duration = await get_video_duration(input_str)
        except:
            duration = None
      #  my_caption += f"\n**Duration**: `{TimeFormatter(duration)}`"
        if thumb is None:
            thumb = take_ss(input_str)
        sent_msg = await client.send_audio(chat_id=Config.LOG_CHANNEL,
                                  audio=input_str,
                                  thumb=thumb,
                                  duration=duration,
                                  caption=my_caption,
                                  progress=progress_for_pyrogram,
                                  progress_args=("Uploading",
                                                 sts_msg,
                                                 current_time,
                                                 file_name))
    else:
        sent_msg = await client.send_document(chat_id=Config.LOG_CHANNEL,
                                  document=input_str,
                                  thumb=thumb,
                                  caption=my_caption,
                                  progress=progress_for_pyrogram,
                                  progress_args=("Uploading",
                                                 sts_msg,
                                                 current_time,
                                                 file_name))
    await Bot.copy_message(user_id, Config.LOG_CHANNEL, sent_msg.id)
    if thumb is None and thumb is not None:
        try:
            os.remove(thumb)
        except:
            pass
    
        
#dict of commands of linux alies for windows
async def StartBot():
    #install()
    print("starting My Bot")
    await Bot.start()
    if User:
        await User.start()
    print("----------Bot Started----------")
    await idle()
    await Bot.stop()
    if User:
        await User.stop()
    print("----------Bot Stopped----------")
    print("--------------BYE!-------------")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(StartBot())
