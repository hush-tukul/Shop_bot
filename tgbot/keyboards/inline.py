import logging

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram_dialog import DialogManager
from aiogram_dialog.utils import get_chat

from tgbot.keyboards.states import States

""""""
"""REGISTER"""
# async def register_inline(dialog_manager: DialogManager, **kwargs):


async def phone_number_inline(dialog_manager: DialogManager, **kwargs):
    phone_permission = 'Confirm phone number'
    option_action_data = [
        ('PROMOTION', 'prom'),
        ('COMMISSION', 'com'),
        ('DOWNLOAD', 'down'),
        ('TRANSACTION', 'tran'),
        ('SETTINGS', 'set'),


    ]
    return {
            "phone_permission": phone_permission,
            "option_action_data": option_action_data,
        }




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