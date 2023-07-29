import operator

from aiogram.enums import ParseMode, ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, Select, SwitchTo, Column
from aiogram_dialog.widgets.text import Const, Format

# from tgbot.keyboards.inline import main_menu_inline, choose_lang, links_list_inline, link_options_inline, \
#     option_action_inline, del_action_inline, add_link_inline
# from tgbot.keyboards.reply import choose_lang_reply, main_menu_reply, links_list_reply, new_link_reply, \
#     link_options_reply, del_action_reply
# from tgbot.keyboards.states import LinkBot





# choose_lang_window = Window(
#     Const('Обрати мову/Chose language/Выберите язык'),
#     Row(
#         Select(
#             Format("{item[0]}"),
#             id="second_window_c",
#             item_id_getter=operator.itemgetter(1),
#             items='lang',
#             on_click=choose_lang_reply
#         ),
#     ),
#     parse_mode=ParseMode.HTML,
#     state=LinkBot.choose_lang_state,
#     getter=choose_lang
# )
#
#
#
#
# main_menu_window = Window(
#     Format("{title}"),
#     Column(
#         Select(
#             Format("{item[0]}"),
#             id="main_menu_1",
#             item_id_getter=operator.itemgetter(1),
#             items='title_buttons_1',
#             on_click=main_menu_reply
#         ),
#         Select(
#             Format("{item[0]}"),
#             id="main_menu_2",
#             item_id_getter=operator.itemgetter(1),
#             items="title_buttons_2",
#             on_click=main_menu_reply,
#
#         ),
#     ),
#     parse_mode=ParseMode.HTML,
#     state=LinkBot.main_menu_state,
#     getter=main_menu_inline
# )
#
#
# links_list_window = Window(
#     Format("{links_title}"),
#     Column(
#         Select(
#             Format("{item[0]}"),
#             id="option_list",
#             item_id_getter=operator.itemgetter(1),
#             items='links_info',
#             on_click=links_list_reply
#         ),
#     ),
#     MessageInput(new_link_reply, ContentType.TEXT),
#     SwitchTo(Const("Back"), id="Back", state=LinkBot.main_menu_state),
#     parse_mode=ParseMode.HTML,
#     state=LinkBot.links_list_state,
#     getter=links_list_inline
# )
#
#
# add_link_window = Window(
#     Format("{title}"),
#     Format("{confirm_button}"),
#     MessageInput(new_link_reply, ContentType.TEXT),
#     SwitchTo(Const("Back"), id="Back", state=LinkBot.links_list_state),
#     parse_mode=ParseMode.HTML,
#     state=LinkBot.add_link_state,
#     getter=add_link_inline
# )
#
#
#
# link_options_window = Window(
#     Format("{title}"),
#     Column(
#         Select(
#             Format("{item[0]}"),
#             id="link_options",
#             item_id_getter=operator.itemgetter(1),
#             items='link_option_buttons',
#             on_click=link_options_reply
#         ),
#     ),
#     SwitchTo(Const("Back"), id="Back", state=LinkBot.links_list_state),
#     parse_mode=ParseMode.HTML,
#     state=LinkBot.link_options_state,
#     getter=link_options_inline
# )
#
# option_action_window = Window(
#     Format("{title}"),
#     Format("{confirm_button}"),
#     Format("{option_action_data}"),
#     MessageInput(new_link_reply, ContentType.TEXT),
#     SwitchTo(Const("Back"), id="Back", state=LinkBot.link_options_state),
#     parse_mode=ParseMode.HTML,
#     state=LinkBot.option_action_state,
#     getter=option_action_inline
# )
#
#
# del_link_window = Window(
#     Format("{title}"),
#     Column(
#         Select(
#             Format("{item[0]}"),
#             id="del_action",
#             item_id_getter=operator.itemgetter(1),
#             items='confirm_button',
#             on_click=del_action_reply
#         ),
#     ),
#     SwitchTo(Const("Back"), id="Back", state=LinkBot.link_options_state),
#     parse_mode=ParseMode.HTML,
#     state=LinkBot.del_link_state,
#     getter=del_action_inline
# )