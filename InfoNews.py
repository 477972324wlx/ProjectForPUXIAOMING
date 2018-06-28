# -*- coding=utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
import re
import csv
from bs4 import BeautifulSoup


first_use = 1
pattern = 'w+'
    
def getUrlInfo(url,writer):
    req = requests.get(url)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text,"html.parser")
    date = soup.find("span",{"class":"Article_PublishDate"})
    title = soup.find("span",{"class":"Article_Title"})
    VisitCnt = soup.find("span",{"class":"WP_VisitCount"})
    raw_data = [title.text,date.text,VisitCnt.text,url]
    writer.writerow(raw_data)
    
    
def getList_of_index(index):
    jwc_url = "http://www.jwc.ecnu.edu.cn"
    if(index == 0):
        url = 'http://www.jwc.ecnu.edu.cn/10611/list.htm' 
    else:
        url = 'http://www.jwc.ecnu.edu.cn/10611/list'+str(index)+'.htm' 
    print("正在抓取的网址：" + url)
    wd_data = requests.get(url)
    
    global first_use,pattern
    
    soup = BeautifulSoup(wd_data.text,"html.parser")
    Lists = soup.findAll("a",{"href":re.compile('^\/..\/..\/.*\/page.htm')})
    csvFile = open("InfoUrl.csv",pattern,newline='')
    writer  = csv.writer(csvFile)
    
    if(first_use == 1):
        writer.writerow(("title","date","VisitCount","url"))
        first_use = 0
        pattern = 'a+'
        
    for t_url in Lists:
        finalUrl = jwc_url+t_url["href"]
        getUrlInfo(finalUrl,writer)
 
#获取前两页即可
for i in range(1,3):
    getList_of_index(i)
