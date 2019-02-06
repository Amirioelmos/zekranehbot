
from bot.DataBase.models.base import Session
from bot.DataBase.models.user import User
from bot.Utils.callbacks import my_logger

session = Session()


def is_user(peer_id):
    try:
        user = session.query(User).filter(User.peer_id == peer_id).first()
        if user:
            return True
        else:
            return False

    except Exception as e:
        return False


def add_user(peer_id, access_hash):
    user = User(peer_id=peer_id, access_hash=access_hash)
    try:
        session.add(user)
        session.commit()
        my_logger.info("Adding new user")
    except Exception as e:
        session.rollback()
        my_logger.info("Adding new user failed, {}".format(e))

def get_all_users():
    try:
        return session.query(User).all()
    except Exception as e:
        my_logger.info("Fail to Load all Users. : {}".format(e))
        return 0