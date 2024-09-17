
# 规范名称：
# content:资料名称，即要下载的资料（最小单位）
# material:资料（指课堂派的资料目录）
# course:课程
# semester:学年
# term:学期

import json
import time
import requests
from tqdm import tqdm
   
#登录
def login(name,password):
    reqtimestamp = int(time.time() * 1000)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "sec-ch-ua-mobile": "?0",   
    }
    url = "https://openapiv5.ketangpai.com//UserApi/login"
    data = {
        "email": name,
        "password": password,
        "remember": "0",
        "code": "",
        "mobile": "",
        "type": "login",
        "encryption": 0,
        "reqtimestamp": reqtimestamp
    }
    data = json.dumps(data, separators=(',', ':'))
    try:
        response = requests.post(url, headers=headers, data=data)
        print("登录成功")
        token= response.json()["data"]["token"]
        return response
    except Exception as e:
        print("登录失败")
        print(e)
        return None
#  获取课表  
def get_semester_list(headers,semester,term):
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
        return response
    # print(response.text)
    # with open("F:\project\python\spider\example\ketangpai\\test.txt","w")as f:
    #     f.write(response.text)
    except Exception as e:
        print("获取课表失败")
        print(e)
        return None

# 进入课堂
def get_course(semester_response,course_need):
    for course in semester_response.json()["data"]:
        if(course["coursename"]==course_need):
            return course


# 进入资料区(content_type=['2','8'])
def get_course_material(headers,courseid):
   
    url = "https://openapiv5.ketangpai.com//FutureV2/CourseMeans/getCourseContent"
    data = {
        "courseid": courseid,
        "contenttype": [
            "2",
            "8"
        ],
        "dirid": 0,
        "lessonlink": [],
        "sort": [],
        "page": 1,
        "limit": 50,
        "desc": 3,
        "courserole": 0,
        "vtr_type": "",
        "reqtimestamp":int(time.time()*1000)
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, data=data)
    try:
        print('获取资料区成功')
        return response
    except Exception as e:
        print("获取课程资料失败")
        print(e)
        return None


# 进入资料区子文件夹
def get_dir_content(headers,courseid,dirid):
    
    url = "https://openapiv5.ketangpai.com//FutureV2/CourseMeans/getCourseContent"
    data = {
        "courseid": courseid,
        "contenttype": [
            "2",
            "8"
        ],
        "dirid": dirid,
        "lessonlink": [],
        "sort": [],
        "page": 1,
        "limit": 50,
        "desc": 3,
        "courserole": 0,
        "vtr_type": "",
        "reqtimestamp": int(time.time() * 1000)
    }
    data = json.dumps(data, separators=(',', ':'))
    try:
        response = requests.post(url, headers=headers, data=data)
        print('进入子文件夹成功')
        return response
    except Exception as e:
        print("进入子文件夹失败")
        print(e)
        return None


#获取下载链接
def get_download_link(content_num,content_list):
    url_list=[]
    for num in content_num:
        url_list.append(content_list[int(num)-1]['attachment'][0]['url'])
    return url_list
# 进行下载
def download_material(url,material_name):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69",
        }
        # 采用流式下载，显示实时进度条
        response = requests.get(url,stream=True)
        total_size=int(response.headers.get('Content-Length',0))
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
        with open( f".\{material_name}", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk: 
                    f.write(chunk)
                    progress_bar.update(len(chunk))
        progress_bar.close()
        print("下载成功")
    except Exception as e:
        print("下载失败")
        print(e)
        return None

# 打印课表
def print_semester_list(semester_response):
    i=1
    course_list=semester_response.json()["data"]
    for course in course_list:
        print(f"{i}. "+course['coursename'])
        i+=1
    return course_list
    
#打印资料列表
def print_material_list(material_response):
    material_list=material_response.json()["data"]["list"]
    i=1
    material_list = [material for material in material_list if material['item_type'] != '3'] # 过滤掉item_type为3的元素,不能在循环中删除，会破坏索引
    for material in material_list:
        try:
            print(f"{i}."+material['title'])
            i+=1
        except Exception as e:
            continue
    return material_list

# 打印子文件夹信息
def print_dir_list(dir_response):
    dir_list=dir_response.json()["data"]["list"]
    i=1
    for dir in dir_list:
        try:
            print(f"{i}."+dir['name'])
            i+=1
        except Exception as e:
            continue
    return dir_list


def main():
    name=input('请输入用户名(账号)')
    password=input('请输入密码')
   
    
    login_response=login(name,password)
    token=login_response.json()["data"]["token"]
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://www.ketangpai.com",
        "Referer": "https://www.ketangpai.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "token": token
    }
    while(True):
        semster=input('请输入学年（如2023-2024）')
        term=input('请输入学期（填1或2）')
        #请求课表
        semester_response=get_semester_list(headers,semester=semster,term=term)

        # 打印课表
        course_list=print_semester_list(semester_response)

        #选择课程
        coursenum=int(input('请输入课程序号（课程名字前面的序号）'))
        #获取课程名字
        course_need=course_list[coursenum-1]["coursename"]

        #进入课堂
        course=get_course(semester_response,course_need)
    
        courseid=course["id"]
        #进入资料区
        material=get_course_material(headers,courseid)


        # 是否有子文件夹
        sub=input('资料是否在子文件夹中（填1或0）,1表示在，0表示不在')
        if(sub=='1'):
            #打印子文件夹信息
            dir_list=print_dir_list(material)
            dirnum=int(input('请输入子文件夹序号（子文件夹名字前面的序号）'))
            # 获取dirid
            dirid=dir_list[dirnum-1]["id"]
            #进入资料区子文件夹       
            dir_content=get_dir_content(headers,courseid,dirid)
            #打印资料列表
            content_list=print_material_list(dir_content)
            # 输入下载资料的序号
            content_num=input('请输入下载资料的序号(资料名字前面的序号),输入多个序号时用一个空格隔开')
            content_num=content_num.split(sep=' ')
            #获取资料链接
            url_list=get_download_link(content_num,content_list)   
        else:
            #打印资料列表
            content_list=print_material_list(material)
            # 输入下载资料的序号
            content_num=input('请输入下载资料的序号(资料名字前面的序号),输入多个序号时用一个空格隔开')
            content_num=content_num.split(sep=' ')
            #获取资料链接
            url_list=get_download_link(content_num,content_list)
        #下载资料
        num=0
        for url in url_list:
            print(f'开始下载第{num+1}个资料')
            content_name=content_list[num-1]["title"]
            download_material(url,content_name)
            num+=1
        print('如果退出，请输入q,否则输入任意键继续下载')
        if(input()=='q'):
            break
        else:
            continue

if __name__ == '__main__':
    main()