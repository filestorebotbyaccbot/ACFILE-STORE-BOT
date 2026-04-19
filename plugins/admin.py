import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import *
from database.database import db 

# --- COMMAND TO ADD ADMINS ---
@Bot.on_message(filters.command('add_admin') & filters.private & filters.user(OWNER_ID))
async def add_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>⌛ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    admin_ids = await db.get_all_admins()
    admins = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])

    if not admins:
        return await pro.edit(
            "<b>❌ Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ Usᴇʀ ID(s).</b>\n\n"
            "<b>Usage:</b> <code>/add_admin 12345678</code>",
            reply_markup=reply_markup
        )

    admin_list = ""
    check = 0
    for id in admins:
        try:
            user_id = int(id)
            if user_id in admin_ids:
                admin_list += f"<blockquote><b>ID <code>{user_id}</code> is already an Admin.</b></blockquote>\n"
            else:
                await db.add_admin(user_id)
                admin_list += f"<b><blockquote>✅ ID: <code>{user_id}</code> Added Successfully.</blockquote></b>\n"
                check += 1
        except ValueError:
            admin_list += f"<blockquote><b>❌ Invalid ID: <code>{id}</code></b></blockquote>\n"

    await pro.edit(f"<b>⚡ Admin Management Result:</b>\n\n{admin_list}", reply_markup=reply_markup)

# --- COMMAND TO DELETE ADMINS ---
@Bot.on_message(filters.command('deladmin') & filters.private & filters.user(OWNER_ID))
async def delete_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>⌛ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    admin_ids = await db.get_all_admins()
    admins = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])

    if not admins:
        return await pro.edit("<b>❌ Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ Usᴇʀ ID ᴛᴏ ʀᴇᴍᴏᴠᴇ.</b>", reply_markup=reply_markup)

    passed = ""
    for admin_id in admins:
        try:
            id = int(admin_id)
            if id in admin_ids:
                await db.del_admin(id)
                passed += f"<blockquote><b>🗑️ ID: <code>{id}</code> Removed.</b></blockquote>\n"
            else:
                passed += f"<blockquote><b>⚠️ ID <code>{id}</code> not found in list.</b></blockquote>\n"
        except:
            passed += f"<blockquote><b>❌ Invalid ID: <code>{admin_id}</code></b></blockquote>\n"

    await pro.edit(f"<b>⛔ Admin Removal Result:</b>\n\n{passed}", reply_markup=reply_markup)

# --- COMMAND TO LIST ADMINS ---
@Bot.on_message(filters.command('admins') & filters.private & admin)
async def get_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>⌛ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..</i></b>", quote=True)
    admin_ids = await db.get_all_admins()

    if not admin_ids:
        admin_list = "<b><blockquote>❌ No Admins Found.</blockquote></b>"
    else:
        admin_list = "\n".join(f"<b><blockquote>👤 ID: <code>{id}</code></blockquote></b>" for id in admin_ids)

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]])
    await pro.edit(f"<b>⚡ Current Admin List:</b>\n\n{admin_list}", reply_markup=reply_markup)
