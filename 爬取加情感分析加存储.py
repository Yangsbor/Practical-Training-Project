import requests
from lxml import etree
import pandas as pd
import time
import datetime
import random
from elasticsearch import Elasticsearch


#加载停用词
stopwords=pd.read_csv('F:\桌面文件\实训数据\停用词文本.txt',index_col=False,quoting=3,sep="\t",names=['stopword'], encoding='gbk')
stopwords=stopwords['stopword'].values
es=Elasticsearch()  #建立es连接

#情感判断函数
class judgement():
    def __init__(self,str):
        self.string=str

    def build_vector(self,text,size,wv):
        #创建一个指定大小的数据空间
        vec = np.zeros(size).reshape((1,size))
        #count是统计有多少词向量
        count = 0
        #循环所有的词向量进行求和
        for w in text:
            try:
                vec +=  wv[w].reshape((1,size))
                count +=1
            except:
                continue
        #循环完成后求均值
        if count!=0:
            vec/=count
        return vec
    def get_predict_vecs(self,words):
        # 加载模型
        wv = Word2Vec.load("F:\桌面文件\实训数据/model3.pkl")
        #将新的词转换为向量
        train_vecs = self.build_vector(words,300,wv)
        return train_vecs
    def svm_predict(self,string):
        # 对语句进行分词
        words = jb.lcut_for_search(string)
        words = [v for v in words if not str(v).isdigit()]  #去数字
        words = list(filter(lambda x:x.strip(), words))     #去左右空格
        words = list(filter(lambda x:len(x)>1, words))      #长度为1的字符
        words = list(filter(lambda x:x not in stopwords,words)) #去掉停用词
        # 将分词结果转换为词向量
        word_vecs = self.get_predict_vecs(words)
        #加载模型
        cls = joblib.load("F:\桌面文件\实训数据/neutralnetworkmodel.pkl")
        #预测得到结果
        result = cls.predict(word_vecs)
        #输出结果
        if result  == '0':
            return '负面'
        elif result =='1':
            return '中立'
        else:
            return '正面'
    def main(self):
        s=self.svm_predict(self.string)
        return s


#爬虫——————————————————————————————————————————————————————
user_agent = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

content_list=[]#定义内容列表
title_list=[]#定义标题列表
link_list=[]#定义连接列表
time_list=[]
link_exist_list=[]  #已经存在过的链接
x=[]
for i in range(1,2):
    time.sleep(600)
    j=i*10
    url='https://www.baidu.com/s?ie=utf-8&medium=2&rtt=4&bsst=1&rsv_dl=news_b_pn&cl=2&wd=mate+40&tn=news&rsv_bp=1&rsv_sug3=4&rsv_sug1=4&rsv_sug7=100&oq=&rsv_sug2=0&rsv_btype=t&f=8&inputT=1067&rsv_sug4=1962&x_bfe_rqs=03E80&x_bfe_tjscore=0.000000&tngroupname=organic_news&newVideo=12&pn='+str(j)
    page_text = requests.get(url=url,headers={'User-Agent': random.choice(user_agent)}).content.decode()
    #数据解析
    tree = etree.HTML(page_text)
    link_li=tree.xpath('//h3[@class="news-title_1YtI1"]/a/@href')
    print(link_li)
    for j in link_li:
        if j not in link_exist_list:  #判断是否爬取过
            print(123)
            #print(j)
            url1=j
            page_text = requests.get(url=url1,headers={'User-Agent': random.choice(user_agent)}).content.decode()
            tree=etree.HTML(page_text)
            content_li=tree.xpath('//div[@class="article-content"]//span[@class="bjh-p"]//text()')
            title_li=tree.xpath('//div[@class="article-title"]/h2/text()')
            time_li=tree.xpath('//div[@class="article-source article-source-bjh"]/span[@class="date"]//text()')
            content_lis=''
            title_lis=''
            time_lis=''
            for subcontent in content_li:
               if subcontent.isspace() == False:
                   content_lis=content_lis+subcontent
            for subtitle in title_li:
                title_lis=title_lis+subtitle          
            for subtime in time_li:
                time_lis=time_lis+subtime
            
            classes=judgement(content_lis).main()   #进行情感判断
            x.append(classes)
            
            #插入es中
            es.index(index='phonenews',doc_type='news',body={'title':title_lis,'class':classes,'time':time_lis,'content':content_lis})
            #----------------------------------------------------------------------------
            content_list.append(content_lis)     #存为列表
            title_list.append(title_lis)
            time_list.append(time_lis)
            link_exist_list.append(j)    #存进列表中
        else:
            continue
    
    print('第'+str(i)+'页爬取完成')
    
print(len(content_list))
print(len(link_li))
print(len(title_list))
print(len(time_list))

l=pd.DataFrame({'标题':title_list,'时间':time_list,'内容':content_list})
#l.to_csv('F:\桌面文件\实训资料\手机新闻爬取2.csv',mode='a',header=False,index=False,encoding='gbk')


print(title_list)
print(time_list)
print(x)




