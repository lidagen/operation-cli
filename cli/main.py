# This is a sample Python script.
import os

import click
import typer
from rich import print, box
from .utils import config
from .utils.env_enums import Env
from rich.table import Table
from .utils.database_helper import DBInstanceMapping, __fetch
from .utils import jwt_utils
from .utils import fanyi_baidu_helper
from .utils import gemini_uitl
from .utils import sqlite3_util
from volcengine.maas import MaasService, MaasException, ChatRole

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
app = typer.Typer(rich_markup_mode="rich")


@app.callback()
def callback(ctx: typer.Context):
    """
    config is not null
    """
    if ctx.invoked_subcommand != 'configure' and config.is_valid() is False:
        print('Please run `opscli configure` to configure the essential information.')
        raise typer.Exit()


@app.command()
def configure(
        salt: str = typer.Option(..., prompt=True),  # 6位
        db_username: str = typer.Option(..., prompt=True),
        db_password: str = typer.Option(..., prompt=True, hide_input=True, confirmation_prompt=True),

):
    config_content = {
        "db_username": db_username,
        "db_password": db_password,
        "env": "LOCAL",
        "salt": salt,
        "db_host": "127.0.0.1",
    }
    config.init(config_content)


@app.command()
def env():
    env_mapping = {
        '1': Env.REMOTE,
        '2': Env.LOCAL
    }
    print('OPSCLI environment:')
    for number in env_mapping.keys():
        print(f'[{number}] -> {env_mapping[number].value}')
    env_index = typer.prompt('Select apply environment', type=click.Choice(env_mapping.keys()), show_choices=False)
    env_name = env_mapping.get(env_index, Env.REMOTE).value
    config.append_config_item({'env': env_name})
    _host = '127.0.0.1'
    config.append_config_item({'db_host': _host})
    if env_name == Env.REMOTE.value:
        _host = typer.prompt("input remote server host", default=_host, hide_input=True)
        remote_user = typer.prompt("input remote server user", hide_input=True)
        remote_password = typer.prompt("input remote server password", hide_input=True)
        remote_mapping = {
            '1': "CLOSE",
            '2': "OPEN"
        }
        print('select open ssh_tunnel:')
        for number in remote_mapping.keys():
            print(f'[{number}] -> {remote_mapping[number]}')
        ssh_tunnel = typer.prompt('Select apply ssh_tunnel ', type=click.Choice(remote_mapping.keys()),
                                  show_choices=False)
        ssh_tunnel_val = remote_mapping.get(ssh_tunnel, "OPEN")

        config.append_config_item({'db_host': _host})
        config.append_config_item({'ssh_tunnel': ssh_tunnel_val})
        config.append_config_item({'remote_host': _host})
        config.append_config_item({'remote_user': remote_user})
        config.append_config_item({'remote_password': remote_password})
    print(f"😇 Successfully applied new environment: {env_name},host:{_host}")


@app.command()
def getAccount():
    type = typer.prompt("select certi by type").upper()
    table = Table('TYPE', 'NAME', 'PASSWORD', 'REMARK')
    result = sqlite3_util.query(type)
    # result = __fetch(f"select * from certi where type = '{type}';", get_instance())
    for certi in result:
        table.add_row(certi[0], certi[1], jwt_utils.decode(certi[2]),certi[3])
    print(table)


@app.command()
def yunque(
        query: str = typer.Option(..., prompt=True),
        flag: str = typer.Option("N",
                                 help="'--flag=y' can write the answer to a local file .")
):
    maas = MaasService('maas-api.ml-platform-cn-beijing.volces.com', 'cn-beijing')
    skylark_key = config.read_config().get('skylarkKey', None)
    skylark_secret_key = config.read_config().get('skylarkSecretKey', None)
    maas.set_ak(skylark_key)
    maas.set_sk(skylark_secret_key)
    req = {
        "model": {
            "name": "skylark-chat",
        },
        "parameters": {
            "max_new_tokens": 1000,  # 输出文本的最大tokens限制
            "temperature": 0.7,  # 用于控制生成文本的随机性和创造性，Temperature值越大随机性越大，取值范围0~1
            "top_p": 0.9,  # 用于控制输出tokens的多样性，TopP值越大输出的tokens类型越丰富，取值范围0~1
            "top_k": 0,  # 选择预测值最大的k个token进行采样，取值范围0-1000，0表示不生效
        },
        "messages": [
            {
                "role": ChatRole.USER,
                "content": query
            },
        ]
    }
    resp = maas.chat(req)
    print(resp.choice.message.content)
    current_path = os.getcwd()
    if flag.upper() == 'Y':
        with open(f'{current_path}/{query}.txt', 'w') as f:
            # 将当前路径写入文本文件
            f.write(resp.choice.message.content)
        # 关闭文本文件
        f.close()
        print(f"{current_path} write end!")


@app.command()
def gemini(
        query: str = typer.Option(..., prompt=True),
        flag: str = typer.Option("N",
                                 help="'--flag=y' can write the answer to a local file .")
):
    gemini_key = config.read_config().get('geminiKey', None)
    resp = gemini_uitl.genai_no_stream(gemini_key, query)
    # 写入文本
    current_path = os.getcwd()

    if flag.upper() == 'Y':
        with open(f'{current_path}/{query}.txt', 'w') as f:
            # 将当前路径写入文本文件
            f.write(resp.text)
        # 关闭文本文件
        f.close()
        print(f"{current_path} write end!")

    print(resp.text)


def get_instance():
    db_instance_list: DBInstanceMapping = DBInstanceMapping()
    return db_instance_list.LOCAL if config.read_config().get("env") == 'LOCAL' else db_instance_list.REMOTE


@app.command()
def accounts():
    #result = __fetch(f"select type from certi", get_instance())
    result = sqlite3_util.fetch_all()
    table = Table('TYPE')
    for type in result:
        table.add_row(type[0])
    print(table)


@app.command()
def fanyi(
        query: str = typer.Option(..., prompt=True),

):
    result = fanyi_baidu_helper.translate(query)
    for re in result:
        print(re)


@app.command()
def decode(
        val: str = typer.Option(..., prompt=True),
):
    print(jwt_utils.decode(val))


@app.command()
def encode(
        val: str = typer.Option(..., prompt=True),
):
    print(jwt_utils.enconde(val))
