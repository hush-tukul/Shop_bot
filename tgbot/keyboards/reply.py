
import logging
import re
from datetime import datetime
from typing import Any



from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput


from db import Users, Items
from tgbot.keyboards.states import States

logger = logging.getLogger(__name__)


# user_data_router = Router()

# async def close_menu(c: CallbackQuery, widget: Any, dialog_manager: DialogManager):
#     await dialog_manager.done()



async def filter_float(input_str):
    pattern_comma = re.compile(r"^\d+(\,\d+)?$")
    pattern_dot = re.compile(r"^\d+(\.\d+)?$")

    if pattern_comma.match(input_str):
        float_str = input_str.replace(',', '.')
        try:
            result = float(float_str)
            return result
        except ValueError:
            return None

    elif pattern_dot.match(input_str):
        try:
            result = float(input_str)
            return result
        except ValueError:
            return None
    else:
        return None

async def filter_int(input_str):
    try:
        check = int(input_str)
        return check
    except ValueError as e:
        logger.error(e)
        return None



async def gate_reply(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, access_button:str):
    logging.info('You are in gate_reply')
    await dialog_manager.switch_to(States.access_state)


async def access_reply(m: Message, input: MessageInput, dialog_manager: DialogManager):
    logger.info('You are in access_reply')
    user_id = dialog_manager.start_data.get('user_id')
    user_name = dialog_manager.start_data.get('user_name')
    key = m.text
    user_key = Users.get_user(user_id)[2]
    friend = Users.find_user_by_key(key)
    if key.isalnum() and len(key) == 8:
        if friend:
            Users.update_access_key(user_id, key)
            Users.referral_bonus(key)
            await m.reply(f"Access granted! Congratulations!!! - {user_name}!"
                          f"\nYou was recommended to Our Shop_bot by user - {friend[1]}"
                          f"\nPlease find below Your referral link that You can share with Your friends to get 10 extra points!"
                          f"\nhttps://t.me/Clstl_bot?start={user_key}", parse_mode="HTML")
            await dialog_manager.switch_to(States.main_menu_state)
        else:
            await m.reply(f"Unfortunately We can`t find Your key in Our base. "
                          f"Ask a friend for an up-to-date access key or referral link.", parse_mode="HTML")
    else:
        await m.reply(f"Your key contains letters or has an incorrect length!\nPlease provide correct access key.",
                      parse_mode="HTML")




async def main_menu_reply(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, menu_option: str):
    dialog_manager.dialog_data.update(menu_option=menu_option)
    logger.info('You are in main_menu_reply')
    g = {
        'admin_panel': States.admin_panel_state,

    }
    await dialog_manager.switch_to(g[menu_option])


async def admin_panel_reply(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, admin_option: str):
    dialog_manager.dialog_data.update(admin_option=admin_option)
    g = {
        'add': States.add_item_state,
        'delete': States.delete_item_state,
    }
    await dialog_manager.switch_to(g[admin_option])



async def add_item_reply(m: Message, input: MessageInput, dialog_manager: DialogManager):
    logger.info('You are in add_item_reply')
    user_id = dialog_manager.start_data.get('user_id')
    user_name = dialog_manager.start_data.get('user_name')
    item_name = m.text
    logger.info(item_name)
    if 15 < len(item_name) < 100:
        dialog_manager.dialog_data.update(item_name=item_name)
        await dialog_manager.switch_to(States.add_description_state)
    else:
        await m.reply(text="Please provide the name of the item using only letters and digits, "
                           "and make sure it's not empty and doesn't exceed 100 characters.\n Thanks!",
                      parse_mode="HTML")


async def add_description_reply(m: Message, input: MessageInput, dialog_manager: DialogManager):
    logger.info('You are in add_description_reply')
    user_id = dialog_manager.start_data.get('user_id')
    user_name = dialog_manager.start_data.get('user_name')
    item_description = m.text
    if 50 < len(item_description) < 300:
        dialog_manager.dialog_data.update(item_description=item_description)
        await dialog_manager.switch_to(States.add_price_state)
    else:
        await m.reply(text="Please provide a description of the item using only letters and digits, "
                           "ensuring it falls within the character limit of 50 to 300 characters.\nThanks!",
                      parse_mode="HTML")



async def add_price_reply(m: Message, input: MessageInput, dialog_manager: DialogManager):
    logger.info('You are in add_price_reply')
    user_id = dialog_manager.start_data.get('user_id')
    user_name = dialog_manager.start_data.get('user_name')
    item_price = m.text
    correct_price_format = await filter_float(item_price)
    if item_price and correct_price_format:
        dialog_manager.dialog_data.update(item_price=item_price)
        await dialog_manager.switch_to(States.add_quantity_state)
    else:
        await m.reply(text="No no no, please type the price of the item, using format '0.0'. Thanks!",
                      parse_mode="HTML")



