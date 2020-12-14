# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 15:04:20 2020

@author: dell
"""
from pyecharts import options as opts
from pyecharts.charts import Pie
from snapshot_selenium import snapshot as driver
from pyecharts.render import make_snapshot
import pandas as pd 

df=pd.read_csv('手机数据.csv')
x=df['手机'][:10]
y=[170,150,130,110,90,70,50,30,10]
m=[list(z) for z in zip(x,y)]
print(m)


pic1 = (
    Pie(init_opts=opts.InitOpts(width="1000px", height="1200px"))
    .add(
         "",[list(z) for z in zip(x,y)],
        
        radius=['13%','90%'],
        center=["70%", "60%"],
        rosetype="radius",
        is_clockwise=False,
        label_opts=opts.LabelOpts(is_show=False),
     )
    .set_global_opts(title_opts=opts.TitleOpts(title="热门手机排名",
                                              pos_left="center",pos_top="15%",
                                              title_textstyle_opts=opts.TextStyleOpts(font_size=30)),
                                   legend_opts=opts.LegendOpts(orient="vertical", pos_top="20%", pos_left="90%")
                    )
    )
    
pic2 = (
    Pie(init_opts=opts.InitOpts(width="1000px", height="1200px"))
    .add(
         "",[list(z) for z in zip(df['手机'][10:20],y)],
        
        radius=['13%','90%'],
        center=["70%", "60%"],
        rosetype="radius",
        is_clockwise=False,
        label_opts=opts.LabelOpts(is_show=False),
     )
    .set_global_opts(title_opts=opts.TitleOpts(title="手机品牌排名",
                                              pos_left="60%",pos_top="15%",
                                              title_textstyle_opts=opts.TextStyleOpts(font_size=30)),
                                   legend_opts=opts.LegendOpts(orient="vertical", pos_top="20%", pos_left="90%")
                    )
    )
    
pic3 = (
    Pie(init_opts=opts.InitOpts(width="1000px", height="1200px"))
    .add(
         "",[list(z) for z in zip(df['手机'][80:90],y)],
        
        radius=['13%','90%'],
        center=["70%", "60%"],
        rosetype="radius",
        is_clockwise=False,
        label_opts=opts.LabelOpts(is_show=False),
     )
    .set_global_opts(title_opts=opts.TitleOpts(title="5G手机品牌排名",
                                              pos_left="60%",pos_top="15%",
                                              title_textstyle_opts=opts.TextStyleOpts(font_size=30)),
                                   legend_opts=opts.LegendOpts(orient="vertical", pos_top="20%", pos_left="90%")
                    )
    )


pic1.render(path='热门手机排名.html')
pic2.render(path='手机品牌排名.html')
pic3.render(path='5G手机排名.html')