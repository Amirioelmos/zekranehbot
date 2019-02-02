import functools
import sys
import time
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import glob
import os

import persian
from balebot.filters import *
from balebot.handlers import MessageHandler, CommandHandler

from balebot.models.messages import *


from bot.DataBase.Logic.BookMark import add_book_mark, is_marked_for_user, remove_book_mark, get_all_marked
from bot.DataBase.Logic.MainText import count_of_aye, get_aye
from bot.DataBase.Logic.MigrationManager import run_migrate
from bot.DataBase.Logic.Page import get_page
from bot.DataBase.Logic.user import is_user, add_user

from bot.DataBase.models.base import engine, Base, Session
from bot.Quran.Soore import soore_show, soore_number
from bot.Utils.base_bot import Bot
from bot.Utils.callbacks import *

# from bot.DataBase.models.base import Base, engine
from bot.Utils.constants import *



session = Session()
my_logger = Logger.get_logger()

template_bot = Bot()
bot = template_bot.bot
updater = template_bot.updater
dispatcher = template_bot.dispatcher
loop = template_bot.loop

Base.metadata.create_all(engine)

run_migrate()

#################################### Meta Functions ################################


def _get_peer(update):
    return update.get_effective_user()


def _get_msg(update):
    return update.get_effective_message()


def _formatter(id):
    return persian.convert_en_numbers(str(id))


def _return_to_back_step_check_up(msg):
    if isinstance(msg, TemplateResponseMessage):
        if msg.get_json_object()['textMessage'] == ButtonMessage.return_to_back_step:
            return True
    else:
        return False


def send_message(message, peer, step=Step.conversation_starter, succedent_message=None):
    kwargs = {UserData.user_peer: peer, UserData.step_name: step, UserData.succedent_message: succedent_message,
              UserData.message: message, UserData.attempt: SendingAttempt.first, UserData.bot: bot}
    bot.send_message(message=message, peer=peer, success_callback=step_success, failure_callback=step_failure,
                     kwargs=kwargs)


def check_message(msg, update):
    send_message(TextMessage("Check Message : {}".format(msg)), update.get_effective_user(), sys._getframe().f_code.co_name)
######################## conversation ###################





@dispatcher.message_handler(TemplateResponseFilter(pattern=Patterns.return_to_main_menu))
@dispatcher.command_handler([Command.start])
@dispatcher.default_handler()
def start_bot(bot, update):
    user = _get_peer(update)
    _is_user = is_user(user.peer_id)
    if _is_user:
        txt = BotMessage.choose_one_option
        txt_msg = TextMessage(txt)
        btn = [
            TemplateMessageButton(ButtonMessage.tarjome, ButtonMessage.tarjome, ButtonAction.default),
            TemplateMessageButton(ButtonMessage.tafsir, ButtonMessage.tafsir, ButtonAction.default),
            TemplateMessageButton(ButtonMessage.read, ButtonMessage.read, ButtonAction.default)
        ]
        msg = TemplateMessage(txt_msg, btn)
        send_message(msg, _get_peer(update), Step.showing_menu)
        dispatcher.register_conversation_next_step_handler(update, [
            MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.tarjome), tarjome_step_1),
            MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.tafsir), tafsir_step_1),
            MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.read), read_step_1),
            MessageHandler(DefaultFilter(), start_bot)
        ])
    else:
        add_user(user.peer_id, user.access_hash)
        txt = BotMessage.greeting
        txt_msg = TextMessage(txt)
        btn = [
            TemplateMessageButton(ButtonMessage.tarjome, ButtonMessage.tarjome, ButtonAction.default),
            TemplateMessageButton(ButtonMessage.tafsir, ButtonMessage.tafsir, ButtonAction.default),
            TemplateMessageButton(ButtonMessage.read, ButtonMessage.read, ButtonAction.default)
        ]
        msg = TemplateMessage(txt_msg, btn)
        send_message(msg, _get_peer(update), Step.showing_menu)
        dispatcher.register_conversation_next_step_handler(update, [
            MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.tarjome), tarjome_step_1),
            MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.tafsir), tafsir_step_1),
            MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.read), read_step_1),
            MessageHandler(DefaultFilter(), start_bot)
        ])


