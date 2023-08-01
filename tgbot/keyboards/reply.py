import logging
from typing import Any

import requests
from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from db import Users
from tgbot.keyboards.states import States


# from db import Users, shorten_url, Reflink
# from run import bot

user_data_router = Router()


@user_data_router.message(F.text == "Back")
async def back_reply(m: Message, state: FSMContext, dialog_manager: DialogManager, bot: Bot):

    message_id = dialog_manager.dialog_data.get('message_id')
    await bot.delete_message(message_id)
    await dialog_manager.switch_to(States.main_menu_state)


async def main_window_reply(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, menu_option: str):
    # states_list = {
    #     'reg': States.register_state
    # }

    """Ask for phone version"""
    kb_phone = [[
        KeyboardButton(text="REGISTER Winbot33", request_contact=True)
    ], [
        KeyboardButton(text="Back")
    ]]
    markup_phone = ReplyKeyboardMarkup(keyboard=kb_phone, resize_keyboard=True,
                                       input_field_placeholder="Send phone number")

    await dialog_manager.switch_to(States.register_state)
    message = await c.message.answer(text="Please tap on [🎁 REGISTER Winbot33 🎁] & CLAIM FREE ANGPAO\n🧧 🧧 🧧 🧧 🧧 🧧 🧧 🧧\n⬇️ ⬇️ ⬇️ ⬇️ ⬇️ ⬇️ ⬇️ ⬇️",
                           reply_markup=markup_phone)
    dialog_manager.dialog_data.update(
                message_id=message.message_id
            )





    # await dialog_manager.switch_to(states_list[menu_option])
    # await c.answer(text='Test', show_alert=True)









"""Ask for phone version"""
# kb_phone = [[
    #     KeyboardButton(text="Сообщить номер телефона", request_contact=True)
    # ]]
    # markup_phone = ReplyKeyboardMarkup(keyboard=kb_phone, resize_keyboard=True,
    #                                    input_field_placeholder="Отправить телефон")
    #
    # await m.answer('PLease confirm Your phone number', reply_markup=markup_phone)





