import logging
import time
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart, Text, CommandObject
from aiogram.types import Message, InlineQuery
from aiogram_dialog import DialogManager, StartMode

from db import Users
from tgbot.keyboards.states import States

user_router = Router()



# @user_router.inline_query(lambda query: query.startswith('start='))
# async def inline_start_handler(query: InlineQuery):

@user_router.message(CommandStart(deep_link=True))
async def user_dl_start(m: Message, command: CommandObject, dialog_manager: DialogManager):
    parameter = command.args
    logging.info(parameter)
    reg_time = datetime.now()
    user_id = m.from_user.id
    user_name = m.from_user.username
    user_data = Users.get_user(user_id)
    friend = Users.find_user_by_key(parameter)
    logging.info(user_data)
    dialog_data = {
        "reg_time": reg_time,
        "user_id": user_id,
        "user_name": user_name,
        "access_key": user_data[3] if user_data else None,
        "user_balance": user_data[4] if user_data else 0,
    }
    if friend:
        Users.referral_bonus(parameter)
        if user_data is None:
            Users.add_user(user_id, user_name, None, 0, reg_time)
        Users.update_access_key(user_id, parameter)
        user_key = Users.get_user(user_id)[2]
        await m.reply(f"Access granted! Congratulations!!! - {user_name}!"
                      f"\nYou was recommended to Our Shop_bot by user - {friend[2]}"
                      f"\nPlease find below Your referral link that You can share with Your friends to get 10 extra points!"
                      f"\nhttps://t.me/Clstl_bot?start={user_key}", parse_mode="HTML")

        await dialog_manager.start(
            States.main_menu_state,
            data=dialog_data,
            mode=StartMode.RESET_STACK,
        )
    else:
        if user_data is None:
            Users.add_user(user_id, user_name, None, 0, reg_time)
        #await m.reply(f"Access denied! Wrong access key - {parameter}!\nPlease provide correct key below or use correct referral link.", parse_mode="HTML")
            await dialog_manager.start(
                States.gate_state,
                data=dialog_data,
                mode=StartMode.RESET_STACK,
            )
        else:
            await dialog_manager.start(
                States.gate_state,
                data=dialog_data,
                mode=StartMode.RESET_STACK,
            )

    # await m.reply(f"{parameter}", parse_mode="HTML")


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
        "access_key": user_data[3] if user_data else None,
        "user_balance": user_data[4] if user_data else 0,
    }
    if user_data is None:
        Users.add_user(user_id, user_name, None, 0, reg_time)
        await dialog_manager.start(
            States.access_state,
            data=dialog_data,
            mode=StartMode.RESET_STACK,
        )
    elif user_data[3]:
        await dialog_manager.start(
            States.main_menu_state,
            data=dialog_data,
            mode=StartMode.RESET_STACK,
        )
    else:
        await dialog_manager.start(
            States.access_state,
            data=dialog_data,
            mode=StartMode.RESET_STACK,
        )







# @user_router.message(CommandStart(deep_link=True))
# async def user_dl_start(m: Message, command: CommandObject, dialog_manager: DialogManager):
#     parameter = command.args
#     if parameter in Users.find_user_by_key(parameter):
#         reg_time = datetime.now()
#         user_id = m.from_user.id
#         user_name = m.from_user.username
#         user_data = Users.get_user(user_id)
#         logging.info(user_data)
#         dialog_data = {
#             "reg_time": reg_time,
#             "user_id": user_id,
#             "user_name": user_name,
#             "access_key": user_data[3] if user_data else None,
#             "user_balance": user_data[4] if user_data else 0,
#         }
#         if user_data is None:
#             Users.add_user(user_id, user_name, None, 0, reg_time)
#         await dialog_manager.start(
#             States.access_state,
#             data=dialog_data,
#             mode=StartMode.RESET_STACK,
#         )
#     else:





# @user_router.message(CommandStart())
# async def user_start(m: Message, dialog_manager: DialogManager):
#     reg_time = datetime.now()
#     user_id = m.from_user.id
#     user_name = m.from_user.username
#     user_data = Users.get_user(user_id)
#     logging.info(user_data)
#     dialog_data = {
#         "reg_time": reg_time,
#         "user_id": user_id,
#         "user_name": user_name,
#         "user_lang": user_data[2] if user_data else None
#     }
#     if user_data is None:
#         Users.add_user(user_id, user_name, None, reg_time)
#     else:
#         Users.add_user(user_id, user_name, user_data[2], reg_time)
#     await m.reply("Hello user!")
#     await dialog_manager.start(
#         States.main_menu_state,
#         data=dialog_data,
#         mode=StartMode.RESET_STACK,
#     )



# @user_router.message(Text('Back'))
# async def user_start(m: Message, dialog_manager: DialogManager):
#     await dialog_manager.start(
#         States.main_menu_state,
#         mode=StartMode.RESET_STACK,
#     )