def tarjome_step_1(bot, update, start=1, end=30):
    txt = BotMessage.choose_soore
    txt_msg = TextMessage(txt)
    soore_list = soore_show(start, end)
    btn = []
    for soore in soore_list:
        btn.append(TemplateMessageButton(soore, soore, 0))
    if end < 114:
        btn.append(TemplateMessageButton(ButtonMessage.show_more, ButtonMessage.show_more, 0))
    btn.append(TemplateMessageButton(ButtonMessage.return_to_main_menu, ButtonMessage.return_to_main_menu, 0))
    msg = TemplateMessage(txt_msg, btn)
    send_message(msg, _get_peer(update), Step.conversation_starter)
    dispatcher.register_conversation_next_step_handler(update, [
        MessageHandler(TemplateResponseFilter(keywords=soore_show(1, 114)), tarjome_step_2),
        MessageHandler(TemplateResponseFilter(keywords=soore_show(1, 114)), tarjome_step_2),
        MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.show_more),
                       functools.partial(tarjome_step_1, start=end+1, end=end+30)),
        MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.return_to_main_menu), start_bot),
        MessageHandler(DefaultFilter(), start_bot)

    ])


def tarjome_step_2(bot, update):
    msg = _get_msg(update)
    if isinstance(msg, TemplateResponseMessage):
        soore = msg.get_json_object()['textMessage']
        if soore == ButtonMessage.return_to_main_menu:
            start_bot(bot, update)
            return
        dispatcher.set_conversation_data(update, "soore", soore)
        num = soore_number(soore)
        number_of_ayes = count_of_aye(num)
        txt_msg = TextMessage(BotMessage.choose_aye_number.format(soore, persian.convert_en_numbers(number_of_ayes)))
        dispatcher.set_conversation_data(update, "number_of_ayes", number_of_ayes)
        dispatcher.set_conversation_data(update, "soore_number", num)
        send_message(txt_msg, _get_peer(update), Step.conversation_starter)
        dispatcher.register_conversation_next_step_handler(update, [
            MessageHandler(TextFilter(), tarjome_step_3),
            MessageHandler(DefaultFilter(), start_bot)
        ])


def tarjome_step_3(_, update):
    # check_message("s + {}".format(_get_msg(update).text), update)
    msg = _get_msg(update).text
    number_of_ayes = dispatcher.get_conversation_data(update, "number_of_ayes")
    if msg.isnumeric() and 1 <= int(msg) <= number_of_ayes:
        soore_number = dispatcher.get_conversation_data(update, "soore_number")
        soore = dispatcher.get_conversation_data(update, "soore")
        aye = get_aye(soore_number, int(msg))
        aye_text = aye.aye_text
        tarjome_text = aye.tarjome_text
        btn = [
            TemplateMessageButton(ButtonMessage.tarjome, ButtonMessage.tarjome, 0),
            TemplateMessageButton(ButtonMessage.tafsir, ButtonMessage.tafsir, 0),
            TemplateMessageButton(ButtonMessage.read, ButtonMessage.read, ButtonAction.default)
        ]

        def send_done(_, __):
            continue_msg = TextMessage(BotMessage.continue_msg)
            _msg = TemplateMessage(continue_msg, btn)
            send_message(_msg, _get_peer(update))
            dispatcher.register_conversation_next_step_handler(update, [
                MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.tafsir), tafsir_step_1),
                MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.tarjome), tarjome_step_1),
                MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.read), read_step_1),
                MessageHandler(DefaultFilter(), start_bot)
            ])

        def send_fail(_, __):
            pass

        text_aye = BotMessage.aye_text.format(soore, persian.convert_en_numbers(int(msg)), aye_text)
        text_tarjome = BotMessage.tarjome_text.format(tarjome_text)
        all_msg = TextMessage(text_aye + "\n" + text_tarjome)
        bot.send_message(all_msg, _get_peer(update), success_callback=send_done, failure_callback=send_fail)

    else:
        soore = dispatcher.get_conversation_data(update, "soore")
        txt_msg = TextMessage(BotMessage.wrong_input + "\n" + BotMessage.choose_aye_number.format(soore,
                                                                persian.convert_en_numbers(number_of_ayes)))
        send_message(txt_msg, _get_peer(update), Step.conversation_starter)
        dispatcher.register_conversation_next_step_handler(update, [
            MessageHandler(TextFilter(), tarjome_step_3),
            MessageHandler(DefaultFilter(), start_bot),
            CommandHandler(Command.start, start_bot),
        ])


