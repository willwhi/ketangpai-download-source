import time
import encrypt
import json
import requests


def login(name,password):
    reqtimestamp = int(time.time() * 1000)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "sec-ch-ua-mobile": "?0",   
    }
    url = "https://openapiv5.ketangpai.com//UserApi/login"
    password = encrypt.encrypt("ktp4567890123456", "ktp4567890123456", "pkcs7", password)
    data = {
        "email": name,
        "password": password,
        "remember": "0",
        "code": "",
        "mobile": "",
        "type": "login",
        "encryption": 1,
        "reqtimestamp": reqtimestamp
    }
    data = json.dumps(data, separators=(',', ':'))
    try:
        response = requests.post(url, headers=headers, data=data)
        print("登录成功")
        return response.json()["data"]["token"]
    except Exception as e:
        print("登录失败")
        print(e)
        return None
    