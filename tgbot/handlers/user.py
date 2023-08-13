import html
import logging
import time
from datetime import datetime
from typing import Optional

from aiogram import Router, F, Bot
from aiogram.enums import ContentType, ChatType
from aiogram.filters import CommandStart, CommandObject, ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.types import Message, chat_member, ChatMemberUpdated, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent
from aiogram_dialog import DialogManager, StartMode

from db import Users, Items
from tgbot.keyboards.states import States

user_router = Router()

@user_router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER), F.chat.type == ChatType.CHANNEL)
async def on_user_leave(event: ChatMemberUpdated):
    user_id = event.from_user.id
    logging.info(user_id)



@user_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER), F.chat.type == ChatType.CHANNEL)
async def on_user_join(event: ChatMemberUpdated, bot: Bot):
    user_id = event.from_user.id
    chat_id = Users.get_user(user_id)[5]
    Users.update_access_key(user_id, 'be31fd64')
    logging.info(user_id)
    await bot.send_message(chat_id=chat_id, text=f"Access granted.\nPlease enter /start command to use Our Shop_bot.")



# @user_router.inline_query(lambda query: query.startswith('start='))
# async def inline_start_handler(query: InlineQuery):

@user_router.message(CommandStart(deep_link=True))
async def user_dl_start(m: Message, command: CommandObject, dialog_manager: DialogManager):
    parameter = command.args
    logging.info(parameter)
    reg_time = datetime.now()
    user_id = m.from_user.id
    user_name = m.from_user.username
    chat_id = m.chat.id
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
            Users.add_user(user_id, user_name, None, 0, chat_id, reg_time)
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
            Users.add_user(user_id, user_name, None, 0, chat_id, reg_time)
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
    chat_id = m.chat.id
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
        Users.add_user(user_id, user_name, None, 0, chat_id, reg_time)
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










@user_router.inline_query(F.query == "")
async def show_user_links(query: InlineQuery):
    await query.answer(
        results=[
            InlineQueryResultArticle(
                id="list",
                title="Type something...",
                input_message_content=InputTextMessageContent(
                    message_text="You don`t need to press it",

                )

            )
        ],
        cache_time=5
    )

@user_router.inline_query()
async def some_query(query: InlineQuery):
    user_id = query.from_user.id
    if Users.get_user(user_id) is None:
        await query.answer(
            results=[],
            switch_pm_text="Bot is unavailable. Please register first",
            switch_pm_parameter="connect_user",
            cache_time=5,

        )
        return


# @user_router.inline_query()
# async def show_user_links(inline_query: InlineQuery):
#
#     # Эта функция просто собирает текст, который будет
#     # отправлен при нажатии на вариант в инлайн-режиме
#     def get_message_text(
#             item: str,
#             title: str,
#             description: Optional[str]
#     ) -> str:
#         text_parts = [f'{html.bold(html.quote(title))}']
#         if description:
#             text_parts.append(html.quote(description))
#         text_parts.append("")  # добавим пустую строку
#         text_parts.append(id)
#         return "\n".join(text_parts)
#
#
#     item_list = Items.get_items()
#     results = []
#
#     for item in item_list:
#         results.append(InlineQueryResultArticle(
#             id=item["id"],
#             title=item["item"],
#             description=item["item_details"],
#             input_message_content=InputTextMessageContent(
#                 message_text=get_message_text(
#                     item=item["item"],
#                     title=item["item"],
#                     description=item["item_details"]
#                 ),
#                 parse_mode="HTML"
#             )
#         ))
#
#     await inline_query.answer(results, is_personal=True, cache_time=5)








# ChatMemberMember
#ContentType


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
