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



print(len("Monitor iiyama G-Master G2450HS-B1 Black Hawk"))