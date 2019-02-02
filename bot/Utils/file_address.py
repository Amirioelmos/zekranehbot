from bot.Utils.config import BotConfig
import os


class FileAddress:
    all_text = os.path.join(BotConfig.project_path, "bot/files/all_text.xlsx")
    all_images = os.path.join(BotConfig.project_path, "bot/files/images/*.jpg")
    page_info = os.path.join(BotConfig.project_path, "bot/files/page_info.xlsx")
    images_page = os.path.join(BotConfig.project_path, "bot/files/images_page.csv")