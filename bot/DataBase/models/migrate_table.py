from sqlalchemy import Column, Integer, String

from bot.DataBase.models.base import Base


class Migrate(Base):
    __tablename__ = "migrate"
    id = Column(Integer, primary_key=True)
    is_migrated = Column(String)

    def __init__(self, migrate_id):
        self.is_migrated = migrate_id


class MigrateIDS():
    main_text = "main_text"
    images_page = "images_page"