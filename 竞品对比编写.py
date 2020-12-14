import pandas as pd
from flask import request
from flask import Flask
from jinja2 import Markup
import jsonify
from flask import render_template
from pyecharts import options as opts
from pyecharts.charts import Line
from flask import jsonify ,Flask,request
from flask import render_template

data_iphone=pd.read_csv('F:\桌面文件\实训数据\百度搜索.csv',encoding='gbk')
date=list(data_iphone['date'][:36])
index=data_iphone['index']
iphone12_index_search=list(index[:36])
mate40_index_search=list(index[108:144])


data_iphone_media=pd.read_csv('F:\桌面文件\实训数据\百度媒体.csv',encoding='gbk')
index_media=data_iphone_media[72:108]
print(index_media)
date=list(date)
index=list(index)




l=[]
for i in index:
    l.append(i)



print(iphone12_index_search)


app = Flask(__name__,template_folder="F:\桌面文件\moban",static_folder="F:\桌面文件\moban",static_url_path='/1')
@app.route('/compare', methods=["GET"])
def compare():
     return render_template("typography.html")
@app.route('/compa', methods=["GET"]) #compa 名字可以改为任意，但一定要与HTML文件中一至
def compa():
    return jsonify(categories = date,data =iphone12_index_search,data2=mate40_index_search)

if __name__ == '__main__':
    app.run()
