import login
import shared
from getcourse import get_course_list
import getcontent
import download
#登录获取token
name=""
password=""
token=login.login(name,password)

#完善headers
headers=shared.headers
headers["token"]=token

#获取课表(课程对象的列表属性有id和name)
semester="" 
term=""
course_list= get_course_list(headers,semester,term)


#完善data
courseid=""
data=shared.data
data["courseid"]=courseid


#获取资料
content_lsit=getcontent.get_course_material(headers,data)


#进入子文件夹
dirid=""
data["dirid"]=dirid
content_list=getcontent.get_course_material(headers,data)


#下载资源
predownload_list=[]
path=""
download.sdownload(predownload_list,path)