from flask import Flask,request,jsonify,Response
from flask_cors import CORS
from newsClassify import *
from dataTreating import *
from keyWordCloud import *


app = Flask(__name__)

CORS(app)

@app.route("/get_data", methods=['POST'])
def main():
    args = request.get_data()
    content = str(args,'utf-8')

    contents_clean, all_words, ten_top = get_parameter(content)
    url = word(all_words)

    label = bayes(contents_clean)

    # flask不能返回list
    dicts = {"label":label,"ten":ten_top,"url":url}


    return dicts

@app.route("/get_label",methods=['GET'])
def return_label():
    return jsonify(list(class_num().keys()))

if __name__ == '__main__':
    # 开启 debug模式，这样我们就不用每更改一次文件，就重新启动一次服务
    # 设置 host='0.0.0.0'，让操作系统监听所有公网 IP
    # 也就是把自己的电脑作为服务器，可以让别人访问
    app.run(debug=True, host='0.0.0.0',port='8585')
