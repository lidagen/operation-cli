from . import config
from .env_enums import Env


class DBInstance:
    def __init__(self, host, db):
        self.host = host
        self.db = db
        self.username = config.read_config().get('db_username')
        self.username = config.read_config().get('db_password')

    def get_host(self):
        return self.host

    def get_db(self):
        return self.db


class DBInstanceMapping:
    def __init__(self):
        self.REMOTE = DBInstance(host=config.read_config().get("db_host"), db='certificate')
        self.LOCAL = DBInstance(host='127.0.0.1', db='certificate')


def __fetch(sql: str, db_instance: DBInstance):
    print(sql)

