# Codeflix_Botz
# rohit_1888 on Tg

import motor, asyncio
import motor.motor_asyncio
import time
import pymongo, os
import difflib  # Spelling check ke liye zaroori
from config import DB_URI, DB_NAME
import logging
from datetime import datetime, timedelta

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

logging.basicConfig(level=logging.INFO)

default_verify = {
    'is_verified': False,
    'verified_time': 0,
    'verify_token': "",
    'link': ""
}

class Rohit:

    def __init__(self, DB_URI, DB_NAME):
        self.dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
        self.database = self.dbclient[DB_NAME]

        # Collections
        self.channel_data = self.database['channels']
        self.admins_data = self.database['admins']
        self.user_data = self.database['users']
        self.sex_data = self.database['sex']
        self.banned_user_data = self.database['banned_user']
        self.del_timer_data = self.database['del_timer']
        self.fsub_data = self.database['fsub']   
        self.rqst_fsub_Channel_data = self.database['request_forcesub_channel']
        
        # 🆕 Naya Collection Story Links ke liye
        self.story_links = self.database['story_links']

    # ==========================
    #   NEW: DIRECT REDIRECT & SPELLING LOGIC
    # ==========================

    async def add_story(self, keyword, channel_link):
        """Admin keyword aur channel link save karega"""
        await self.story_links.update_one(
            {"keyword": keyword.lower()},
            {"$set": {"keyword": keyword.lower(), "link": channel_link}},
            upsert=True
        )

    async def search_story(self, query):
        """Group mein search karne aur suggestion dene ke liye"""
        query = query.lower()
        
        # 1. Direct Match Check
        result = await self.story_links.find_one({"keyword": query})
        if result:
            return result, None
        
        # 2. Agar nahi mila toh "Did you mean" logic
        all_docs = await self.story_links.find({}, {"keyword": 1}).to_list(length=None)
        all_keywords = [d['keyword'] for d in all_docs]
        
        # Spelling match check (cutoff 0.6 = 60% match)
        suggestion = difflib.get_close_matches(query, all_keywords, n=1, cutoff=0.6)
        return None, suggestion[0] if suggestion else None

    # ==========================
    #   Aapka Purana Code (Waisa hi hai)
    # ==========================

    async def present_user(self, user_id: int):
        found = await self.user_data.find_one({'_id': user_id})
        return bool(found)

    async def add_user(self, user_id: int):
        if not await self.present_user(user_id):
            await self.user_data.insert_one({'_id': user_id})

    async def admin_exist(self, admin_id: int):
        found = await self.admins_data.find_one({'_id': admin_id})
        return bool(found)

    async def add_admin(self, admin_id: int):
        if not await self.admin_exist(admin_id):
            await self.admins_data.insert_one({'_id': admin_id})

    async def del_admin(self, admin_id: int):
        await self.admins_data.delete_one({'_id': admin_id})

    async def get_all_admins(self):
        docs = await self.admins_data.find().to_list(length=None)
        return [doc['_id'] for doc in docs]

    async def ban_user_exist(self, user_id: int):
        found = await self.banned_user_data.find_one({'_id': user_id})
        return bool(found)

    async def add_ban_user(self, user_id: int):
        if not await self.ban_user_exist(user_id):
            await self.banned_user_data.insert_one({'_id': user_id})

    async def del_ban_user(self, user_id: int):
        await self.banned_user_data.delete_one({'_id': user_id})

    async def show_channels(self):
        docs = await self.fsub_data.find().to_list(length=None)
        return [doc['_id'] for doc in docs]

    async def get_channel_mode(self, channel_id: int):
        data = await self.fsub_data.find_one({'_id': channel_id})
        return data.get("mode", "off") if data else "off"

    async def set_channel_mode(self, channel_id: int, mode: str):
        await self.fsub_data.update_one({'_id': channel_id}, {'$set': {'mode': mode}}, upsert=True)

    async def db_verify_status(self, user_id):
        user = await self.user_data.find_one({'_id': user_id})
        return user.get('verify_status', default_verify) if user else default_verify

    async def db_update_verify_status(self, user_id, verify):
        await self.user_data.update_one({'_id': user_id}, {'$set': {'verify_status': verify}})

    async def get_total_verify_count(self):
        pipeline = [{"$group": {"_id": None, "total": {"$sum": "$verify_count"}}}]
        result = await self.sex_data.aggregate(pipeline).to_list(length=1)
        return result[0]["total"] if result else 0

# Database Instance
db = Rohit(DB_URI, DB_NAME)
    
