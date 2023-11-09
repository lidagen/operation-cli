from sshtunnel import SSHTunnelForwarder
from . import config
import pymysql


def query_mysql(db_user, db_password, db_name, sql):
    with  SSHTunnelForwarder(
            (config.read_config().get('remote_host'), 22),  # ssh远程服务器和端口
            ssh_username=config.read_config().get('remote_user'),  # ssh user
            ssh_password=config.read_config().get('remote_password'),  # ssh password
            remote_bind_address=('127.0.0.1', 3306),
            # local_bind_addresses=('127.0.0.1', 13306)
    ) as server:
        print(f"server.port:{server.local_bind_port}")
        conn = pymysql.connect(
            host='127.0.0.1',
            port=server.local_bind_port,  # ssh目标服务器用于连接mysql服务器的端口
            user=db_user,
            password=db_password,
            database=db_name,
            charset='utf8'
        )
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()

        except Exception as e:
            print(f"SQL Error :{e}")
