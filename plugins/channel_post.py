import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from bot import Bot
from config import *
from helper_func import encode, admin
from database.database import db 

@Bot.on_message(filters.private & admin & ~filters.command(['start', 'commands','users','broadcast','batch', 'custom_batch', 'genlink','stats', 'dlt_time', 'check_dlt_time', 'dbroadcast', 'ban', 'unban', 'banlist', 'addchnl', 'delchnl', 'listchnl', 'fsub_mode', 'pbroadcast', 'add_admin', 'deladmin', 'admins', 'addpremium', 'premium_users', 'remove_premium', 'myplan', 'count', 'delreq']))
async def channel_post(client: Client, message: Message):
    # Sirf media files ko handle karega
    if not (message.document or message.video or message.audio):
        return

    reply_text = await message.reply_text("<b>⌛ Pʀᴏᴄᴇssɪɴɢ Yᴏᴜʀ Fɪʟᴇ...</b>", quote=True)
    
    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        await reply_text.edit_text(f"<b>❌ Eʀʀᴏʀ:</b> {e}")
        return

    # File ka naam nikalna
    file_name = message.document.file_name if message.document else (message.video.file_name if message.video else message.audio.file_name)
    if not file_name:
        file_name = "Audio Story File"

    # Unique Link banana
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    
    # 💾 Database mein save (Indexing)
    try:
        await db.database['files'].update_one(
            {"file_id": base64_string},
            {"$set": {"file_name": file_name, "msg_id": post_message.id}},
            upsert=True
        )
    except Exception as e:
        print(f"DB Save Error: {e}")

    # Bot ka link
    bot_link = f"https://t.me/{client.username}?start={base64_string}"

    # --- MODEL LOOK BUTTONS ---
    buttons = [
        [
            InlineKeyboardButton("🚀 Gᴇᴛ Fɪʟᴇ Lɪɴᴋ", url=bot_link),
            InlineKeyboardButton("📢 Sʜᴀʀᴇ", url=f"https://telegram.me/share/url?url={bot_link}")
        ],
        [
            InlineKeyboardButton("🗑️ Dᴇʟᴇᴛᴇ Fɪʟᴇ (Admin)", callback_data=f"delete_file_{base64_string}")
        ]
    ]

    # --- FINAL MESSAGE (Model Style) ---
    final_text = (
        "<b>✅ Fɪʟᴇ Iɴᴅᴇxᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!</b>\n\n"
        f"<b>📝 Nᴀᴍᴇ:</b> <code>{file_name}</code>\n"
        f"<b>🆔 ID:</b> <code>{base64_string}</code>\n\n"
        "<i>Ab yeh file database mein save ho gayi hai aur group search mein mil jayegi.</i>"
    )

    await reply_text.edit(text=final_text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