def tafsir_step_1(bot, update, start=1, end=30):
    txt = BotMessage.choose_soore
    txt_msg = TextMessage(txt)
    soore_list = soore_show(start, end)
    btn = []
    for soore in soore_list:
        btn.append(TemplateMessageButton(soore, soore, 0))
    if end < 114:
        btn.append(TemplateMessageButton(ButtonMessage.show_more, ButtonMessage.show_more, 0))
    btn.append(TemplateMessageButton(ButtonMessage.return_to_main_menu, ButtonMessage.return_to_main_menu, 0))
    msg = TemplateMessage(txt_msg, btn)
    send_message(msg, _get_peer(update), Step.conversation_starter)
    dispatcher.register_conversation_next_step_handler(update, [
        MessageHandler(TemplateResponseFilter(keywords=soore_show(1, 114)), tafsir_step_2),
        MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.show_more),
                       functools.partial(tafsir_step_1, start=end+1, end=end+30)),
        MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.return_to_main_menu), start_bot),
        MessageHandler(DefaultFilter(), tafsir_step_1)
    ])


def tafsir_step_2(bot, update):
    msg = _get_msg(update)
    if isinstance(msg, TemplateResponseMessage):
        soore = msg.get_json_object()['textMessage']
        if soore == ButtonMessage.return_to_main_menu:
            start_bot(bot, update)
            return
        dispatcher.set_conversation_data(update, "soore", soore)
        num = soore_number(soore)
        dispatcher.set_conversation_data(update, "soore_number", num)
        number_of_ayes = count_of_aye(num)
        txt_msg = TextMessage(BotMessage.choose_aye_number.format(soore, persian.convert_en_numbers(number_of_ayes)))
        dispatcher.set_conversation_data(update, "number_of_ayes", number_of_ayes)
        send_message(txt_msg, _get_peer(update), Step.conversation_starter)
        dispatcher.register_conversation_next_step_handler(update, [
            MessageHandler(TextFilter(), tafsir_step_3)
        ])


def tafsir_step_3(_, update):
    # check_message("s + {}".format(_get_msg(update).text), update)
    msg = _get_msg(update).text
    number_of_ayes = dispatcher.get_conversation_data(update, "number_of_ayes")
    if msg.isnumeric() and 1 <= int(msg) <= number_of_ayes:
        soore_number = dispatcher.get_conversation_data(update, "soore_number")
        soore = dispatcher.get_conversation_data(update, "soore")
        aye = get_aye(soore_number, int(msg))
        aye_text = aye.aye_text
        tafsir_text = aye.tafsir_text
        btn = [
            TemplateMessageButton(ButtonMessage.tarjome, ButtonMessage.tarjome, 0),
            TemplateMessageButton(ButtonMessage.tafsir, ButtonMessage.tafsir, 0),
            TemplateMessageButton(ButtonMessage.read, ButtonMessage.read, ButtonAction.default)
        ]

        def send_done(_, __):
            continue_msg = TextMessage(BotMessage.continue_msg)
            _msg = TemplateMessage(continue_msg, btn)
            send_message(_msg, _get_peer(update))
            dispatcher.register_conversation_next_step_handler(update, [
                MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.tafsir), tafsir_step_1),
                MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.tarjome), tarjome_step_1),
                MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.read), read_step_1),
                MessageHandler(DefaultFilter(), start_bot)
            ])

        def send_fail(_, __):
            pass

        text_aye = BotMessage.aye_text.format(soore, persian.convert_en_numbers(int(msg)), aye_text)
        text_tafsir = BotMessage.tafsir_text.format(tafsir_text)
        all_msg = TextMessage(text_aye + "\n" + text_tafsir)
        bot.send_message(all_msg, _get_peer(update), success_callback=send_done, failure_callback=send_fail)
    else:
        soore = dispatcher.get_conversation_data(update, "soore")
        txt_msg = TextMessage(BotMessage.wrong_input + "\n" + BotMessage.choose_aye_number.format(soore,
                                                                persian.convert_en_numbers(number_of_ayes)))
        send_message(txt_msg, _get_peer(update), Step.conversation_starter)
        dispatcher.register_conversation_next_step_handler(update, [
            MessageHandler(TextFilter(), tafsir_step_3),
            MessageHandler(DefaultFilter(), start_bot),
            CommandHandler(Command.start, start_bot),
        ])

