import os
from pyrogram import filters, Client
from sample_config import Config
import aiofiles
import aiohttp
from random import randint
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from googletrans import Translator as google_translator

translator = google_translator()

BOT_TOKEN = Config.BOT_TOKEN
BOT_ID = Config.BOT_ID

bot = Client("MizukiChat", bot_token=BOT_TOKEN, api_id=6,
             api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")
print("\nMizuki Chatbot Started!\n")


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                data = await resp.json()
            except:
                data = await resp.text()
    return data


@bot.on_message(filters.text & ~filters.private & ~filters.edited & ~filters.bot & ~filters.via_bot & ~filters.channel & ~filters.forwarded)
async def mizuki(client, message):
    chat_id = message.chat.id
    if not message.reply_to_message:
        message.continue_propagation()
    try:
        aibot = message.reply_to_message.from_user.id
    except:
        return
    if aibot != BOT_ID:
        message.continue_propagation()
    text = message.text

    if text.startswith("/") or text.startswith("@"):
        message.continue_propagation()
    try:
        lan = translator.detect(text)
    except:
        return
    test = text
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, lang_tgt="en")
        except:
            return
    finaltxt = test.replace(" ", "%20")
    try:
        L = await fetch(f"https://api.affiliateplus.xyz/api/chatbot?message={finaltxt}&botname=Mizuki&ownername=Jason&user=1")
        msg = L["message"]        
    except Exception as e:
        await m.edit(str(e))
        return
    if not "en" in lan and not lan == "":
        msg = translator.translate(msg, lang_tgt=lan[0])
    try:
        await bot.send_chat_action(message.chat.id, "typing")
        await message.reply(msg)
    except:
        return
    message.continue_propagation()

    
@bot.on_message(filters.command("start") & ~filters.edited)
async def start(client, message):
   if message.chat.type == 'private':
       await message.reply("**Hey There, I'm Mizuki. An advanced chatbot with AI. \n\nAdd me to your group and chat with me!**",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "Dev", url="https://t.me/MizukiUpdatesOfficial"),
                                        InlineKeyboardButton(
                                            "Repo", url="https://github.com/ImJanindu/Mizuki-Chat-Bot")
                                    ]]
                            ),               
           )
   else:

       await message.reply("**I'm alive, check my pm to know more about me!**")
   
  
bot.run()
