from flask import Flask,request
from elasticsearch import Elasticsearch
import json
from flask import render_template
from wtforms import Form, BooleanField, StringField, validators,SubmitField
from flask import request
from flask import Flask
from jinja2 import Markup
import jsonify
from flask import render_template
from pyecharts import options as opts
from pyecharts.charts import Line
from flask import jsonify ,Flask,request
from flask import render_template

#-------------------------------------------------------图表数据填充部分
data_iphone=pd.read_csv('F:\桌面文件\实训数据\百度搜索.csv',encoding='gbk')[216:252]
date=data_iphone['date']
index=data_iphone['index']
data_iphone_media=pd.read_csv('F:\桌面文件\实训数据\百度媒体.csv',encoding='gbk')
index_media=data_iphone_media[72:108]
print(index_media)
date=list(date)
index=list(index)
index_media=list(index_media['index'])
l=[]
for i in index:
    l.append(i)


l1=[]
for j in index_media:
    l1.append(j)
    
print(index_media)

#关于5g的数据
index_iphone_5g=pd.read_csv('F:\桌面文件\实训数据\百度搜索1.csv')[:38]
date_5g=index_iphone_5g['date']
index_5g=index_iphone_5g['index']
index_5g=list(index_5g)
date_5g=list(date_5g)


media_iphone_5g=pd.read_csv('F:\桌面文件\实训数据\百度媒体1.csv',encoding='gbk')[:38]
media_5g=media_iphone_5g['index']
media_5g=list(media_5g)
#-------------------------------------------------------图表数据填充部分
#----------------------------------------------------------------------------搜索部分
class highSearch(Form):
    defualtsearch=SubmitField('search');  
    

class elasticSearch():

    def __init__(self, index_type: str, index_name: str, ip="127.0.0.1"):

        # self.es = Elasticsearch([ip], http_auth=('elastic', 'password'), port=9200)
        self.es = Elasticsearch("localhost:9200")
        self.index_type = index_type
        self.index_name = index_name

    def search(self, query, count: int = 30):
        dsl = {
            "query": {
                "term": {
                        "class":query
                }
            },
            "from": 0,
            "size": 10,
            "sort": [],
            "aggs": {}
        }
        match_data = self.es.search(
            index=self.index_name, body=dsl, size=count)
        return match_data
#----------------------------------------------------------------------------搜索部分    
    
# 实例化，创建对象
app = Flask(__name__,template_folder="F:\桌面文件\moban",static_folder="F:\桌面文件\moban",static_url_path='/1')

app.secret_key='Yangsbor'



# 设置路由
@app.route('/main',methods=['GET','POST'])
# 定义视图函数
def main():
    form=highSearch()
    searchname=''
    address_list = []
    if request.method=='POST':
        searchname=request.form.get('search')
        print(type(searchname))
        es = elasticSearch(index_name='phonenews', index_type='_doc')
        data = es.search(searchname)
        print(data)
        address_data = data['hits']['hits']
        for item in address_data:
            address_list.append(item['_source'])
       # new_data = json.dumps(address_list)
        print(address_list)
        
        
    return render_template('dashboard.html',searchname=address_list[:10])

@app.route('/hotsearch', methods=["GET"])
def hotsearch():
     return render_template("table.html")
@app.route('/echarts', methods=["GET"]) #echarts 名字可以改为任意，但一定要与HTML文件中一至
def echarts():
    return jsonify(categories = date,data =l,date1=date,index1=index_media,date2=date_5g,index2=index_5g,date4=date_5g,index4=media_5g)


if __name__ == '__main__':
    app.config["JSON_AS_ASCII"] = False
    # app.run()中host设置主机，port设置端口，开启调试模式debug，可随程序代码更新得到最新的页面显示，省去了重新启动服务器程序调试的麻烦
    app.run()
