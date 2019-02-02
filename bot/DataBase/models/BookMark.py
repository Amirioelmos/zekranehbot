from sqlalchemy import Column, Integer, String
from bot.DataBase.models.base import Base


class BookMark(Base):
    __tablename__ = "bookmark"
    id = Column(Integer, primary_key=True)
    peer_id = Column(String)
    page_number = Column(Integer)

    def __init__(self, peer_id, page_number):
        self.peer_id = peer_id
        self.page_number = page_number
