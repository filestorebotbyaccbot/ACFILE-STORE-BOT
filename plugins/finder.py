from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot  # Agar aapka bot instance 'Bot' naam se hai
from database.database import db 

@Bot.on_message(filters.text & filters.group)
async def story_finder(client, message):
    # 1. User ka message uthao aur clean karo
    query = message.text.strip().lower()
    
    # 2. 3 akshar se chhote words ko ignore karo (jaise 'hi', 'ok')
    if len(query) < 3: 
        return 

    # 3. Database se search aur suggestion mangwao
    # (Ye functions humne database.py mein pehle hi add kar diye hain)
    result, suggestion = await db.search_story(query)

    if result:
        # ✅ CASE 1: Agar sahi naam likha (Direct Redirect Button)
        buttons = [[InlineKeyboardButton("📖 OPEN STORY", url=result['link'])]]
        
        await message.reply_text(
            f"<b>✅ Result Found: {query.capitalize()}</b>\n\n"
            "Niche diye gaye button par click karke story par jayein.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    
    elif suggestion:
        # 💡 CASE 2: Agar spelling galat hai (Did you mean feature)
        # Is button par click karte hi sahi spelling search ho jayegi
        buttons = [[
            InlineKeyboardButton(
                text=f"Sᴇᴀʀᴄʜ Fᴏʀ: {suggestion.upper()} 🔍", 
                switch_inline_query_current_chat=suggestion
            )
        ]]
        
        await message.reply_text(
            f"<b>❌ '{query}' nahi mila.</b>\n\n"
            f"Kya aapka matlab tha: <code>{suggestion}</code>?",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        
