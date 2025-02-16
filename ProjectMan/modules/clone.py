# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import os

from pyrogram import *
from pyrogram.types import *

from config import CMD_HANDLER as cmd
from ProjectMan.helpers.basic import edit_or_reply, get_text, get_user

from .help import *

OWNER = os.environ.get("OWNER", None)
BIO = os.environ.get("BIO", "404 : Bio Lost")


def get_user(message, text):
    # Implement your logic to extract the user ID from the message and text
    # This is a placeholder implementation; adjust as needed
    if text:
        # Example: assuming the user ID is mentioned in the text
        user_id = text.split()[1]  # Adjust this logic based on your command structure
        return user_id
    return None


@ubot.on_message(filters.command("clone", PREFIX) & filters.me)
async def clone(client: Client, message: Message):
    text = get_text(message)  # Assuming this function extracts the text from the message
    op = await edit_or_reply(message, "`Cloning`")
    
    # Extract user ID from the message text
    userk = get_user(message, text)  # Assuming get_user returns a user ID or None
    if not userk:
        await op.edit("`Whom should I clone?`")
        return

    try:
        user_ = await client.get_users(userk)
    except Exception as e:
        await op.edit("`Error fetching user.`")
        return

    if not user_:
        await op.edit("`Whom should I clone?`")
        return

    get_bio = await client.get_chat(user_.id)
    f_name = user_.first_name
    c_bio = get_bio.bio if get_bio.bio else "No bio available."  # Handle case where bio might be None
    pic = user_.photo.big_file_id if user_.photo else None  # Check if user has a photo

    if pic:
        poto = await client.download_media(pic)
        await client.set_profile_photo(photo=poto)

    await client.update_profile(
        first_name=f_name,
        bio=c_bio,
    )
    await message.edit(f"**From now I'm** __{f_name}__")



@Client.on_message(filters.command("revert", cmd) & filters.me)
async def revert(client: Client, message: Message):
    await message.edit("`Reverting`")
    r_bio = BIO

    # Get ur Name back
    await client.update_profile(
        first_name=OWNER,
        bio=r_bio,
    )
    # Delte first photo to get ur identify
    photos = [p async for p in client.get_chat_photos("me")]
    await client.delete_profile_photos(photos[0].file_id)
    await message.edit("`I am back!`")


add_command_help(
    "clone",
    [
        ["clone", "To Clone someone Profile."],
        ["revert", "To Get Your Account Back."],
    ],
)
