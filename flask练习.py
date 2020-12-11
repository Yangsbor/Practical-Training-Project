from flask import Flask,request
from elasticsearch import Elasticsearch
import json
from flask import render_template
from wtforms import Form, BooleanField, StringField, validators,SubmitField

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
    
    
# 实例化，创建对象
app = Flask(__name__,template_folder="F:\桌面文件\moban",static_folder="F:\桌面文件\moban",static_url_path='/1')

app.secret_key='Yangsbor'


# 设置路由
@app.route('/',methods=['GET','POST'])
# 定义视图函数
def index():
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


if __name__ == '__main__':
    app.config["JSON_AS_ASCII"] = False
    # app.run()中host设置主机，port设置端口，开启调试模式debug，可随程序代码更新得到最新的页面显示，省去了重新启动服务器程序调试的麻烦
    app.run()

    # 当然也可以直接使用默认参数
    # app.run()