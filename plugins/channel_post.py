# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport
#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from bot import Bot
from config import *
from helper_func import encode, admin
from database.database import db # Database import kiya

@Bot.on_message(filters.private & admin & ~filters.command(['start', 'commands','users','broadcast','batch', 'custom_batch', 'genlink','stats', 'dlt_time', 'check_dlt_time', 'dbroadcast', 'ban', 'unban', 'banlist', 'addchnl', 'delchnl', 'listchnl', 'fsub_mode', 'pbroadcast', 'add_admin', 'deladmin', 'admins', 'addpremium', 'premium_users', 'remove_premium', 'myplan', 'count', 'delreq']))
async def channel_post(client: Client, message: Message):
    # Sirf media files (Audio, Video, Document) ko handle karne ke liye
    if not (message.document or message.video or message.audio):
        return

    reply_text = await message.reply_text("<b>Processing and Indexing... Please Wait!</b>", quote = True)
    
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(f"Forward Error: {e}")
        await reply_text.edit_text("Something went Wrong..!")
        return

    # File Details nikalna search ke liye
    file_name = ""
    if message.document: file_name = message.document.file_name
    elif message.video: file_name = message.video.file_name or "Video File"
    elif message.audio: file_name = message.audio.file_name or "Audio File"

    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    
    # 🔥 ZAROORI: Database mein file ko save karna taaki Search kaam kare
    try:
        # Hum wahi collection use karenge jo database.py mein banaya tha
        await client.database['files'].update_one(
            {"file_id": base64_string},
            {"$set": {"file_name": file_name, "msg_id": post_message.id}},
            upsert=True
        )
    except Exception as e:
        print(f"DB Save Error: {e}")

    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

    await reply_text.edit(f"<b>✅ File Indexed Successfully!</b>\n\n<b>Name:</b> <code>{file_name}</code>\n\n<b>Link:</b> {link}", reply_markup=reply_markup, disable_web_page_preview = True)

    if not DISABLE_CHANNEL_BUTTON:
        try:
            await post_message.edit_reply_markup(reply_markup)
        except:
            pass

