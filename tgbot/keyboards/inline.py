import logging

from aiogram.enums import ContentType
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.utils import get_chat
from environs import Env

from db import Users
from tgbot.keyboards.states import States


env = Env()








async def gate_inline(dialog_manager: DialogManager, **kwargs):
    user_name = dialog_manager.start_data.get('user_name')
    access_denied_info = f"Access denied for user {user_name}!\nPlease provide access code or use referral-link to access the bot: "
    access_button = [
            ('🔑 Access key', 'access'),
        ]
    return {
            "access_denied_info": access_denied_info,
            "access_button": access_button,
        }


async def access_inline(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.start_data.get('user_id')
    user_name = dialog_manager.start_data.get('user_name')
    user_data = Users.get_user(user_id)
    header = "Please provide access code below: "

    return {
        "header": header,
    }





async def main_window_inline(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.start_data.get('user_id')
    user_name = dialog_manager.start_data.get('user_name')
    user_data = Users.get_user(user_id)
    title = "Main Menu"
    main_menu = [('🛒 Market', 'access'), ('Feedback / Contact', 'contact'), ('Referral link / key', 'key'), ('Admin panel', 'admin_panel') if user_id in list(map(int, env.list("ADMINS"))) else None]

    return {
        "title": title,
        "main_menu_1": main_menu[:2],
        "main_menu_2": main_menu[2:] if main_menu[-1] else main_menu[2:3],

    }








# """"""
# """REGISTER"""
# async def register_inline(dialog_manager: DialogManager, **kwargs):
#     phone_permission = 'Confirm phone number'
#
#
# async def main_window_inline(dialog_manager: DialogManager, **kwargs):
#     header = 'Welcome to Winbot33!' \
#              '\nAgent-free, Exclusive & Direct HQ'\
#              '\nPlease select an option below :'
#     pic = 'AgACAgUAAxkBAAIBmmTH_Q9wDWVJw9E0_aIGEYDbiG26AAJ-tzEbMPpAViqBFy2ZJ2o5AQADAgADcwADLwQ'
#     image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(pic))
#     main_options = [
#         ('\U0001F4B0 REGISTER & CLAIM FREE \U0001F4B0', 'reg'),
#     ]
#     return {
#             'header': header,
#             'pic': image,
#             "main_options": main_options,
#         }


















# async def register_window_inline(dialog_manager: DialogManager, **kwargs):
#     header = 'Please tap on REGISTER Winbot33 & CLAIM FREE ANGPAO'
#
#     return {
#         'header': header
#     }


# async def main_menu_inline(dialog_manager: DialogManager, **kwargs):
#     user_lang = dialog_manager.start_data.get('user_lang')
#     logging.info(user_lang)
#     title_name = title(user_lang)[0][0]
#     t_buttons = title_buttons(user_lang)
#     return {
#         "title": title_name,
#         "title_buttons_1": t_buttons[:3],
#         "title_buttons_2": t_buttons[3:],
#     }
#
#
#
# # async def menu_option_inline(dialog_manager: DialogManager, **kwargs):
# #     user_lang = dialog_manager.start_data.get('user_lang')
# #     option = dialog_manager.dialog_data.get('main_menu_option')
# #     title_name = option_title(user_lang, option)[0][0]
# #     lang_option_buttons = option_buttons(user_lang, option)
# #     return {
# #         "title": title_name,
# #         'lang_option_buttons': lang_option_buttons
# #     }
#
# async def links_list_inline(dialog_manager: DialogManager, **kwargs):
#     dialog_manager.dialog_data.update(chosen_link='add_link')
#     user_lang = dialog_manager.start_data.get('user_lang')
#     option = dialog_manager.dialog_data.get('main_menu_option')
#     user_id = dialog_manager.start_data.get('user_id')
#     links_info = links_list(user_lang, option, user_id)
#     logging.info(user_lang, option, user_id)
#     return {
#         "links_title": links_info[0],
#         'links_info': links_info[1],
#     }
#
#
# async def add_link_inline(dialog_manager: DialogManager, **kwargs):
#     user_lang = dialog_manager.start_data.get('user_lang')
#     option = dialog_manager.dialog_data.get('main_menu_option')
#     action = 'change_link'
#     confirm_button = action_confirm_button(user_lang, option, action)
#     logging.info(confirm_button)
#     return {
#         'title': confirm_button[0][0],
#         'confirm_button': confirm_button[1][0][0]
#     }
#
#
#
#
#
# async def link_options_inline(dialog_manager: DialogManager, **kwargs):
#     user_lang = dialog_manager.start_data.get('user_lang')
#     option = dialog_manager.dialog_data.get('main_menu_option')
#     user_id = dialog_manager.start_data.get('user_id')
#     link_id = dialog_manager.dialog_data.get('chosen_link')
#     orig_link = Reflink.get_original_link_by_user_id(user_id, link_id)
#     link_option_buttons = option_buttons(user_lang, option)
#     return {
#         'title': orig_link,
#         'link_option_buttons': link_option_buttons
#     }
#
#
# async def option_action_inline(dialog_manager: DialogManager, **kwargs):
#     link_id = dialog_manager.dialog_data.get('chosen_link')
#     user_lang = dialog_manager.start_data.get('user_lang')
#     option = dialog_manager.dialog_data.get('main_menu_option')
#     action = dialog_manager.dialog_data.get('chosen_option')
#
#     logging.info(f"option_action_inline/option: {option}")
#     logging.info(f"option_action_inline/action: {action}")
#     confirm_button = action_confirm_button(user_lang, option, action)
#     option_action_data = ''
#     if action == 'show_ref_link':
#         redirect_url = f"http://89.117.54.23:5000/{link_id}"
#         option_action_data = redirect_url
#     return {
#         'title': confirm_button[0][0],
#         'confirm_button': confirm_button[1][0][0],
#         'option_action_data': option_action_data
#     }
#
#
# async def del_action_inline(dialog_manager: DialogManager, **kwargs):
#     user_lang = dialog_manager.start_data.get('user_lang')
#     option = dialog_manager.dialog_data.get('main_menu_option')
#     action = dialog_manager.dialog_data.get('chosen_option')
#     confirm_button = action_confirm_button(user_lang, option, action)
#     return {
#         'title': confirm_button[0][0],
#         'confirm_button': confirm_button[1]
#     }






# Second state - MAIN PARAMETERS:
#          "Your links"
#     -     "Ваші посилання"    -> provides to Third state - List of links
#          "Ваши ссылки"
#
#          "Global statistics"
#     -     "Загальна статистика"  -> provides to Third state - "Global statistics parameters for all user links"
#          "Общая статистика"
#
#          "Instruction"
#     -     "Інструкція"   -> provides to Third state - "Instruction and info about each service of this bot"
#          "Инструкция"
#
#
#          "Change lang"
#     -    "Змінити мову" -> provides to Third state - ""
#          "Поменять язык"
#
#
#          "Contact Us"
#     -    "Контакти"   -> provides to Third state - "Contact window to save request/questions/asks from users"
#          "Контакты"