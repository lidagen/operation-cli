from enum import Enum


class Type(Enum):
    ENCODE = 'encode'
    DECODE = 'decode'
    CRON = "cron"
