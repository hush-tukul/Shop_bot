# import re
#
#
# def filter_float(input_str):
#     # Check if the input_str is a valid float representation
#     pattern_comma = re.compile(r"^\d+(\,\d+)?$")
#     pattern_dot = re.compile(r"^\d+(\.\d+)?$")
#
#     if pattern_comma.match(input_str):
#         # Replace comma with dot and convert to float
#         float_str = input_str.replace(',', '.')
#         try:
#             result = float(float_str)
#             return result
#         except ValueError:
#             return None
#
#     elif pattern_dot.match(input_str):
#         try:
#             result = float(input_str)
#             return result
#         except ValueError:
#             return None
#     else:
#         return None
#
#
#
# print(filter_float("0,44"))
# from datetime import datetime
#
# g = [
#     {
#         'id': '1',
#         'item': 'Monitor iiyama G-Master G2450HS-B1 Black Hawk',
#         'user_id': '683497406',
#         'user_tg_name': 'd_w_y_t',
#         'item_details': 'Ekran: 21.5", 1920 x 1080px, VA\nCzęstotliwość odświeżania obrazu [Hz]: 75'
#                         '\nCzas reakcji matrycy [ms]: 1\nJasność ekranu [cd/m2]: 250\nProporcje ekranu: 16:9'
#                         '\nZłącza: Wyjście liniowe audio, HDMI x 1, DisplayPort x 1',
#         'item_price': '9,99', 'item_quantity': 1,
#         'item_photo': 'AgACAgQAAxkBAAISiGTYwBHous7cfe6hXFRu4voMUqRkAALjuzEbdvjBUgeDsPmMG1zmAQADAgADcwADMAQ',
#         'registry_datetime': datetime(2023, 8, 13, 11, 35, 53, 946858)},
#     {
#         'id': '2',
#         'item': 'Monitor ACER Predator XB253QGW 24.5" 1920x1080px IPS 280Hz 1 ms',
#         'user_id': '683497406', 'user_tg_name': 'd_w_y_t',
#         'item_details': 'Ekran: 24.5", 1920 x 1080px, IPS'
#                         '\nCzęstotliwość odświeżania obrazu [Hz]: 280''\nCzas reakcji matrycy [ms]: 1'
#                         '\nJasność ekranu [cd/m2]: 400\nProporcje ekranu: 16:9'
#                         '\nZłącza: Wyjście liniowe audio, USB x 2, HDMI x 2, DisplayPort x 1',
#         'item_price': '15,99',
#         'item_quantity': 1,
#         'item_photo': 'AgACAgQAAxkBAAISk2TYwGanPv1-OGBNeZihTeFRNIY6AALkuzEbdvjBUiLi4XoD1T7xAQADAgADcwADMAQ',
#         'registry_datetime': datetime(2023, 8, 13, 11, 37, 15, 143000)}]
#
# result = []
#
#
# for item in g:
#     result.append(
#         [item["id"], item["item"], item["item_details"]]
#     )
#
# print(result)
#
#
#
# for link, link_data in get_links_by_id(inline_query.from_user.id).items():
#         # В итоговый массив запихиваем каждую запись
#         results.append(InlineQueryResultArticle(
#             id=link,  # ссылки у нас уникальные, потому проблем не будет
#             title=link_data["title"],
#             description=link_data["description"],
#             input_message_content=InputTextMessageContent(
#                 message_text=get_message_text(
#                     link=link,
#                     title=link_data["title"],
#                     description=link_data["description"]
#                 ),
#                 parse_mode="HTML"
#             )
#         ))
import re


def filter_float(input_str):
    pattern_comma = re.compile(r"^\d+(\,\d+)?$")
    pattern_dot = re.compile(r"^\d+(\.\d+)?$")

    if pattern_comma.match(input_str):
        float_str = input_str.replace(',', '.')
        try:
            result = round(float(float_str), 2)
            return result
        except ValueError:
            return None

    elif pattern_dot.match(input_str):
        try:
            result = round(float(input_str), 2)
            return result
        except ValueError:
            return None
    else:
        return None


print(type(filter_float('34,6')))