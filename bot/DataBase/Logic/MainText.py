from balebot.utils.logger import Logger
from openpyxl import load_workbook
from sqlalchemy import func

from bot.DataBase.models.MainText import MainText
from bot.DataBase.models.base import Session
from bot.DataBase.models.migrate_table import MigrateIDS, Migrate
from bot.Quran.Soore import soore_name
from bot.Utils.file_address import FileAddress

session = Session()
my_logger = Logger.get_logger()


def migrate():
    migrate_id = MigrateIDS.main_text
    is_migrated = session.query(Migrate).filter(Migrate.is_migrated == migrate_id).one_or_none()
    if is_migrated:
        my_logger.info("Table MainText Migrated")
        return
    else:
        workbook = load_workbook(filename=FileAddress.all_text)
        session.add(Migrate(migrate_id))
        ws = workbook['Sheet']
        for i in ws:
            session.add(MainText(i[0].value, soore_name(i[0].value), i[1].value, i[2].value, i[3].value, i[4].value))
            my_logger.info("Add New Aye")
        session.commit()


def count_of_aye(soore_number):
    return session.query(func.count(MainText.id)).filter(MainText.soore_number == soore_number).one_or_none()[0]


def get_aye(soore_number, aye_number):
    my_logger.info("asdasad : {}, sadkljahsd : {}".format(soore_number, aye_number))
    aye = session.query(MainText).filter(MainText.soore_number == soore_number).filter(
        MainText.aye_number == aye_number).one_or_none()
    my_logger.info("ayyyyyyyyyyye : {}".format(aye))
    return aye