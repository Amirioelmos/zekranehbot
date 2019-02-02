from sqlalchemy import Column, Integer, String

from bot.DataBase.models.base import Base


class MainText(Base):
    __tablename__ = "main_text"
    id = Column(Integer, primary_key=True)
    soore_number = Column(Integer)
    soore_name = Column(String)
    aye_number = Column(Integer)
    aye_text = Column(String)
    tarjome_text = Column(String)
    tafsir_text = Column(String)

    def __init__(self, soore_number, soore_name, aye_number, aye_text, tarjome_text, tafsir_text):
        self.soore_number = soore_number
        self.soore_name = soore_name
        self.aye_number = aye_number
        self.aye_text = aye_text
        self.tarjome_text = tarjome_text
        self.tafsir_text = tafsir_text
