import html
import logging
import os
import re
import time
from datetime import datetime
from typing import Optional

from aiogram import Router, F, Bot
from aiogram.enums import ContentType, ChatType
from aiogram.filters import CommandStart, CommandObject, ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER, \
    callback_data, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, chat_member, ChatMemberUpdated, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent, InputInvoiceMessageContent, LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup, \
    CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.manager.bg_manager import BgManager

from db import Users, Items
from tgbot.keyboards.callback_filter import MyCallback
from tgbot.keyboards.states import States

logger = logging.getLogger(__name__)

user_router = Router()






async def query_builder(letters):
    logger.info(f"query_builder: ")
    items = Items.get_items_by_letters(letters)
    if items:
        logger.info(f"query_builder: if items: ")
        results = []

        for item in items:
            if item['item_quantity'] > 0:
                cb1 = MyCallback(foo="buy_item", bar=item["id"]).pack()
                keyboard = [
                    [
                        InlineKeyboardButton(text="Buy item", callback_data=cb1),
                    ]
                ]
                results.append(InlineQueryResultArticle(
                    id=str(item["id"]),
                    title=item["item"],

                    input_message_content=InputTextMessageContent(
                        message_text=f"\nItem: {item['item']}"
                                     f"\nDescription: {item['item_details']}"
                                     f"\nPrice: {item['item_price']} USD"
                                     f"\n{item['item_url']}",
                    ),
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    thumbnail_url=item["item_url"],
                    description=item["item_details"],
                    parse_mode="HTML",
                )
                )
            else:
                results.append(InlineQueryResultArticle(
                    id=str(item["id"]),
                    title=f"🚫OUT OF STOCK🚫 - {item['item']}",
                    input_message_content=InputTextMessageContent(
                        message_text=f"❗️❗️❗️🚫 OUT OF STOCK 🚫❗️❗️❗"
                                     f"\nItem: {item['item']}"
                                     f"\nDescription: {item['item_details']}"
                                     f"\nPrice: {item['item_price']} USD"
                                     f"\n{item['item_url']}",

                    ),
                    thumbnail_url=item["item_url"],
                    description=item["item_details"],
                    parse_mode="HTML",
                )
                )

        logger.info(f"results = {results}")
        return results

    elif letters is None:
        logger.info(f"query_builder: elif letters is None: ")
        results = []

        for item in Items.get_items():
            if item['item_quantity'] > 0:
                cb1 = MyCallback(foo="buy_item", bar=item["id"]).pack()
                keyboard = [
                    [
                        InlineKeyboardButton(text="Buy item", callback_data=cb1),
                    ]
                ]
                results.append(InlineQueryResultArticle(
                    id=str(item["id"]),
                    title=item["item"],
                    input_message_content=InputTextMessageContent(
                        message_text=f"\nItem: {item['item']}"
                                     f"\nDescription: {item['item_details']}"
                                     f"\nPrice: {item['item_price']} USD"
                                     f"\n{item['item_url']}",

                    ),
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    thumbnail_url=item["item_url"],
                    description=item["item_details"],
                    parse_mode="HTML",
                )
                )
            else:
                results.append(InlineQueryResultArticle(
                    id=str(item["id"]),
                    title=f"🚫OUT OF STOCK🚫 - {item['item']}",
                    input_message_content=InputTextMessageContent(
                        message_text=f"❗️❗️❗️🚫 OUT OF STOCK 🚫❗️❗️❗"
                                     f"\nItem: {item['item']}"
                                     f"\nDescription: {item['item_details']}"
                                     f"\nPrice: {item['item_price']} USD"
                                     f"\n{item['item_url']}",

                    ),
                    thumbnail_url=item["item_url"],
                    description=item["item_details"],
                    parse_mode="HTML",
                )
                )
        logger.info(f"results = {results}")
        return results
    else:
        logger.info(f"query_builder: else: ")
        return None


@user_router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER), F.chat.type == ChatType.CHANNEL)
async def on_user_leave(event: ChatMemberUpdated):
    user_id = event.from_user.id
    logger.info(event.chat.id)


@user_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER), F.chat.type == ChatType.CHANNEL)
async def on_user_join(event: ChatMemberUpdated, bot: Bot):
    user_id = event.from_user.id
    user_info = Users.get_user(user_id)
    reg_time = datetime.now()
    user_name = event.from_user.username
    chat_id = event.chat.id
    if user_info:
        chat_id = user_info[5]
        Users.update_access_key(user_id, 'be31fd64')
        logger.info(user_id)
        logger.info(event.chat.id)
        await bot.send_message(chat_id=chat_id, text=f"Access granted.\nPlease enter /start command to use Our Shop_bot.")
    else:
        Users.add_user(user_id, user_name, None, 0, chat_id, reg_time)
        chat_id = user_info[5]
        Users.update_access_key(user_id, 'be31fd64')
        logger.info(user_id)
        logger.info(event.chat.id)
        await bot.send_message(chat_id=chat_id,
                               text=f"Access granted.\nPlease enter /start command to use Our Shop_bot.")

# @user_router.inline_query(lambda query: query.startswith('start='))
# async def inline_start_handler(query: InlineQuery):

