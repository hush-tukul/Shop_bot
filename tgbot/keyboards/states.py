from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    """FOR NEW USERS / ZERO WINDOW"""
    gate_state = State()
    access_state = State()


    """FIRST WINDOW FOR REGULAR USERS"""
    main_menu_state = State()

    """SECOND WINDOW"""
    admin_panel_state = State()

    """THIRD WINDOW"""

    add_item_state = State()
    delete_item_state = State()
    us_state = State()

    """FORTH WINDOW"""
    add_description_state = State()

    """FIFTH WINDOW"""
    add_price_state = State()

    """SIXTH WINDOW"""
    add_quantity_state = State()

    """SEVENTH WINDOW"""
    add_photo_state = State()

    """EIGHTH WINDOW"""
    add_item_confirmation_state = State()
    item_added_state = State()









    """"""
    # """FOR NEW USERS / ZERO WINDOW"""
    # choose_lang_state = State()
    #
    # """FIRST WINDOW FOR REGULAR USERS"""
    # main_menu_state = State()
    #
    # """SECOND WINDOW"""
    # menu_option_state = State()
    #
    # """THIRD WINDOW"""
    # links_list_state = State()
    # global_stats_state = State()
    # chosen_service_info_state = State()
    # lang_was_changed_state = State()
    # reasons_feedback_state = State()
    #
    # """FORTH WINDOW"""
    # link_options_state = State()
    # add_link_state = State()
    #
    # """FIFTH WINDOW"""
    # link_was_created_state = State()
    # chosen_link_options_state = State()
    # feedback_write_state = State()
    #
    #
    # """SIXTH WINDOW"""
    # option_action_state = State()
    # statslink_reflink_state = State()
    #
    # """SEVENTH WINDOW"""
    # del_link_state = State()







# First state
#Choose lang buttons -> provides to Second state - "Please save Your first link"

"""IF LINK/LINKS ALREADY EXISTS"""

#Second state - MAIN PARAMETERS:
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
#     -    "Змінити мову"  -> provides to #Third_state - "Change user language"
#          "Поменять язык"
#
#
#          "Contact Us"
#     -    "Контакти"   -> provides to Third state - "Contact window to save request/questions/asks from users"
#          "Контакты"


"""IF NOT EXISTS"""
"""DON`T ADD THIS TO JSON!!!!! -> Please save Your first link"""
##Second state - "Please save Your first link" -> provides to Forth state - Choosen link parameters





"""ALL THIRD STATES"""

#Third state - List of links -> provides to Forth state - Choosen link

#Third state - "Global statistics parameters for all user links" -> end window of branch

#Third state - "Instruction and info about each service of this bot" -> provides to Forth state - Info and instruction about chosen service of this bot

#Third_state - "Change user language"  -> provides to Forth state - User language successfully changed!

#Third state - "Contact window to save request/questions/asks from users" -> provides to Forth state - List of reason to leave feedback to choose

"""ALL FORTH STATES"""

#Forth state - Choosen link:
# - Change link -> provides to Fifth state - Please send new link to change
# - Show referral link that provide to orig-link -> provides to Fifth state - Referral generated link
# - Show link stat -> provides to Fifth state - Link stats
# - Delete link -> provides to Fifth state - Link was succesfully deleted

#Forth state - Info and instruction about chosen service of this bot -> end window of branch

#Forth state - User language successfully changed! -> end window of branch

#Forth state - List of reason to leave feedback to choose -> provides to Fifth state - Please write and send Your feedback


"""ALL FIFTH STATES"""
#Fifth state - Please send new link to change -> provides to Sixth state - Link "yourlink" succesfully changed
#Fifth state - Referral generated link -> end window of branch
#Fifth state - Link stats -> end window of branch
#Fifth state - Link was succesfully deleted -> end window of branch
#Fifth state - Please write and send Your feedback (it tagged by chosen reason of feedback) -> end window of branch



"""ALL SIXTH STATES"""


#Sixth state - Link "yourlink" succesfully changed -> end window of branch