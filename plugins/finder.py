from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.database import db 
from config import *

# Yahan 'Bot' ki jagah 'Client' use karein taaki handler sahi se register ho
@Client.on_message(filters.text & filters.group)
async def story_finder_logic(client, message):
    # 1. Jo user ne dhoondhne ke liye likha
    query = message.text.strip()

    # 2. Chhote words ko ignore karein (Faltu chatting se bot trigger nahi hoga)
    if len(query) < 3:
        return

    # 3. Database se results check karna
    try:
        results = await db.get_search_results(query)
    except Exception as e:
        print(f"Search Error: {e}")
        return

    # 4. SILENT CONDITION: Agar file mili tabhi reply jayega
    if results:
        buttons = []
        for file in results:
            f_name = file.get("file_name")
            f_id = file.get("file_id")

            # Audio Icon ke saath sunder button
            buttons.append([
                InlineKeyboardButton(
                    text=f"🎧 {f_name}", 
                    url=f"https://t.me/{client.username}?start={f_id}"
                )
            ])
        
        # --- MODEL LOOK REPLY ---
        ms = await message.reply_text(
            text=(
                f"<b>🔍 Sᴇᴀʀᴄʜ Rᴇsᴜʟᴛs Fᴏʀ:</b> <code>{query}</code>\n\n"
                f"<i>Niche di gayi list mein se apni story chunein. "
                "Yeh button aapko direct bot ke PM mein le jayega.</i>"
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        
        # OPTIONAL: Agar aap chahte hain ki ye message 2 minute baad delete ho jaye
        # await asyncio.sleep(120)
        # await ms.delete()
    
    # Agar kuch nahi mila, toh bot khamosh rahega (Silent Mode)
    return
