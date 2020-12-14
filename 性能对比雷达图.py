from pyecharts import Radar

value_mate40=[[8.7,6.76, 8, 4400, 212, 7299]]
value_iphone=[[8.6,6.7,6,3687, 226, 9299]]

indicator=[{"name":"点评","max":10,"min":0 },
           {"name":"尺寸","max":8,"min":0  },
           {"name":"RAM（GB)","max": 8,"min":0  },
           {"name":"电池容量（mAh)","max": 5000,"min":0  },
           {"name":"重量（g)","max": 5000,"min":0  },
           {"name":"价格","max": 20000,"min":0  }]
           
radar = Radar()

radar.config(c_schema=indicator)
radar.add("HuaWei mate 40 pro",value_mate40,item_color="#f9713c", 
          symbol=None,area_color="#ea3a2e", area_opacity=0.3,
          legend_top='bottom',line_width=3)

radar.add("Apple iphone 12 pro",value_iphone,item_color='#2525f5', 
          symbol=None,area_color='#2525f5',area_opacity=0.3,
          legend_top='bottom',legend_text_size=20,line_width=3)

radar.render("F:\桌面文件\实训数据\Rader.html")