from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.database import db # Aapka database variable
from config import *

@Bot.on_message(filters.text & filters.group)
async def story_finder_logic(client, message):
    # Jo user ne text bheja hai
    query = message.text.strip()

    # Agar user sirf 'hi', 'hello' ya 2 akshar likhe toh ignore karo
    if len(query) < 3:
        return

    # Database se audio story search mangwana
    results = await db.get_search_results(query)

    # SEEDHI BAAT: Agar database mein files hain tabhi reply jayega
    if results:
        buttons = []
        for file in results:
            f_name = file.get("file_name")
            f_id = file.get("file_id") # File ki unique ID

            # Audio story ke liye button
            buttons.append([
                InlineKeyboardButton(
                    text=f"🎧 {f_name}", 
                    url=f"https://t.me/{client.username}?start={f_id}"
                )
            ])
        
        # Sirf tabhi message jayega jab story milengi
        await message.reply_text(
            text=f"**Mujhe ye Audio Stories mili hain:**\n\nSearch: `{query}`",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    
    # Agar files nahi mili toh bot 'return' ho jayega (Silent Mode)
    return

