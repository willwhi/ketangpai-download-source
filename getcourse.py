import json
import requests
import time

class Course:
    def __init__(self,name,id):
        self.__name=name
        self.__id=id
    def get_name(self):
        return self.__name
    def get_id(self):
        return self.__id
def get_course_list(headers,semester,term):
    url = "https://openapiv5.ketangpai.com//CourseApi/semesterCourseList"
    data = {
        "isstudy": "1",
        "search": "",
        "semester": semester,
        "term": term,
        "reqtimestamp":int(time.time()*1000)
    }
    data = json.dumps(data, separators=(',', ':'))
    try:
        response = requests.post(url, headers=headers, data=data)
        print("获取课表成功")
        course_list=[Course(course["coursename"],course["id"]) for course in response.json()["data"][0]]
        return course_list
    except Exception as e:
        print("获取课表失败")
        print(e)
        return None