# async def close_menu(c: CallbackQuery, widget: Any, dialog_manager: DialogManager):
#     await dialog_manager.done()
#
#
# async def choose_lang_reply(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, user_lang: str):
#     logging.info('user_lang was added to DB')
#     dialog_manager.start_data.update(
#         user_lang=user_lang
#     )
#     user_id = dialog_manager.start_data.get('user_id')
#     Users.update_user_lang(user_id, user_lang)
#     await dialog_manager.switch_to(LinkBot.main_menu_state)
#
#
# async def main_menu_reply(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, main_menu_option: str):
#     dialog_manager.dialog_data.update(
#         main_menu_option=main_menu_option
#     )
#     logging.info(f'main_menu_reply: {main_menu_option}')
#     g = {
#         'links': LinkBot.links_list_state,
#         'global_stats': LinkBot.global_stats_state,
#         'all_instructions': LinkBot.chosen_service_info_state,
#         'change_lang': LinkBot.lang_was_changed_state,
#         'contact_feedback': LinkBot.reasons_feedback_state,
#
#     }
#
#     await dialog_manager.switch_to(g[main_menu_option])
#
#
#
#
#     # g = {
#     #     'change_link': LinkBot.change_link_state,
#     #     'link_stat': LinkBot.link_stats_state,
#     #     'show_ref_link': LinkBot.show_reflink_state,
#     #     'del_link': LinkBot.link_delete_state,
#     # }
#     #
#     # await dialog_manager.switch_to(g[main_menu_option])
#
#
#
# async def links_list_reply(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, chosen_link: str):
#     dialog_manager.dialog_data.update(
#         chosen_link=chosen_link
#     )
#     logging.info(f'links_list_reply: {chosen_link}')
#     await dialog_manager.switch_to(LinkBot.link_options_state if chosen_link not in ['add_link', None]
#                                    else LinkBot.add_link_state)
#     # logging.info(f'User choose: {list_choice}')
#     # await dialog_manager.switch_to(LinkBot.chosen_link_options_state if list_choice != 'insert_link'
#     #                                else LinkBot.link_was_created_state)
#
#
# async def link_options_reply(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, chosen_option: str):
#     chosen_link = dialog_manager.dialog_data.get('chosen_link')
#     dialog_manager.dialog_data.update(
#         chosen_option=chosen_option if chosen_link not in ['add_link', None] else 'add_link'
#     )
#     logging.info(f'link_options_reply: {chosen_option}')
#     await dialog_manager.switch_to(LinkBot.option_action_state if chosen_option != 'del_link'
#                                    else LinkBot.del_link_state)
#
#
# async def del_action_reply(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, action: str):
#     dialog_manager.dialog_data.update(
#         action=action
#     )
#     user_id = dialog_manager.start_data.get('user_id')
#     chosen_link = dialog_manager.dialog_data.get("chosen_link")
#     logging.info(f'del_action_reply: {action}')
#     logging.info(f'chosen_link: {chosen_link}')
#     Reflink.delete_link(user_id, chosen_link)
#     logging.info(f'Link {chosen_link} has been deleted!')
#     await c.answer(
#         text="Link has been deleted!",
#         show_alert=True
#     )
#     await dialog_manager.switch_to(LinkBot.links_list_state)
#
#
#
# async def new_link_reply(message: Message, input: MessageInput, dialog_manager: DialogManager):
#     chosen_link = dialog_manager.dialog_data.get('chosen_link')
#     logging.info('Trying to save a new link')
#     logging.info(f"chosen_link: {chosen_link}")
#     link = message.text
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         'Accept-Language': 'en-US,en;q=0.9',
#     }
#     response = requests.get(link, headers=headers)
#     response.raise_for_status()
#     link = message.text
#     user_id = message.from_user.id
#     link_id = await shorten_url(link)
#     if chosen_link == 'add_link':
#         logging.info(f'chosen_link: {chosen_link}')
#         try:
#
#             if response.status_code == 200:
#                 logging.info(f'The link {link} returned a status code of 200 (OK)')
#
#                 f = Reflink.save_link(user_id, link, link_id)
#                 logging.info(link_id)
#                 if f == 'exist':
#                     logging.info("link already exist, trying to make refer-link")
#                     await message.answer(f"Link already exist.", parse_mode='HTML')
#                     await dialog_manager.switch_to(LinkBot.links_list_state)
#
#                 else:
#                     logging.info("link was saved, trying to make refer-link")
#                     redirect_url = f"http://89.117.54.23:5000/{link_id}"
#                     logging.info("refer-link created")
#                     await message.answer(f"Link was saved and referral-link was created - {redirect_url}", parse_mode='HTML')
#                     await dialog_manager.switch_to(LinkBot.links_list_state)
#                 # Link is valid and returns status code 200
#             else:
#                 logging.warning(f'The link {link} returned a status code of {response.status_code}')
#                 await bot.send_message(chat_id=message.chat.id, text=f"Sorry:(\nVideo is unavailable on server.")
#                 await dialog_manager.switch_to(LinkBot.links_list_state)
#                 # Link is not valid or returns a status code other than 200
#         except requests.exceptions.RequestException as e:
#             logging.error(f'An error occurred while checking the link: {e}')
#
#     else:
#         if response.status_code == 200:
#             logging.info(f'The link {link} returned a status code of 200 (OK)')
#             logging.info("Trying to replace link")
#             g = Reflink.replace_link(user_id, chosen_link, link)
#             logging.info(f"Link was successfully replaced - {g}")
#             await message.answer(f"Link was successfully replaced - {g}", parse_mode='HTML')
#             await dialog_manager.switch_to(LinkBot.links_list_state)
#
#
#



