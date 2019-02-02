from sqlalchemy import Column, Integer, String

from bot.DataBase.models.base import Base


class Page(Base):
    __tablename__ = "page"
    id = Column(Integer, primary_key=True)
    soore_name = Column(String)
    number = Column(Integer)
    joz = Column(String)
    file_id = Column(String)
    file_access_hash = Column(String)

    def __init__(self, file_id, file_access_hash, number, joz, soore_name):
        self.file_id = file_id
        self.file_access_hash = file_access_hash
        self.number = number
        self.joz = joz
        self.soore_name = soore_name

