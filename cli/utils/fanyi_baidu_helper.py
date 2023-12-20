# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
import json
from hashlib import md5

# Set your own appid/appkey.
appid = '20231130001896362'
appkey = 'N9ekUoNYXCzh_NLB81ar'

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`


endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path
salt = random.randint(32768, 65536)

# Build request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

import re


def has_chinese_character(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    result = pattern.search(text)
    if result:
        return True
    else:
        return False


def has_english_character(text):
    pattern = re.compile(r'[a-zA-Z]')
    result = pattern.search(text)
    if result:
        return True
    else:
        return False


# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def translate(query: str):
    flag = has_chinese_character(query)

    from_lang = 'zh' if flag else "en"
    to_lang = 'en' if flag else "zh"

    sign = make_md5(appid + query + str(salt) + appkey)

    # Send request
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    # Show response
    return result['trans_result']
