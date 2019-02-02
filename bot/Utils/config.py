import os
import logging


class BotConfig:
    project_path = os.getcwd()
    daily_report_filename = None
    full_report_filename = None
    root_admin = os.environ.get('BOT_ADMIN_ID', '1471278867')
    reports_route = "files/"
    base_url = os.environ.get('BASE_URL', None) or "wss://api.bale.ai/v1/bots/"
    bot_token = os.environ.get('TOKEN', None) or "a2a98561c716dd10f10c20d5cbda0a8f2477692f"
    system_local = os.environ.get('SYSTEM_LOCAL', None) or "fa_IR"
    resending_max_try = int(os.environ.get('RESENDING_MAX_TRY', 5))
    reuploading_max_try = int(os.environ.get('REUPLOADING_MAX_TRY', 5))


class DbConfig:
    db_user = os.environ.get('POSTGRES_USER', None)
    db_password = os.environ.get('POSTGRES_PASSWORD', None)
    db_host = os.environ.get('POSTGRES_HOST', None)
    db_name = os.environ.get('POSTGRES_DB', None)
    db_port = os.environ.get('POSTGRES_PORT', None)
    database_url = "postgresql://{}:{}@{}:{}/{}".format(db_user, db_password, db_host, db_port, db_name) or None
    # database_url = "postgresql://postgres:nader1993@localhost:5432/testdb"