async def add_quantity_reply(m: Message, input: MessageInput, dialog_manager: DialogManager):
    logger.info('You are in add_price_reply')
    user_id = dialog_manager.start_data.get('user_id')
    user_name = dialog_manager.start_data.get('user_name')
    item_quantity = m.text
    correct_quantity_format = await filter_int(item_quantity)
    if item_quantity and correct_quantity_format:
        dialog_manager.dialog_data.update(item_quantity=correct_quantity_format)
        await dialog_manager.switch_to(States.add_photo_state)
    else:
        await m.reply(text="No no no, please type the quantity of the item, using format '123'. Thanks!",
                      parse_mode="HTML")



async def add_photo_reply(m: Message, input: MessageInput, dialog_manager: DialogManager):
    logger.info('You are in add_photo_reply')
    user_id = dialog_manager.start_data.get('user_id')
    user_name = dialog_manager.start_data.get('user_name')
    item_photo = m.photo[0].file_id
    logger.info(item_photo)
    if item_photo:
        dialog_manager.dialog_data.update(item_photo=item_photo)
        await dialog_manager.switch_to(States.add_item_confirmation_state)
    else:
        await m.reply(text="Please upload correct photo, using one of the formats -> JPEG or PNG."
                           "\nPlease refrain from uploading files larger than 20 mb, "
                           "as it may affect the performance and usability of the bot. Thanks!",
                      parse_mode="HTML")



async def add_item_confirmation_reply(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, button: str):
    logger.info("You are in add_item_confirmation_reply")
    item_name = dialog_manager.dialog_data.get('item_name')
    user_id = dialog_manager.start_data.get('user_id')
    user_name = dialog_manager.start_data.get('user_name')
    item_description = dialog_manager.dialog_data.get('item_description')
    item_price = dialog_manager.dialog_data.get('item_price')
    item_photo = dialog_manager.dialog_data.get('item_photo')
    item_quantity = dialog_manager.dialog_data.get('item_quantity')
    registry_datetime = datetime.now()
    dialog_manager.dialog_data.update(button=button)
    Items.add_item(item_name, user_id, user_name, item_description, item_price, item_quantity, item_photo, registry_datetime)
    g = {
        'confirm': States.item_added_state,
        'cancel': States.admin_panel_state,
    }
    await dialog_manager.switch_to(g[button])

async def item_added_reply(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, button: str):
    logger.info("You are in item_added_reply")


    g = {
        'admin_panel': States.admin_panel_state,
    }
    await dialog_manager.switch_to(g[button])




async def delete_item_reply(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, button: str):
    logger.info('You are in delete_item_reply')
    user_id = dialog_manager.start_data.get('user_id')
    user_name = dialog_manager.start_data.get('user_name')
    #Items.delete_item()
    #await dialog_manager.switch_to(States.confirmed_item_delete_state)



async def confirmed_item_delete_reply(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, button: str):
    logger.info('You are in delete_item_reply')
    user_id = dialog_manager.start_data.get('user_id')
    user_name = dialog_manager.start_data.get('user_name')
    await dialog_manager.switch_to(States.confirmed_item_delete_state)




# @user_data_router.message(F.text == "Back")
# async def back_reply(m: Message, state: FSMContext, dialog_manager: DialogManager, bot: Bot):
#
#     message_id = dialog_manager.dialog_data.get('message_id')
#     await bot.delete_message(message_id)
#     await dialog_manager.switch_to(States.main_menu_state)

















# async def main_window_reply(c: CallbackQuery, widget: Any, dialog_manager: DialogManager, menu_option: str):
#     # states_list = {
#     #     'reg': States.register_state
#     # }
#
#     """Ask for phone version"""
#     kb_phone = [[
#         KeyboardButton(text="REGISTER Winbot33", request_contact=True)
#     ], [
#         KeyboardButton(text="Back")
#     ]]
#     markup_phone = ReplyKeyboardMarkup(keyboard=kb_phone, resize_keyboard=True,
#                                        input_field_placeholder="Send phone number")
#
#     await dialog_manager.switch_to(States.register_state)
#     message = await c.message.answer(text="Please tap on [🎁 REGISTER Winbot33 🎁] & CLAIM FREE ANGPAO\n🧧 🧧 🧧 🧧 🧧 🧧 🧧 🧧\n⬇️ ⬇️ ⬇️ ⬇️ ⬇️ ⬇️ ⬇️ ⬇️",
#                            reply_markup=markup_phone)
#     dialog_manager.dialog_data.update(
#                 message_id=message.message_id
#             )





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



