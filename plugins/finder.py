from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.database import db 

@Client.on_message(filters.text & filters.group)
async def story_finder(client, message):
    query = message.text.strip().lower()
    if len(query) < 3: return # Chote words ignore karein

    result, suggestion = await db.search_story(query)

    if result:
        # ✅ Sahi naam likha toh seedha button
        buttons = [[InlineKeyboardButton("📖 OPEN STORY", url=result['link'])]]
        await message.reply_text(
            f"<b>✅ Story Mil Gayi!</b>\n\nNiche button par click karke dekhein.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    
    elif suggestion:
        # 💡 Ulta-seedha naam likha toh suggestion (Did you mean)
        # Is button par click karte hi sahi spelling likh jayegi
        buttons = [[InlineKeyboardButton(f"Sᴇᴀʀᴄʜ Fᴏʀ: {suggestion.upper()} 🔍", switch_inline_query_current_chat=suggestion)]]
        await message.reply_text(
            f"<b>❌ '{query}' nahi mila.</b>\n\nKya aapka matlab tha: <code>{suggestion}</code>?",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
