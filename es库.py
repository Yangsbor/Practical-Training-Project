from elasticsearch import Elasticsearch
import time,datetime
import elasticsearch.helpers as helpers
es = Elasticsearch()


#清楚索引
es.indices.delete('phonenews')  # 删除索引
'''
mappings = {
            "mappings": {#type_doc_test为doc_type
                    "properties": {
                        "id": {
                            "type": "long",
                            "index": "false"
                        },
                        "serial": {
                            "type": "keyword",  # keyword不会进行分词,text会分词
                            "index": "false"  # 不建索引
                        },
                        "hasTag": {
                            "type": "long",
                            "index": True
                        },
                        "status": {
                            "type": "long",
                            "index": True
                        },
                        "createTime": {
                            "type": "date",
                            "format": "yyyy-MM-dd"
                        },
                        "updateTime": {
                            "type": "date",
                            "format": "yyyy-MM-dd"
                        }
                    }

            }
        }

res = es.indices.create(index = 'index_test',body =mappings)

#写入数据

action ={
              "id": "1111122222",
              "serial":"版本",
              "hasTag":"123",
              "status":"11",
              "createTime" :"2020-10-01",
              "updateTime":"2020-10-01",
                }

action1 ={
              "id": "11111222223",
              "serial":"版本",
              "hasTag":"123",
              "status":"11",
              "createTime" :"2020-10-01",
              "updateTime":"2020-10-01",
                }
es.index(index="index_test",body = action)

es.index(index="index_test",body = action1)
#即可写入一条数据

body = {
    "query":{
        "term":{
            "updateTime":"2020-10-01"
        }
    }
}
# 查询name="python"的所有数据
es.search(index="index_test",doc_type="_doc",body=body)
'''


#建立索引
mappings = {
            "mappings": {#type_doc_test为doc_type
                    "properties": {
                        "title": {
                            "type":"keyword",  # keyword不会进行分词,text会分词
                            "index":True,  # 不建索引
                            #"analyzer":"ik_max_word"
                        },
                        "class": {
                            "type":"keyword",
                            "index": True
                        },
                        "time":{
                            "type":"date",
                            "format":"yyyy-MM-dd"
                        },
                        "content": {
                            "type": "text",
                            "index": True,
                           # "analyzer":"ik_max_word"
                        }
                    }

            }
        }

es.indices.create(index = 'phonenews',body =mappings)

#插入数据
data=pd.read_csv("F:\桌面文件\实训数据\新闻情感模型数据.csv",encoding="gbk")
print(data)
title=data['标题']
classes=data['类别']
time=data['时间']
content=data['内容']

new_time=[]

for i in time:
    i='2020-'+i[-5:]
    print(i)
    new_time.append(i)
    print(type(i))

print(new_time)

for x in new_time:
    print(x)



for i in range(100):
    print(title[0])
    
print(len(data))

print(title[0])
for i in range(0,2684):
    print(i)
    action ={
              "title":title[i],
              "class":classes[i],
              "time":new_time[i],
              "content":content[i],
                }
    
    es.index(index='phonenews',id=i,body=action)
    
    
    
#查询数据:
body = {
    "query":{
        "term":{
            "class":"负面"
            }
    },
    "sort":{
        "time":{"order":"desc"}
            },
    "size":500
}
# 查询name="python"的所有数据
es.search(index="phonenews",doc_type="_doc",body=body)


scanResp = helpers.scan(es,query=body,scroll= "10m", index="phonenews", doc_type="_doc", timeout="10m")
   
for resp in scanResp:
   print(resp)
