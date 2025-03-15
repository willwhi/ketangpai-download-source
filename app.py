from flask import Flask, jsonify, request
from getcourse import get_course_list
import login  # 你的登录模块
import download  # 你的下载模块
from shared import headers, data
import getcontent
app = Flask(__name__)

token=""
course_dict={}
content_dict={}
content_list=[]

@app.route('/login',  methods=['POST'])
def login_usr():
    global token
    global headers
    name = request.json.get('username')
    password = request.json.get('password')
    token = login.logina(name, password)  # 登录并获取 token
    headers["token"]=token
    return jsonify({"status": "success"})


@app.route('/course_list',  methods=['POST'])
def course_list():
    global course_dict
    data = request.get_json() 
    semester = data.get('semester') 
    term = data.get('term') 
    # 这里应该添加实际的获取课程表逻辑
    course_list= get_course_list(headers,semester,term)
    for course in course_list:
        course_dict[course.get_id()]= course.get_name()
    course_dict=[course_dict]
    return jsonify(course_dict)


@app.route('/material_list',  methods=['POST'])
def material_list():
    global data
    #获取前端数据，区域和课程id
    contenttype = request.get_json("contenttype")
    courseid=request.get_json("courseid")
    #修改data
    data["courseid"]=courseid
    if(contenttype=="资料区"):
        data['contenttype']=["2","8"]
    elif(contenttype=="课件区"):
        data['contenttype']="1"
    # 这里应该添加实际的获取资料列表逻辑
    global content_list
    content_list=getcontent.get_course_material(headers,data)
    global content_dict
    for content in content_list:
        if(content.get_type()=="0"):#如果是文件夹，那么这个键的值是dirid
            content_dict[content.get_name()]=content.get_id()
        else:#如果不是文件，那么这个键的值是url
            content_dict[content.get_name()]=content.get_url()
    return jsonify(content_dict)


#获取子文件夹内容
@app.route('/dir_list',  methods=['POST'])
def dir_list():
    global data
    dirid=request.get_json("dirid")
    data["dirid"]=dirid
    # 这里应该添加实际的获取资料列表逻辑
    global content_list
    content_list=getcontent.get_course_material(headers,data)
    global content_dict
    for content in content_list:
        if(content.get_type()=="0"):#如果是文件夹，那么这个键的值是dirid
            content_dict[content.get_name()]=content.get_id()
        else:#如果不是文件，那么这个键的值是url
            content_dict[content.get_name()]=content.get_url()
    return jsonify(content_dict)



@app.route('/download',  methods=['POST'])
def download():
    content_name = request.get_json("dirname") 
    path=request.get_json("path")
    content_url=content_dict[content_name]
    # 这里应该添加实际的下载逻辑
    return jsonify({'status': 'downloading'})

if __name__ == '__main__':
    app.run(debug=True) 




    # content_list = request.json.get('content_list')                           
    # path = request.json.get('path')
    # download.sdownload(content_list, path)  # 下载操作
    # return jsonify({"status": "success", "message": "Download started"})