@dispatcher.message_handler(filters=[
    TextFilter(pattern=Regex.numbers),
    TemplateResponseFilter(keywords=ButtonMessage.read)
])
def read_step_1(bot, update, wrong_input=False):
    user = _get_peer(update)
    text = ""
    if wrong_input:
        text = BotMessage.wrong_input_page + "\n" + BotMessage.choose_page_number

    all_marked = get_all_marked(user.peer_id)
    btn = []
    keywords = []
    my_logger.info("\n\n\n\n\n\n\n all Marked : {}\n\n\n\n\n\n".format(all_marked))
    if len(all_marked) > 0:
        text = BotMessage.choose_page_book_mark + " " + BotMessage.choose_page_number
        for mark in all_marked:
            btn.append(TemplateMessageButton(text=ButtonMessage.read_page.format(persian.convert_en_numbers(mark[0])),
                                             value=mark[0], action=0))
            keywords.append(str(mark[0]))
    else:
        text = BotMessage.choose_page_number

    btn.append(TemplateMessageButton(ButtonMessage.return_to_main_menu, ButtonMessage.return_to_main_menu, 0))
    txt_msg = TextMessage(text)
    message = TemplateMessage(txt_msg, btn)
    send_message(message, _get_peer(update))
    dispatcher.register_conversation_next_step_handler(update, [
        MessageHandler(TemplateResponseFilter(keywords=keywords), read_step_2),
        MessageHandler(TextFilter(), read_step_2),
        MessageHandler(DefaultFilter(), start_bot),
    ])


def read_step_2(bot, update, change_page=None):

    user = _get_peer(update)
    msg = _get_msg(update)

    if change_page:
        page_number = change_page
    else:
        if isinstance(msg, TemplateResponseMessage):
            page_number = msg.text_message
        else:
            page_number = _get_msg(update).text

    if 0 < int(page_number) < 605:
        page_number = int(page_number)
        page = get_page(page_number)
        msg = PhotoMessage(file_id=page.file_id, access_hash=page.file_access_hash,
                           name="Page.jpg", file_size=500000, mime_type="image/jpeg",
                           thumb=UserData.thumb,
                           ext_width=1260, ext_height=2038,
                           height=80, width=80,
                           file_storage_version=1,
                           caption_text=TextMessage("صفحه: *{}*\n - سوره مبارکه: *{}*\n - جزء: *{}*"
                                                    .format(persian.convert_en_numbers(page_number),
                                                            page.soore_name,
                                                            page.joz)))

        def send_done(_, __):
            btn = [
                TemplateMessageButton(ButtonMessage.next_page, ButtonMessage.next_page, 0),
                TemplateMessageButton(ButtonMessage.before_page, ButtonMessage.before_page, 0),


            ]
            is_marked = is_marked_for_user(user.peer_id, page_number)
            my_logger.info("is marked : {}".format(is_marked))
            if is_marked:
                btn.append(TemplateMessageButton(ButtonMessage.remove_from_book_mark,
                                                 ButtonMessage.remove_from_book_mark, 0))
            else:
                btn.append(TemplateMessageButton(ButtonMessage.add_to_book_mark, ButtonMessage.add_to_book_mark, 0))

            btn.append(TemplateMessageButton(ButtonMessage.return_to_main_menu, ButtonMessage.return_to_main_menu, 0))
            continue_msg = TextMessage(BotMessage.continue_msg)
            _msg = TemplateMessage(continue_msg, btn)
            send_message(_msg, _get_peer(update))
            dispatcher.register_conversation_next_step_handler(update, [
                MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.next_page), functools.partial(
                    read_step_2, change_page=page_number + 1)),
                MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.before_page), functools.partial(
                    read_step_2, change_page=page_number - 1)),
                MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.read), read_step_1),
                MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.add_to_book_mark),
                               functools.partial(add_to_book_mark, page_number=page_number)),
                MessageHandler(TemplateResponseFilter(keywords=ButtonMessage.remove_from_book_mark),
                               functools.partial(remove_from_book_mark, page_number=page_number)),

                MessageHandler(DefaultFilter(), start_bot)
            ])

        def send_fail(_, __):
            pass
        bot.send_message(msg, _get_peer(update), success_callback=send_done, failure_callback=send_fail)

    else:
        read_step_1(bot, update, wrong_input=True)


