
from bot.DataBase.Logic import Page, MainText


def run_migrate():
    Page.migrate()
    MainText.migrate()
