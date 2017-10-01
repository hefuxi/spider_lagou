#!usr/bin/python3
# coding=utf-8
import requests
from bs4 import BeautifulSoup
import json
import time
import lxml
import random
import jsonpath
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class lagou_spider(object):
    def __init__(self):
        self.keyword = raw_input("请输入你要查找的关键字: ")
        self.addr = raw_input("请输入你要查找的地点: ")
        self.endpage = int(raw_input("请输入你要爬取的页码: "))
        self.page = 1
        self.item_lists = []

        self.url = "https://www.lagou.com/jobs/positionAjax.json?"



    def sent_request(self):
        headers = {
            "Accept":"application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "Content-Length":"26",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie":"JSESSIONID=ABAAABAAAGFABEF2733F5B1C31E19F1F82118FE7B477977; SEARCH_ID=8c64767e5a6d4cc89c4707cb760151f3; user_trace_token=20170927145137-6e95d0f8-1f8f-411c-b297-1b7eaed408d5; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1506495098; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1506495098; _ga=GA1.2.2040870855.1506495098; LGSID=20170927145138-4f8681e6-a350-11e7-af1a-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; LGRID=20170927145138-4f868468-a350-11e7-af1a-525400f775ce; LGUID=20170927145138-4f868504-a350-11e7-af1a-525400f775ce; TG-TRACK-CODE=search_code",
            "Host":"www.lagou.com",
            "Origin":"https://www.lagou.com",
            "Referer":"https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "X-Anit-Forge-Code":"0",
            "X-Anit-Forge-Token":"None",
            "X-Requested-With":"XMLHttpRequest"
        }
        if self.page == 1:
            key = "ture"
        else:
            key = "false"

        print self.page
        data = {
            "first":key,
            "pn":self.page,
            "kd":self.keyword
        }
        parmas = {
            "px":"default",
            "city":self.addr,
            "needAddtionalResult":"false",
            "isSchoolJob":"0"
        }


        try:
            self.html = requests.post(self.url,params = parmas,data=data, headers = headers).json()


        except:
            print "^O^出错了"



    def start_work(self):
        while self.page <= self.endpage:
            self.sent_request()
            self.msg_load(self.html)
            self.page += 1

            time.sleep(1)

        self.write_msg(self.item_lists)


    def msg_load(self,html):
        print "正在爬取第%s页"%self.page
        try:
            print 123
            #这里不能用美丽汤,这里得到的是json数据而不是html,这里返回的是一个列表
            result_lists = jsonpath.jsonpath(html, "$..result")[0]
            for item in result_lists:
                item_list = {}
                item_list["companyFullName"] = item['companyFullName']
                item_list["positionName"] = item['positionName']
                item_list["salary"] = item['salary']
                item_list["workYear"] = item['workYear']
                item_list["education"] = item['education']
                item_list["positionAdvantage"] = item['positionAdvantage']
                item_list["district"] = item['district']
                item_list["createTime"] = item['createTime']
                self.item_lists.append(item_list)


        except:
            print "抱歉,数据读取出错"

    def write_msg(self,item_list):

        #这里没有禁用ASCii,asciide 禁用写在后面

        json.dump(item_list,open("lagou_info.json", "w"),ensure_ascii = False)

        '''
        等同于下面
        content = json.dumps(item_list,ensure_ascii = False)
        with open("lagou_info_.json", "w") as f:
            f.write(content.encode("utf-8"))
        '''

if __name__ == "__main__":
    lago_detail = lagou_spider()
    lago_detail.start_work()