@user_router.message(CommandStart(deep_link=True))
async def user_dl_start(m: Message, command: CommandObject, dialog_manager: DialogManager):
    logger.info(f"You are in user_dl_start")
    parameter = command.args
    logger.info(parameter)
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
        logger.info(f"if friend: ")
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
            # await m.reply(f"Access denied! Wrong access key - {parameter}!\nPlease provide correct key below or use correct referral link.", parse_mode="HTML")
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
    logger.info(f"You are in user_start")
    reg_time = datetime.now()
    user_id = m.from_user.id
    user_name = m.from_user.username
    chat_id = m.chat.id
    user_data = Users.get_user(user_id)
    logger.info(user_data)
    dialog_data = {
        "reg_time": reg_time,
        "user_id": user_id,
        "user_name": user_name,
        "access_key": user_data[3] if user_data else None,
        "user_balance": user_data[4] if user_data else 0,
    }
    if user_data is None:
        logger.info(f"if user_data is None: ")
        Users.add_user(user_id, user_name, None, 0, chat_id, reg_time)
        await dialog_manager.start(
            States.access_state,
            data=dialog_data,
            mode=StartMode.RESET_STACK,
        )
    elif user_data[3]:
        logger.info(f"elif user_data[3]: ")
        await dialog_manager.start(
            States.main_menu_state,
            data=dialog_data,
            mode=StartMode.RESET_STACK,
        )

    else:
        logger.info(f"else: ")
        await dialog_manager.start(
            States.access_state,
            data=dialog_data,
            mode=StartMode.RESET_STACK,
        )


@user_router.inline_query()
async def user_query(query: InlineQuery, state: FSMContext):
    logger.info(f"You are in user_query")
    user_id = query.from_user.id
    letters = query.query
    logger.info(f"letters: {letters}")
    await state.clear()
    if Users.get_user(user_id)[3] is None:
        await query.answer(
            results=[],
            switch_pm_text="Bot is unavailable. Please register first",
            switch_pm_parameter="connect_user",
            cache_time=5,

        )
        return

    if letters == "":
        logger.info(f"letters is '': ")
        results = await query_builder(None)
        try:
            await query.answer(
                results=results,
                cache_time=5,
                is_personal=True,
            )
        except Exception as e:
            logger.error(e)

    else:
        logger.info(f"letters is not '': ")
        not_found = [
            InlineQueryResultArticle(
                id="not_found",
                title="Not Found...",
                input_message_content=InputTextMessageContent(
                    message_text="Not Found...",

                ),
                thumbnail_url="https://miro.medium.com/v2/resize:fit:800/1*hFwwQAW45673VGKrMPE2qQ.png",
                description="Please try again...",
                parse_mode="HTML",
            )
        ]
        results = await query_builder(letters)
        logger.info(f"letters is not '' results: {results}")

        try:
            await query.answer(
                results=results if results else not_found,
                cache_time=5,
                is_personal=True,
            )
        except Exception as e:
            logger.error(e)


@user_router.callback_query(MyCallback.filter(F.foo == "buy_item"))
async def user_callback_handler(query: CallbackQuery, state: FSMContext, callback_data: MyCallback):
    logger.info(f"You are in user_callback_handler")
    item_id = callback_data.bar
    logger.info(f"item_id: {item_id}")
    item = Items.get_item_by_id(item_id)
    chat_id = query.from_user.id
    logger.info(f"chat_id: {chat_id}")
    await state.update_data(item_id=item_id)
    await query.bot.send_message(chat_id=chat_id, text='Please enter quantity: ', parse_mode="HTML")
    await state.set_state(States.market_state)


@user_router.message(StateFilter(States.market_state))
async def market_prepare(message: Message, state: FSMContext, dialog_manager: DialogManager):
    logger.info(f"You are in market_prepare")
    text = message.text
    chat_id = message.chat.id
    item_id = await state.get_data()
    if item_id['item_id']:
        logger.info(f"item_id: {item_id['item_id']}")
        quantity = int(message.text)
        logger.info(f"quantity: {quantity}")

        item = Items.get_item_by_id(item_id['item_id'])
        if 0 < quantity <= item['item_quantity']:
            logger.info(f"if item_id['item_id']:  if 0 < quantity <= item['item_quantity']: ")
            prices = [LabeledPrice(label="Test", amount=float(item['item_price']) * 100)]
            await message.answer_invoice(
                title=item['item'],
                description=item['item_details'],
                payload="Custom-Payload",
                provider_token=os.getenv('PAYMENT_TOKEN'),
                currency='USD',
                prices=prices,
                photo_url=item['item_url'],
                need_shipping_address=True,
            )
            await state.clear()
        elif quantity > item['item_quantity'] > 0:
            logger.info(f"Can`t sell this item - quantity > item['item_quantity']")
            await message.answer(text='Unfortunately it`s not enough quantity.\nPlease provide less quantity.',
                                 parse_mode="HTML")
            return
        elif item['item_quantity'] == 0:
            logger.info(f"Can`t sell this item - item_quantity == 0")
            await message.answer(text='Unfortunately this item is not available.',
                                 parse_mode="HTML")
            return
    else:
        logger.info(f"market: else: ")


