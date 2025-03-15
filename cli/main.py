# This is a sample Python script.
import click
import typer
from rich import print
from rich.table import Table
import threading

from .utils import config
from .utils import fanyi_baidu_helper
from .utils import jwt_utils
from .utils import sqlite3_util
from .utils.ai_enums import Ai
from .utils.database_helper import DBInstanceMapping
from .utils.env_enums import Env
from .utils import gemini_uitl
from .utils import deepseek
from .utils import qWen
from .utils import pushplus
from .utils import cronUtil


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
app = typer.Typer(rich_markup_mode="rich")


@app.callback()
def callback(ctx: typer.Context):
    """
    config is not null
    """
    if ctx.invoked_subcommand != 'configure' and config.is_valid() is False:
        print('Please run `cli configure` to configure the essential information.')
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
def ai():
    env_mapping = {
        '1': Ai.DEEP_SEEK,
        '2': Ai.GEMINI,
        '3': Ai.QIAN_WEN
    }
    for number in env_mapping.keys():
        print(f'[{number}] -> {env_mapping[number].value}')
    ai_index = typer.prompt('Select ai', type=click.Choice(env_mapping.keys()), show_choices=False)
    ai_enum = env_mapping.get(ai_index, Ai.DEEP_SEEK)
    query = typer.prompt("input query")
    resp = ""
    if ai_enum == Ai.DEEP_SEEK:
        deepseek_key = config.read_config().get('deepseekKey', None)
        resp = deepseek.genai_no_stream(deepseek_key, query)
        print(resp)
    elif ai_enum == Ai.GEMINI:
        gemini_key = config.read_config().get('geminiKey', None)
        resp = gemini_uitl.genai_no_stream(gemini_key, query)
        print(resp.text)
    elif ai_enum == Ai.QIAN_WEN:
        qWen_key = config.read_config().get('qWenKey', None)
        resp = qWen.genai_no_stream(qWen_key, query)
        print(resp)



@app.command()
def push(
     title: str = typer.Option(..., prompt=True),
     content: str = typer.Option(..., prompt=True)):
  
  token = config.read_config().get('pushPlus', None)
  pushplus.push_plus_notify(token,title,content)
  result = pushplus.push_plus_notify(token,title,content)
  print(result)


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
def getAcc():
        
    table = Table('TYPE', 'NAME', 'PASSWORD', 'REMARK')
    result = sqlite3_util.query(type)
    # result = __fetch(f"select * from certi where type = '{type}';", get_instance())
    for certi in result:
        table.add_row(certi[0], certi[1], jwt_utils.decode(certi[2]), certi[3])
    print(table)


def get_instance():
    db_instance_list: DBInstanceMapping = DBInstanceMapping()
    return db_instance_list.LOCAL if config.read_config().get("env") == 'LOCAL' else db_instance_list.REMOTE


@app.command()
def accounts():
    # result = __fetch(f"select type from certi", get_instance())
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
