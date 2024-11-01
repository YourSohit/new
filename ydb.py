

import motor.motor_asyncio
import logging
_LOG = logging.getLogger(__name__)
from config import Config 

class manag_db():
    def __init__(self):
        try:
            DB_URL = "mongodb+srv://konakachiupender686:wiPbYcbHChC95cJa@cluster0.9oyhqhi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
            self.db = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)["MY_UPLOADER"]
            self.col = self.db.members
            self.time = self.db.timeGap
         #   print(self.col)
        except Exception as e:
          #  _LOG.exception(e)
            self.col = None
          #  print(self.col)
    
    def member_dict(self, userid: int) -> dict:
        return dict(_id=userid,
                    as_stream="t",
                    unzip="f",
                    caption="",
                    ul_mode="t", mkv="mkv",
                    thumb="", format="t", Drive="", cs_drive="f")
    
    async def set_caption(self, userid: int, caption: str):
        await self.col.update_one({"_id": int(userid)}, {'$set': {'caption': caption}})

    async def set_stream(self, userid: int, as_stream: str):
        await self.col.update_one({"_id": int(userid)}, {'$set': {'as_stream': as_stream}})

    async def set_caption(self, userid: int, cap: str):
        await self.col.update_one({"_id": int(userid)}, {'$set': {'format': cap}})
   
    async def cs_drive(self, userid: int, cap: str):
        await self.col.update_one({"_id": int(userid)}, {'$set': {'cs_drive': cap}})
    
    async def set_unzip(self, userid: int, as_unzip: str):
        await self.col.update_one({"_id": int(userid)}, {'$set': {'unzip': as_unzip}})
    
    async def set_show_filename(self, userid: int, show_filename: str):
        await self.col.update_one({"_id": int(userid)}, {'$set': {'filename': show_filename}})

    async def set_thumb(self, userid: int, thumburl: str):
        await self.col.update_one({"_id": int(userid)}, {'$set': {'thumb': thumburl}})

    async def set_drive(self, userid: int, thumburl: str):
        await self.col.update_one({"_id": int(userid)}, {'$set': {'Drive': thumburl}})

    async def add_user(self, id):
        try:
            await self.col.insert_one(self.member_dict(int(id)))
            return True
        except Exception as e:
            #_LOG.exception(e)
            return False

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return True if user else False
    
    async def get_user(self, id):
        user = await self.col.find_one({'_id': int(id)})
      #  print(user)
        return user if user else None

    
    async def set_ul_mode(self, user_id, ul_mode):
        await self.col.update_one({"_id": user_id}, {'$set': {'ul_mode': ul_mode}})
    
    async def get_ul_mode(self, user_id):
        userkey = await self.col.find_one({'_id': user_id})
        if userkey:
            return userkey["ul_mode"]
        else:
            return "gdrive"

    async def set_tk(self, token):
        try:
            await self.col.insert_one({"_id": "tk", "token": token})
        except:
            await self.col.update_one({"_id": "tk"}, {'$set': {'token': token}})

    async def get_tktoken(self):
        userkey = await self.col.find_one({'_id': "tk"})
        if userkey:
            return userkey["token"]
        else:
            return False
            
    async def set_hs(self, token):
        try:
            await self.col.insert_one({"_id": "hs", "token": token})
        except:
            await self.col.update_one({"_id": "hs"}, {'$set': {'token': token}})

    async def get_hstoken(self):
        userkey = await self.col.find_one({'_id': "hs"})
        if userkey:
            return userkey["token"]
        else:
            return False

    async def set_z5(self, token):
        try:
            await self.col.insert_one({"_id": "z5", "token": token})
        except:
            await self.col.update_one({"_id": "z5"}, {'$set': {'token': token}})

    async def get_z5token(self):
        userkey = await self.col.find_one({'_id': "z5"})
        if userkey:
            return userkey["token"]
        else:
            return False
   
    async def set_for(self, user_id, mkv):
        await self.col.update_one({"_id": user_id}, {'$set': {'mkv': mkv}})
    
    async def get_TimeGap(self, id):
        user = await self.time.find_one({'_id': int(id)})
        if user:
            return user["time"]
        else:
            return False
    
    async def set_TimeGap(self, id, timei):
        await self.time.insert_one({"_id": id, "time": timei})

    async def del_TimeGap(self, id):
        await self.time.delete_many({"_id": id})

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    
    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users
    
    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})
