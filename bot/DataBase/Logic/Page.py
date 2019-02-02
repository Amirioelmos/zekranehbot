import csv
from bot.DataBase.models.Page import Page
from bot.DataBase.models.migrate_table import MigrateIDS, Migrate
from bot.Utils.callbacks import my_logger
from bot.Utils.file_address import FileAddress

from bot.DataBase.models.base import Session

session = Session()

def migrate():
    migrate_id = MigrateIDS.images_page
    is_migrated = session.query(Migrate).filter(Migrate.is_migrated == migrate_id).one_or_none()
    if is_migrated:
        my_logger.info("Table Page Migrated")
        return
    else:
        session.add(Migrate(migrate_id))
        with open(FileAddress.images_page) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                session.add(Page(row[4], row[5], row[2], row[3], row[1]))
                my_logger.info("Add New Page")
            session.commit()
        # workbook = load_workbook(filename=FileAddress.images_page)
        # session.add(Migrate(migrate_id))
        # ws = workbook['images_page']
        # for i in ws:
        #     session.add(Page(i[4].value, i[5].value,i[2].value, i[3].value,i[1].value ))
        #     my_logger.info("Add New Page")
        # session.commit()


def get_page(page_number):
    return session.query(Page).filter(Page.number == int(page_number)).one_or_none()

