import logging
from datetime import datetime

from aiogram import Router
from aiogram.filters import CommandStart, Text, CommandObject
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery, InlineQuery
from aiogram_dialog import DialogManager, StartMode

from db import Users
from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.states import States

admin_router = Router()
admin_router.message.filter(AdminFilter())


# @admin_router.inline_query()
# async def admin_start(query: InlineQuery):




# @admin_router.message(CommandStart(deep_link=True))
# async def admin_dl_start(m: Message, command: CommandObject, dialog_manager: DialogManager):
#     parameter = command.text
#     reg_time = datetime.now()
#     user_id = m.from_user.id
#     user_name = m.from_user.username
#     user_data = Users.get_user(user_id)
#     logging.info(user_data)
#     dialog_data = {
#         "reg_time": reg_time,
#         "user_id": user_id,
#         "user_name": user_name,
#         "access_key": user_data[3] if user_data else None,
#         "user_balance": user_data[4] if user_data else 0,
#     }
#     if parameter in Users.find_user_by_key(parameter):
#         if user_data is None:
#             Users.add_user(user_id, user_name, None, 0, reg_time)
#         await dialog_manager.start(
#             States.main_menu_state,
#             data=dialog_data,
#             mode=StartMode.RESET_STACK,
#         )
#     else:
        # await m.reply(f"Access denied! Wrong access key - {parameter}!\nPlease provide correct key below or use correct referral link.", parse_mode="HTML")
        # await dialog_manager.start(
        #     States.gate_state,
        #     data=dialog_data,
        #     mode=StartMode.RESET_STACK,
        # )

# @admin_router.message(CommandStart(deep_link=True))
# async def admin_start(m: Message, command: CommandObject):
#     parameter = command.args
#     await m.reply(f"{parameter}", parse_mode="HTML")

@admin_router.message(CommandStart())
async def admin_start(m: Message, dialog_manager: DialogManager):
    reg_time = datetime.now()
    user_id = m.from_user.id
    user_name = m.from_user.username
    access_key = '123456'
    user_data = Users.get_user(user_id)
    logging.info(user_data)
    dialog_data = {
        "reg_time": reg_time,
        "user_id": user_id,
        "user_name": user_name,
        "access_key": user_data[3] if user_data else access_key,
        "user_balance": user_data[4] if user_data else 0,
    }
    if user_data is None:
        Users.add_user(user_id, user_name, access_key, 0, reg_time)
    await m.reply(f"Hello admin!\U0001F600", parse_mode='HTML')
    await dialog_manager.start(
        States.main_menu_state,
        data=dialog_data,
        mode=StartMode.RESET_STACK,
    )



















# @admin_router.message(CommandStart())
# async def admin_start(m: Message, dialog_manager: DialogManager):
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
#         Users.add_user(user_id, user_name, None, None, reg_time)
#     await m.reply(f"Hello admin!\U0001F600", parse_mode='HTML')
#     await dialog_manager.start(
#         States.main_menu_state,
#         data=dialog_data,
#         mode=StartMode.RESET_STACK,
#     )
#
#
# @admin_router.message(Text('Back'))
# async def user_start(m: Message, dialog_manager: DialogManager):
#     await dialog_manager.start(
#         States.main_menu_state,
#         mode=StartMode.RESET_STACK,
#     )




# @user_router.message(F.photo)
# async def user_start(m: Message):
#     photo_id = m.photo[0]
#     await m.reply(f"{photo_id}", parse_mode='HTML')








# @admin_router.message(F.text)
# async def admin_start(message: Message):
#     g = ['http://', 'https://']
#     if any([True if i in message.text else False for i in g]):
#         link = message.text
#         user_id = message.from_user.id
#         link_id = await shorten_url(link)
#         f = Reflink.save_link(user_id, link, link_id)
#         logging.info(link_id)
#         if f == 'exist':
#             logging.info("link already exist, trying to make refer-link")
#             redirect_url = UTMTracker(link_id).add_link_id()
#             logging.info("refer-link created")
#             await message.answer(f"Link already exist. Referral-link was created - {redirect_url}", parse_mode='HTML')
#
#         else:
#             logging.info("link was saved, trying to make refer-link")
#             redirect_url = UTMTracker(link_id).add_link_id()
#             logging.info("refer-link created")
#             await message.answer(f"Link was saved and referral-link was created - {redirect_url}", parse_mode='HTML')
#
#     else:
#         await message.answer('Wrong link', parse_mode='HTML')

# @admin_router.message(F.text)
# async def instalink(message: Message):
#     g = ['www.instagram.com/p', 'www.instagram.com/reel']
#     if any([True if i in message.text else False for i in g]):
#         logging.info("trying to download video")
#
#         cl = await dp.storage.get_data(bot=bot, key='cl')
#         start = time.time()
#         link = message.text
#         logging.info(cl)
#         r = await download_instagram_video(link, message.from_user.id, cl['cl'])
#         end = time.time()
#         input_file_d = BufferedInputFile(r, filename="cut_video.mp4")
#         await message.answer_video(input_file_d,
#                                    caption=f"File converted successfully!\nTime: {round(end - start, 3)} seconds")
