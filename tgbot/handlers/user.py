import logging
import time
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart, Text
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from db import Users
from tgbot.keyboards.states import States

user_router = Router()



@user_router.message(CommandStart())
async def user_start(m: Message, dialog_manager: DialogManager):
    reg_time = datetime.now()
    user_id = m.from_user.id
    user_name = m.from_user.username
    user_data = Users.get_user(user_id)
    logging.info(user_data)
    dialog_data = {
        "reg_time": reg_time,
        "user_id": user_id,
        "user_name": user_name,
        "user_lang": user_data[2] if user_data else None
    }
    if user_data is None:
        Users.add_user(user_id, user_name, None, reg_time)
    else:
        Users.add_user(user_id, user_name, user_data[2], reg_time)
    await m.reply("Hello user!")
    await dialog_manager.start(
        States.main_menu_state,
        data=dialog_data,
        mode=StartMode.RESET_STACK,
    )



@user_router.message(Text('Back'))
async def user_start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        States.main_menu_state,
        mode=StartMode.RESET_STACK,
    )
