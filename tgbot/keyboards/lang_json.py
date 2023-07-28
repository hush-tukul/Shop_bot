import logging

from db import Reflink

all_langs = {


    'EN': {
        ('~~~~~&lt; MAIN MENU &gt;~~~~~', 'main_menu'): {
            ('-----------------  Your links  -----------------', 'links'): {
                ('--------------------  Change link  --------------------', 'change_link'): {
                    ('--------------------  Please add a new link  --------------------', 'add_link'): {
                        ('Your link has been changed', 'link_changed'),
                        ('Your link has been created', 'link_created')
                    },
                },
                ('--------------------  Link statistic  --------------------', 'link_stat'): {},
                ('--------------------  Show referral link  --------------------', 'show_ref_link'): {
                    ('Referral link: ', 'ref_link'): {}
                    },
                ('--------------------  Delete link  --------------------', 'del_link'): {
                    ('--------------------  Please confirm deletion  --------------------', 'del_link'): {
                    },
                },
            },
            ('-----------  General statistics -------------', 'global_stats'): {},
            ('-----------------  Instruction  -----------------', 'all_instructions'): {},
            ('------------  Change language  ------------', 'change_lang'): {},
            ('----------  Contacts / Feedback  ----------', "reasons_feedback"): {},

            },
        },
    }
    # 'UA': {
    #     ('Головне меню', 'main_menu'): {
    #         ('Ваші посилання', 'links'): {
    #             ('Обране посилання', 'chosen_link'): {
    #                 ('Змінити посилання', 'change_link'): {
    #                     ('Введіть будь ласка нове посилання', 'insert_link'):
    #                         'Ваше посилання було змінене'
    #                     },
    #                 },
    #
    #             },
    #         ('Загальна статистика', 'global_stats'): {},
    #         ('Інструкція', 'all_instructions'): {},
    #         ('Змінити мову', 'change_lang'): {},
    #         ("Контакти / Зворотній зв'язок", "contact_feedback"): {},
    #         },
    #     },
    # 'RU':
    #     {
    #         ('Главное меню', 'main_menu'): {
    #             ('Ваши ссылки', 'links'): {
    #                 ('Выбранная ссылка', 'chosen_link'): {
    #                     ('Изменить ссылку', 'change_link'): {
    #                         ('Введите, пожалуйста, новую ссылку', 'insert_link'):
    #                             'Ваша ссылка была изменeна'
    #                     }
    #                 },
    #             },
    #             ('Общая статистика', 'global_stats'): {},
    #             ('Инструкция', 'all_instructions'): {},
    #             ('Поменять язык', 'change_lang'): {},
    #             ("Контакты / Обратная связь", "contact_feedback"): {},
    #             },
    #         }
    #
    #
    #     }


def title(user_lang):
    return [i for i in all_langs[user_lang].keys() if i[1] == 'main_menu']



def title_buttons(user_lang):
    return list(all_langs[user_lang][title(user_lang)[0]].keys())


def option_title(user_lang, option):
    return [i for i in title_buttons(user_lang) if i[1] == option]


def option_buttons(user_lang, option):
    lang_links = option_title(user_lang, option)[0]
    logging.info(lang_links)
    target_key = list(all_langs[user_lang][title(user_lang)[0]][lang_links].keys())
    return target_key


def action_of_option_button(user_lang, option, action):
    if action:
        action_button = [i for i in option_buttons(user_lang, option) if action in i]
        logging.info(f"action_of_option_button: {action_button}")
    else:
        action_button = [i for i in option_buttons(user_lang, option) if 'change_link' in i]
        logging.info(f"action_of_option_button: {action_button}")
    return action_button

def action_confirm_button(user_lang, option, action):
    lang_links = option_title(user_lang, option)[0]

    confirm = action_of_option_button(user_lang, option, action)[0]
    logging.info(f"action_confirm_button/action_of_option_button: {confirm}")
    r = [confirm, list(all_langs[user_lang][title(user_lang)[0]][lang_links][confirm].keys())]
    logging.info(f"action_confirm_button/list of buttons: {r}")
    return r



def links_list(user_lang, option, user_id):
    lang_links = option_title(user_lang, option)[0]
    logging.info(lang_links)
    g = option_buttons(user_lang, option)[0]
    link_id = Reflink.get_link_id
    target_key = list(all_langs[user_lang][title(user_lang)[0]][lang_links][g])
    if Reflink.get_user_links(user_id):
        link_options = [(i, link_id(i)) for i in Reflink.get_user_links(user_id)]
        link_options.append(target_key[0])
        return [lang_links[0], link_options]
    else:
        return [target_key[0][0], []]
    # return [lang_links[0], [(i, i) for i in Reflink.get_user_links(user_id)]] if Reflink.get_user_links(user_id) \
    #     else [target_key[0][0], []]




# title = [i for i, j in all_langs['UA'].keys() if j == 'main_menu'][0]
# g = list(all_langs['UA'][(title, 'main_menu')].keys())
#
# print(g)
# logging.info(title_buttons('EN'))
# logging.info(option_title('EN', 'links'))
#logging.info(option_buttons('EN', 'links'))
logging.info(links_list('EN', 'links', 683497406))
#logging.info(action_confirm_button('EN', 'links', 'change_link'))