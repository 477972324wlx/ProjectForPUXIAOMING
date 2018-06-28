# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 23:17:54 2018

@author: 47797
"""

from PIL import Image
from selenium import webdriver

import matplotlib.pyplot as plt  
import os
import csv
import sys
import time

first_use = 1
pattern   = 'w+'

def set_ch():    
    from pylab import mpl    
    mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体    
    mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题    

#绘制图表    
def getChart():
    set_ch() 
    name = []
    gpa = []
    plt.figure(figsize=(90,50)) #图片大小
    plt.xticks(fontsize=60)     #图片字体大小
    plt.yticks(fontsize=90)
    
    with open ('gpa.csv') as file:
        reader = csv.reader(file)
        cnt = 0
    
        for row in reader:
            if(cnt > 0):
                name.append(row[1])
                gpa.append(float(row[4]))
            cnt = 1
    plt.bar(range(len(gpa)),gpa,color='gbry',tick_label=name)
    plt.savefig("gpaChart.png")
  
   
    
#通过网页截屏，捕获验证码的图片，机子不一样可能需要调整参数
def getImage():
    img = Image.open("g.gif")
    imsz = img.size
    len_w = imsz[0]
    len_h = imsz[1]
    x = len_w - len_w/6 -160
    y= len_h/3+10
    w = len_w/8-130
    h = 70
    region = img.crop((x, y, x+w, y+h))
    region.save("code.gif")
    

#获取验证码    
def getCaptcha():
    getImage()
    image_file = Image.open("code.gif")
    image_file = image_file.convert('1') 
    image_file.save("result.gif")
    os.system("tesseract result.gif out")
    file = open("out.txt","r")
    captcha = file.read()
    captcha = captcha.replace(" ","")
    captcha = captcha.strip("\n")
    return captcha

#登录过程
def Login(driver):

    para = sys.argv #通过Csharp传来的命令行参数进行确定账号密码
 
    idNum = para[1]
    passWord = para[2];
    
    code = getCaptcha()
    driver.find_element_by_id("un").clear();
    driver.find_element_by_id("un").send_keys(idNum)
    
    driver.find_element_by_id("pd").clear();
    driver.find_element_by_id("pd").send_keys(passWord)
    
    driver.find_element_by_name("code").clear();
    driver.find_element_by_name("code").send_keys(code)
    
    driver.find_element_by_id("index_login_btn").click()
    
#获得课程表
def getSchedule(driver):
    driver.get("http://applicationnewjw.ecnu.edu.cn/eams/courseTableForStd.action")
    driver.get_screenshot_as_file("raw.png")
    im = Image.open("raw.png")
    im_sz = im.size

    region = im.crop((0,0,im_sz[0],im_sz[1] - im_sz[1]/3))
    region.save("timetable.gif")

#获得学分表
def getGPA(driver):
    driver.get("http://applicationnewjw.ecnu.edu.cn/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR")
    tblist = driver.find_element_by_css_selector("[id$=_data]")
    lists = tblist.find_elements_by_tag_name('td')
    csvFile = open("gpa.csv","w",newline='')
    writer  = csv.writer(csvFile)
    writer.writerow(("semester","name","class","credit","gpa"))
    cnt = 0
    row_data = []
    for content in lists:
        cnt = cnt + 1
        if((cnt <= 5 and cnt != 2) or cnt == 10):
            row_data.append(content.text)
        if(cnt == 10):
             writer.writerow(row_data)
             row_data = []
             cnt = 0  
    csvFile.close()


driver = webdriver.Chrome()
driver.get('http://idc.ecnu.edu.cn')
driver.maximize_window()
driver.get_screenshot_as_file("g.gif")
Login(driver)
getSchedule(driver)
getGPA(driver)
driver.quit()
getChart()
