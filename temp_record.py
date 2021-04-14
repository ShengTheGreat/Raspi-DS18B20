#!/usr/bin/python3
#第一行设置Linux下的解释器，在linux中不可缺少

#mysql数据库包，需安装
import pymysql
#时间处理包，python内置
import time
#使用通配符搜索文件包
from glob import glob

#连接到本地的mysql数据库
conn = pymysql.connect(database='temp',user='sheng',password='sheng')

#声明一个全局变量，用来保存上轮循环的温度信息
last = -100

#死循环
while(True):
    
  try:
    
    #查找所有的DS18B20传感器
    temp_sensors = glob("/sys/bus/w1/devices/28-*/temperature")
    
    #判断查找结果是否为空
    if(temp_sensors):
        
      #取查找结果的第一个，防止同时连接多个温度计时出现其它错误
      temp_sensor = temp_sensors[0] 
        
      #读取第一个DS18B20传感器的采集的温度信息
      f = open(temp_sensor,'r',encoding="ascii")
        
      #将文本信息转换为摄氏度的float值
      temp = eval(f.read())/1000
        
      #输出采集到的温度和当前时间的时间信息
      print(temp, time.strftime("%H:%M:%S", time.localtime()))
        
      #如果这次采集的温度与上轮循环不同，且温度变化幅度大于0.1摄氏度
      if last != temp and abs(last - temp) > 0.1:
            
        #记录最新的温度
        last = temp
        
        #将最新采集的温度保存到数据库中
        cur = conn.cursor()
        cur.execute('''insert into record(temp) values(%s)''',temp)
        conn.commit()
        
    else:
      #如果查找到的DS18B20传感器数码为0个，提示没有连接
      print("DS18B20 sensor not connected!")
      
      #等待0.5s以开始下一轮检测
      time.sleep(0.5)
    
  except Exception as e:
    
    #输出捕获的错误信息，并继续下一次的检测
    print(e)
    time.sleep(1)
    continue
