from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from bot.DataBase.models.base import Base


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref=backref("admins", cascade="all, delete-orphan"))
    type = Column(String, default="support")

    def __init__(self, user):
        self.user = user
