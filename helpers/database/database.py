from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pyrogram.types import CallbackQuery
from config import *
from __init__ import LOGGER, MERGE_MODE
import datetime
import motor.motor_asyncio


class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.grp = self.db.groups

async def isuser_exist(uid):
    a = Database.mergebot.isuser_exist.find_one({"_id": uid})
    try:
        if uid == a["_id"]:
            return True
    except TypeError:
        return False
    
async def addUser(uid, fname, lname):
    try:
        userDetails = {
            "_id": uid,
            "name": f"{fname} {lname}",
        }
        Database.mergebot.users.insert_one(userDetails)
        LOGGER.info(f"Nᴇᴡ ᴜsᴇʀ ᴀᴅᴅᴇᴅ ɪᴅ={uid}\n{fname} {lname} \n")
    except DuplicateKeyError:
        LOGGER.info(f"Dᴜᴘʟɪᴄᴀᴛᴇ ᴇɴᴛʀʏ ғᴏᴜɴᴅ ғᴏʀ ɪᴅ={uid}\n{fname} {lname} \n")
    return


async def broadcast():
    a = Database.mergebot.mergeSettings.find({})
    return a


async def allowUser(uid, fname, lname):
    try:
        a = Database.mergebot.allowedUsers.insert_one(
            {
                "_id": uid,
            }
        )
    except DuplicateKeyError:
        LOGGER.info(f"Dᴜᴘʟɪᴄᴀᴛᴇ ᴇɴᴛʀʏ ғᴏᴜɴᴅ ғᴏʀ ɪᴅ={uid}\n{fname} {lname} \n")
    return


async def allowedUser(uid):
    a = Database.mergebot.allowedUsers.find_one({"_id": uid})
    try:
        if uid == a["_id"]:
            return True
    except TypeError:
        return False


async def saveThumb(uid, fid):
    try:
        Database.mergebot.thumbnail.insert_one({"_id": uid, "thumbid": fid})
    except DuplicateKeyError:
        Database.mergebot.thumbnail.replace_one({"_id": uid}, {"thumbid": fid})


async def delThumb(uid):
    Database.mergebot.thumbnail.delete_many({"_id": uid})
    return True


async def getThumb(uid):
    res = Database.mergebot.thumbnail.find_one({"_id": uid})
    return res["thumbid"]


async def deleteUser(uid):
    Database.mergebot.mergeSettings.delete_many({"_id": uid})


async def addUserRcloneConfig(cb: CallbackQuery, fileId):
    try:
        await cb.message.edit("Aᴅᴅɪɴɢ ғɪʟᴇ ᴛᴏ DB")
        uid = cb.from_user.id
        Database.mergebot.rcloneData.insert_one({"_id": uid, "rcloneFileId": fileId})
    except Exception as err:
        LOGGER.info("Uᴘᴅᴀᴛɪɴɢ ʀᴄʟᴏɴᴇ")
        await cb.message.edit("Uᴘᴅᴀᴛɪɴɢ ғɪʟᴇ ɪɴ DB")
        uid = cb.from_user.id
        Database.mergebot.rcloneData.replace_one({"_id": uid}, {"rcloneFileId": fileId})
    await cb.message.edit("Done")
    return


async def getUserRcloneConfig(uid):
    try:
        res = Database.mergebot.rcloneData.find_one({"_id": uid})
        return res["rcloneFileId"]
    except Exception as err:
        return None


def getUserMergeSettings(uid: int):
    try:
        res_cur = Database.mergebot.mergeSettings.find_one({"_id": uid})
        return res_cur
    except Exception as e:
        LOGGER.info(e)
        return None


def setUserMergeSettings(uid: int, name: str, mode, edit_metadata, banned, allowed, thumbnail):
    modes = Config.MODES
    if uid:
        try:
            Database.mergebot.mergeSettings.insert_one(
                document={
                    "_id": uid,
                    "name": name,
                    "user_settings": {
                        "merge_mode": mode,
                        "edit_metadata": edit_metadata,
                    },
                    "isAllowed": allowed,
                    "isBanned": banned,
                    "thumbnail": thumbnail,
                }
            )
            LOGGER.info("Usᴇʀ {} Moᴅᴇ ᴜᴘᴅᴀᴛᴇᴅ ᴛᴏ {}".format(uid, modes[mode - 1]))
        except Exception:
            Database.mergebot.mergeSettings.replace_one(
                filter={"_id": uid},
                replacement={
                    "name": name,
                    "user_settings": {
                        "merge_mode": mode,
                        "edit_metadata": edit_metadata,
                    },
                    "isAllowed": allowed,
                    "isBanned": banned,
                    "thumbnail": thumbnail,
                },
            )
            LOGGER.info("Usᴇʀ {} Moᴅᴇ ᴜᴘᴅᴀᴛᴇᴅ ᴛᴏ {}".format(uid, modes[mode - 1]))
        MERGE_MODE[uid] = mode
    # elif mode == 2:
    #     try:
    #         Database.mergebot.mergeModes.insert_one(
    #             document={"_id": uid, modes[0]: 0, modes[1]: 1, modes[2]: 0}
    #         )
    #         LOGGER.info("User {} Mode updated to {}".format(uid, modes[1]))
    #     except Exception:
    #         rep = Database.mergebot.mergeModes.replace_one(
    #             filter={"_id": uid},
    #             replacement={modes[0]: 0, modes[1]: 1, modes[2]: 0},
    #         )
    #         LOGGER.info("User {} Mode updated to {}".format(uid, modes[1]))
    #     MERGE_MODE[uid] = 2
    #     # Database.mergebot.mergeModes.delete_many({'id':uid})
    # elif mode == 3:
    #     try:
    #         Database.mergebot.mergeModes.insert_one(
    #             document={"_id": uid, modes[0]: 0, modes[1]: 0, modes[2]: 1}
    #         )
    #         LOGGER.info("User {} Mode updated to {}".format(uid, modes[2]))
    #     except Exception:
    #         rep = Database.mergebot.mergeModes.replace_one(
    #             filter={"_id": uid},
    #             replacement={modes[0]: 0, modes[1]: 0, modes[2]: 1},
    #         )
    #         LOGGER.info("User {} Mode updated to {}".format(uid, modes[2]))
    #     MERGE_MODE[uid]=3
    LOGGER.info(MERGE_MODE)


def enableMetadataToggle(uid: int, value: bool):

    1


def disableMetadataToggle(uid: int, value: bool):
    1

db = Database(Config.DATABASE_URI, Config.SESSION_NAME)
