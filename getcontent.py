
# 规范名称：
# content:资料名称，即要下载的资料（最小单位）
# material:资料（指课堂派的资料目录）
# course:课程
# semester:学年
# term:学期

import json
import time
import requests
class Content:
    def __init__(self,type,id):
        self.__type = type
        self.__id = id
    def set_url(self,url):
        self.__url = url
    def set_type(self,type):
        self.__type=type
    def set_name(self,name):
        self.__name=name
    def get_url(self):
        return self.__url
    def get_name(self):
        return self.__name
    def get_id(self):
        return self.__id
    def get_type(self):
        return self.__type


def get_content_list(response:requests.response):
    content_list=[]
    try:
        for content_raw in response.json()["data"]["list"]:
            content=Content(content_raw["contenttype"],content_raw["id"])
            if(content_raw["contenttype"]=="0"):
                content.set_name(content_raw["name"])
            else:
                content.set_name(content_raw["title"])
                content.set_url(content_raw["attachment"][0]["url"]) 
            content_list.append(content)
        return content_list
    except:
        print("没有资料！")


url = "https://openapiv5.ketangpai.com//FutureV2/CourseMeans/getCourseContent"

# 获取资料区或者课件区资料列表或者子文件夹（增加dirid）
def get_course_material(headers,data):
    data["reqtimestamp"]=int(time.time()*1000)
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, data=data)
    content_list=get_content_list(response)
    try:
        print('获取课程资料成功')
        return content_list
    except Exception as e:
        print("获取课程资料失败")
        print(e)
        return None