def add_to_book_mark(bot, update, page_number):
    user = _get_peer(update)
    is_added = add_book_mark(peer_id=user.peer_id, page_number=page_number)
    if is_added == 1:
        text_message = TextMessage(BotMessage.added_to_book_mark.format(persian.convert_en_numbers(page_number)))
        btn = [
            TemplateMessageButton(ButtonMessage.back_to_read.format(persian.convert_en_numbers(page_number)),
                                  ButtonMessage.back_to_read.format(persian.convert_en_numbers(page_number)), 0),
            TemplateMessageButton(ButtonMessage.return_to_main_menu, ButtonMessage.return_to_main_menu, 0)
        ]
        message = TemplateMessage(text_message, btn)
        send_message(message=message, peer=user)
        dispatcher.register_conversation_next_step_handler(update, [
            MessageHandler(TemplateResponseFilter(
                keywords=ButtonMessage.back_to_read.format(persian.convert_en_numbers(page_number))),
                           functools.partial(read_step_2, change_page=page_number)),
            MessageHandler(DefaultFilter(), start_bot)
        ])

def remove_from_book_mark(bot, update, page_number):
    user = _get_peer(update)
    is_removed = remove_book_mark(peer_id=user.peer_id, page_number=page_number)
    if is_removed == 1:
        text_message = TextMessage(BotMessage.removed_from_book_mark.format(persian.convert_en_numbers(page_number)))
        btn = [
            TemplateMessageButton(ButtonMessage.back_to_read.format(persian.convert_en_numbers(page_number)),
                                  ButtonMessage.back_to_read.format(persian.convert_en_numbers(page_number)), 0),
            TemplateMessageButton(ButtonMessage.return_to_main_menu, ButtonMessage.return_to_main_menu, 0)
        ]
        message = TemplateMessage(text_message, btn)
        send_message(message=message, peer=user)
        dispatcher.register_conversation_next_step_handler(update, [
            MessageHandler(TemplateResponseFilter(
                keywords=ButtonMessage.back_to_read.format(persian.convert_en_numbers(page_number))),
                           functools.partial(read_step_2, change_page=page_number)),
            MessageHandler(DefaultFilter(), start_bot)
        ])
    else:
        check_message("asdasdasd", update)

@dispatcher.command_handler([Command.help])
def upload(bot, update):
    page = session.queryi(Page).filter(Page.number == 333).one_or_none()
    msg = PhotoMessage(file_id=page.file_id, access_hash=page.file_access_hash,
                       name="Page", file_size=987, mime_type="image/jpeg",
                       thumb=UserData.thumb,width=1260, height=2038,
                       file_storage_version=1,
                       caption_text=TextMessage("soore : {}, joz  : {}".format(page.soore_name, page.joz)))
    send_message(msg, _get_peer(update))
    # all_pages = session.query(Page).all()
    # workbook = load_workbook(filename=FileAddress.page_info)
    # ws = workbook['Sheet']
    # for page in all_pages:
    #     for row in ws:
    #         if row[0].value == page.number:
    #             page.soore_name = row[1].value
    #             page.joz = row[2].value
    #             my_logger.info("Update Page : {}, Soore : {}, Joz : {}".format(page.number, page.soore_name, page.joz))
    #             session.commit()
    # images_address = glob.glob(FileAddress.all_images)
    # imgae_countrt = 0
    # for image in images_address:
    #     kwargs = {}
    #     number = image.split("/")[-1].split(".")[0].replace("page", "")
    #

            # def pdf_upload_success(result, user_data):
            #     file_id = str(user_data.get("file_id", None))
            #     access_hash = str(user_data.get("user_id", None))
            #     user_data = user_data[UserData.kwargs]
            #     _number = user_data[UserData.number]
            #     new_img = Page(file_id=file_id, file_access_hash=access_hash, number=_number)
            #     session.add(new_img)
            #     session.commit()
            #     my_logger.info("New Image added : {}".format(_number))
            #
            #
            # def file_upload_failed(_, __):
            #     pass
            #
            # number = image.split("/")[-1].split(".")[0].replace("page","")
            # path_to_file = image
            # kwargs.update({"number" : number , "path" : path_to_file})
            # bot.upload_file(file=image, file_type="file",
            #                 success_callback=pdf_upload_success,
            #                 failure_callback=file_upload_failed,
            #                 kwargs=kwargs)


updater.run()
