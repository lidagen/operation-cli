
from . import jwt_utils
from . import cronParser

def decode(val:str):
    return jwt_utils.decode(val)


def encode(val:str):
    return jwt_utils.enconde(val)

def cron(cron_expression):
    try:
        
        parser = cronParser.CronParser(cron_expression)
        print("解析结果：")
        return parser
    except ValueError as e:
        print(f"错误: {e}")


