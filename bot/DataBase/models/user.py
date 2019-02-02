from sqlalchemy import Column, Integer, String

from bot.DataBase.models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    peer_id = Column(String)
    access_hash = Column(String)

    def __init__(self, peer_id, access_hash):
        self.peer_id = peer_id
        self.access_hash = access_hash

