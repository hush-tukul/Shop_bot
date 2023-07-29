import logging
import time
from datetime import datetime

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode


from tgbot.keyboards.states import LinkBot

user_router = Router()



@user_router.message(CommandStart())
async def user_start(m: Message):
    # reg_time = datetime.now()
    # user_id = m.from_user.id
    # user_name = m.from_user.username
    # user_data = Users.get_user(user_id)
    # logging.info(user_data)
    # dialog_data = {
    #     "reg_time": reg_time,
    #     "user_id": user_id,
    #     "user_name": user_name,
    #     "user_lang": user_data[2] if user_data else None
    # }
    # if user_data is None:
    #     Users.add_user(user_id, user_name, None, reg_time)
    # else:
    #     Users.add_user(user_id, user_name, user_data[2], reg_time)
    await m.reply("Hello user!")
    # await dialog_manager.start(
    #     LinkBot.choose_lang_state if user_data is None else LinkBot.main_menu_state,
    #     data=dialog_data,
    #     mode=StartMode.RESET_STACK
    # )


# @user_router.message(F.text)
# async def instalink(message: Message):
#     g = ['www.instagram.com/p', 'www.instagram.com/reel']
#     if any([True if i in message.text else False for i in g]):
#         logging.info("trying to download video")
#
#         start = time.time()
#         link = message.text
#
#         r = await download_instagram_video(link, message.from_user.id)
#         end = time.time()
#         input_file_d = BufferedInputFile(r, filename="cut_video.mp4")
#         await message.answer_video(input_file_d,
#                                    caption=f"File converted successfully!\nTime: {round(end - start, 3)} seconds")
