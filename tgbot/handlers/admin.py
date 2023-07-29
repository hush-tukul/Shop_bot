import logging
from datetime import datetime

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from db import Users
from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.states import States

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(m: Message, dialog_manager: DialogManager):
    try:
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
            Users.add_user(user_id, user_name, None, None, reg_time)
        await m.reply(f"Hello admin!")
        await dialog_manager.start(
            States.phone_number_state,
            data=dialog_data,
            mode=StartMode.RESET_STACK,
        )
    except Exception as e:
        logging.info(e)












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
