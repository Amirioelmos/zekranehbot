from balebot.utils.logger import Logger

from bot.DataBase.models.BookMark import BookMark
from bot.DataBase.models.base import Session

session = Session()
my_logger = Logger.get_logger()


def add_book_mark(peer_id, page_number):
    bm = BookMark(peer_id=peer_id, page_number=page_number)
    try:
        session.add(bm)
        session.commit()
        return 1
    except Exception as e:
        my_logger.info("Add BookMark Failed : {}".format(e))
        return 0


def is_marked_for_user(peer_id, page_number):
    return session.query(BookMark).filter(
        BookMark.peer_id == peer_id).filter(
        BookMark.page_number == page_number).one_or_none()


def remove_book_mark(peer_id, page_number):
    try:
        session.query(BookMark).filter(
            BookMark.peer_id == peer_id).filter(
            BookMark.page_number == page_number).delete(synchronize_session=False)
        session.commit()
        return 1
    except Exception as e:
        my_logger.info("Add BookMark Failed : {}".format(e))
        return 0


def get_all_marked(peer_id):
    return session.query(BookMark.page_number).filter(BookMark.peer_id == peer_id).all()