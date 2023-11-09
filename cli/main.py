# This is a sample Python script.
import click
import typer
from rich import print, box
from .utils import config
from .utils.env_enums import Env
from rich.table import Table
from .utils.database_helper import DBInstance, DBInstanceMapping, __fetch

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
app = typer.Typer(rich_markup_mode="rich")

db_instance_list: DBInstanceMapping = DBInstanceMapping()


@app.callback()
def callback(ctx: typer.Context):
    """
    Awesome Portal Gun
    """
    if ctx.invoked_subcommand != 'configure' and config.is_valid() is False:
        print('Please run `opscli configure` to configure the essential information.')
        raise typer.Exit()


@app.command()
def configure(
        db_username: str = typer.Option(..., prompt=True),
        db_password: str = typer.Option(..., prompt=True, hide_input=True, confirmation_prompt=True),

):
    config_content = {
        "db_username": db_username,
        "db_password": db_password,
        "env": "LOCAL",
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
    if env_name == Env.REMOTE.value:
        remote_host = typer.prompt("input remote host", default='127.0.0.1', hide_input=True)
        config.append_config_item({'db_host': remote_host})
        print(f"😇 Successfully applied new environment: {env_name},host:{remote_host}")


@app.command()
def get_account():
    type = typer.prompt("select certi by type")
    env = config.read_config().get("env")
    if 'LOCAL' == env:
        instance = db_instance_list.LOCAL
    else:
        instance = db_instance_list.REMOTE

    __fetch(f"select * from certi where type = '{type}';", instance)
