from . import config
from .env_enums import Env
import pymysql
from . import sshtunnel_util


class DBInstance:
    def __init__(self, host, db):
        self.host = host
        self.db = db
        self.username = config.read_config().get('db_username')
        self.password = config.read_config().get('db_password')

    def get_host(self):
        return self.host

    def get_db(self):
        return self.db


class DBInstanceMapping:
    def __init__(self):
        self.REMOTE = DBInstance(host=config.read_config().get("db_host"), db='certificate')
        self.LOCAL = DBInstance(host='127.0.0.1', db='certificate')


def __fetch(sql: str, db_instance: DBInstance):
    if db_instance.get_host() != '127.0.0.1':
        print("remote")
        return sshtunnel_util.query_mysql(db_user=db_instance.username, db_password=db_instance.password,
                                   db_name=db_instance.get_db(), sql=sql)
    else:
        print("local")
        conn = pymysql.connect(host=db_instance.get_host(), port=3306, user=db_instance.username,
                               password=db_instance.password, db=db_instance.get_db())
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result
