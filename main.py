import login
import shared
from getcourse import get_course_list
import getcontent
import download
#登录获取token
# name="17667352592"
# password="040814Xu"
# token=login.login(name,password)

# print(token)


# #完善headers
headers=shared.headers
headers["token"]='f896c3473a0bc6c5ba7f5ca3a5120be64f47bad56444aab0e35d26a844a05962'

#获取课表(课程对象的列表属性有id和name)
# semester="2022-2023" 
# term="1"
# course_list= get_course_list(headers,semester,term)


# for course in course_list:
#     print(course.get_id(),course.get_name())

#完善data
courseid="MDAwMDAwMDAwMLOGvdyGz7tohdtyoQ"
data=shared.data
data["courseid"]=courseid

data['contenttype']=["2","8"]
#获取资料
# content_list=getcontent.get_course_material(headers,data)
# for content in content_list:
#     print(content.get_name(),content.get_id(),content.get_url(),content.get_type())


#进入子文件夹
dirid="MDAwMDAwMDAwMLOGtZeIqbNqhc6OoQ"
data["dirid"]=dirid
content_list=getcontent.get_course_material(headers,data)
for content in content_list:
    print(content.get_name(),content.get_id(),content.get_url(),content.get_type())

#下载资源
predownload_list=content_list
path="/home/wilwhi"
download.sdownload(predownload_list,path)