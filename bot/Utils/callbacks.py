import os

from balebot.models.constants.file_type import FileType
from balebot.models.messages import TextMessage, DocumentMessage
from balebot.utils.logger import Logger
from bot.Utils.config import BotConfig
from bot.Utils.constants import UserData, LogMessage, MimeType, BotMessage, SendingAttempt, Step

my_logger = Logger.get_logger()


def step_success(response, user_data):
    user_data = user_data[UserData.kwargs]
    user_peer = user_data[UserData.user_peer]
    step_name = user_data[UserData.step_name]
    my_logger.info(LogMessage.successful_step_message_sending,
                   extra={UserData.user_id: user_peer.peer_id, UserData.step_name: step_name, "tag": "info"})
    if user_data.get(UserData.succedent_message):
        bot = user_data[UserData.bot]
        step_name = user_data[UserData.step_name]
        succedent_message = user_data[UserData.succedent_message]
        kwargs = {UserData.user_peer: user_peer, UserData.step_name: step_name,
                  UserData.message: succedent_message, UserData.attempt: SendingAttempt.first,
                  UserData.logger: my_logger, UserData.bot: bot}
        bot.send_message(message=succedent_message, peer=user_peer, success_callback=step_success,
                         failure_callback=step_failure, kwargs=kwargs)


def step_failure(response, user_data):
    user_data = user_data[UserData.kwargs]
    user_peer = user_data[UserData.user_peer]
    step_name = user_data[UserData.step_name]
    bot = user_data[UserData.bot]
    message = user_data[UserData.message]
    user_data[UserData.attempt] += 1
    if user_data[UserData.attempt] < BotConfig.resending_max_try:
        bot.send_message(message=message, peer=user_peer, success_callback=step_success, failure_callback=step_failure,
                         kwargs=user_data)
        return
    my_logger.error(LogMessage.failed_step_message_sending,
                    extra={UserData.user_id: user_peer.peer_id, UserData.step_name: step_name, "tag": "error"})


def full_report_upload_success(result, user_data):
    file_id = str(user_data.get(UserData.file_id, None))
    file_url = str(user_data.get(UserData.url))
    access_hash = str(user_data.get(UserData.user_id, None))
    user_data = user_data[UserData.kwargs]
    bot = user_data[UserData.bot]
    user_peer = user_data[UserData.user_peer]
    record_changes_num = user_data[UserData.record_changes_num]

    my_logger.info(LogMessage.successful_report_upload,
                   extra={UserData.file_url: file_url, "tag": "info"})
    file_size = os.path.getsize(BotConfig.reports_route + BotConfig.full_report_filename)
    doc_message = DocumentMessage(file_id=file_id, access_hash=access_hash, name=BotConfig.full_report_filename,
                                  file_size=file_size, mime_type=MimeType.xlsx,
                                  caption_text=TextMessage(BotMessage.full_report_body.format(
                                      record_changes_num[0], record_changes_num[1], record_changes_num[2],
                                      record_changes_num[3], record_changes_num[4], record_changes_num[5],
                                      record_changes_num[6], record_changes_num[7])))
    # loop.call_soon(send_message, message, admin_peer)
    kwargs = {UserData.user_peer: user_peer, UserData.doc_message: doc_message,
              UserData.report_attempt: SendingAttempt.first, UserData.logger: my_logger, UserData.bot: bot}
    bot.send_message(doc_message, user_peer, success_callback=report_success,
                     failure_callback=report_failure, kwargs=kwargs)


def full_report_upload_failure(result, user_data):
    user_data = user_data[UserData.kwargs]
    user_peer = user_data[UserData.user_peer]
    bot = user_data[UserData.bot]
    upload_attempt = user_data[UserData.attempt]
    upload_attempt += 1
    if upload_attempt <= BotConfig.reuploading_max_try:
        kwargs = {UserData.user_peer: user_peer,
                  UserData.attempt: upload_attempt, UserData.logger: my_logger, UserData.bot: bot}
        bot.upload_file(file=BotConfig.reports_route + BotConfig.full_report_filename, file_type=FileType.file,
                        success_callback=full_report_upload_success,
                        failure_callback=full_report_upload_failure, kwargs=kwargs)
        return
    message = TextMessage(BotMessage.upload_failed)
    kwargs = {UserData.user_peer: user_peer, UserData.message: message, UserData.step_name: Step.upload_fail,
              UserData.attempt: SendingAttempt.first, UserData.logger: my_logger, UserData.bot: bot}
    bot.send_message(message, user_peer, success_callback=step_success, failure_callback=step_failure, kwargs=kwargs)
    my_logger.error(LogMessage.failed_report_upload,
                    extra={UserData.user_id: user_peer.peer_id, "tag": "error"})


def report_success(response, user_data):
    user_data = user_data[UserData.kwargs]
    my_logger.info(LogMessage.successful_report_sending,
                   extra={UserData.user_id: user_data[UserData.user_peer].peer_id, "tag": "info"})


def report_failure(response, user_data):
    user_data = user_data[UserData.kwargs]
    bot = user_data[UserData.bot]
    user_data[UserData.report_attempt] += 1
    if user_data[UserData.report_attempt] <= BotConfig.resending_max_try:
        bot.send_message(user_data[UserData.doc_message], user_data[UserData.user_peer],
                         success_callback=report_success,
                         failure_callback=report_failure, kwargs=user_data)
        return
    my_logger.error(LogMessage.failed_report_sending,
                    extra={UserData.user_id: user_data[UserData.user_peer].peer_id, "tag": "info"})
