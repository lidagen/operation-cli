# This is a sample Python script.
import os

import click
import typer
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.vectorstores.chroma import Chroma
from openai import OpenAI
from rich import print, box
from .utils import config
from .utils.env_enums import Env
from rich.table import Table
from .utils.database_helper import DBInstanceMapping, __fetch
from .utils import jwt_utils

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
        config.append_config_item({'db_host': _host})
        config.append_config_item({'remote_host': _host})
        config.append_config_item({'remote_user': remote_user})
        config.append_config_item({'remote_password': remote_password})
    print(f"😇 Successfully applied new environment: {env_name},host:{_host}")


@app.command()
def get_account():
    type = typer.prompt("select certi by type").upper()
    table = Table('TYPE', 'NAME', 'PASSWORD')
    result = __fetch(f"select * from certi where type = '{type}';", get_instance())
    for certi in result:
        table.add_row(certi[1], certi[2], jwt_utils.decode(certi[3]))
    print(table)


@app.command()
def config_open_ai_key():
    open_ai_key = typer.prompt('Open AI Token [https://platform.openai.com/account/api-keys]')
    config.append_config_item({'open_ai_key': open_ai_key})
    print('😎 Welcome to the world of AI.')


@app.command()
def openai():
    word = typer.prompt("请输入需要查询的词汇")
    openai_api_key = config.read_config().get('open_ai_key', None)
    vectordb_path = os.path.join(os.path.dirname(__file__), '.', 'resources', 'chroma_db')
    assert openai_api_key, 'Please execute `opscli config-open-ai-key to finish configure.`'
    assert vectordb_path and os.path.exists(vectordb_path), 'Missing vector-db directory.'

    embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
    llm = OpenAI(temperature=0.9, openai_api_key=openai_api_key)
    vectordb = Chroma(persist_directory=vectordb_path, embedding_function=embedding)

    retriever = vectordb.as_retriever(search_kwargs={"k": 4}, search_type='mmr')
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    prompt_template = '''
        You are a business system dictionary query chatbot, please use the context information for word explanation, the 
        context is comma-separated text, the source format is CSV format, the column header of the table is (abbreviation, 
        Chinese name, type, related squad, description, remarks), please use the description column to explain as much as 
        possible. If you don't know the answer, say you don't know, don't try to make up the answer, please output the 
        answer in Chinese.

        {context}

        Question: {question}
        Helpful Answer:
        '''
    custom_prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    qa.combine_documents_chain.llm_chain.prompt = custom_prompt
    answer = qa.run(word)
    print(f'{answer}')


def get_instance():
    db_instance_list: DBInstanceMapping = DBInstanceMapping()

    return db_instance_list.LOCAL if config.read_config().get("env") == 'LOCAL' else db_instance_list.REMOTE


@app.command()
def account_type():
    result = __fetch(f"select type from certi", get_instance())
    print(result)
    table = Table('TYPE')
    for type in result:
        table.add_row(type[0])
    print(table)
