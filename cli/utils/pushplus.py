import requests

def push_plus_notify(token:str,title:str,content:str):
    url = "http://www.pushplus.plus/send"
    payload = {
        "token": token,
        "title": title,
        "content": content,
        "template": "txt"  # 默认文本格式，可选 html/markdown
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        if result.get("code") == 200:
            return "success"
        else:
            return(f"❌ 推送失败: {result.get('msg')}")
    except requests.exceptions.RequestException as e:
        return(f"⚠️ 网络请求失败: {str(e)}")