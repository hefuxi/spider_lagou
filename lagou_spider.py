#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import jsonpath
import json
import time
import random

class LagouSpider(object):
    def __init__(self):
        self.base_url = "https://www.lagou.com/jobs/positionAjax.json?"

        #headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.headers = {
            #"Referer" : "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
            # 反爬点1：检查Referer是否是正常合理的Referer
            "Referer" : "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
            # 反爬点2：检查User-Agent
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        }
        self.position_name = raw_input("请输入需要查询的职位:")
        self.city_name = raw_input("请输入需要查询的城市:")
        self.end_page = int(raw_input("请输入爬取的页数:"))
        #self.proxy_list = [xxxx, xxx, xxx]
        self.item_list = []
        self.page = 1


    def load_page(self):
        params = {
            "px" : "default",
            "city" : self.city_name,
            "needAddtionalResult" : "false",
            "isSchoolJob" : "0"
        }

        data = {
            "first":"false",
            "pn":self.page,
            "kd":self.position_name
        }

        # 每次发送请求，随机获取一个代理
        #proxy = random.choice(self.proxy_list)
        # 如果这个请求将返回一个json，json() 之间返回json转换后的Python数据类型
        #json_obj = requests.post(self.base_url, params = params, data = data, headers = self.headers, proxies = proxy).json()
        try:
            json_obj = requests.post(self.base_url, params = params, data = data, headers = self.headers).json()
            print "[INFO]: 正在爬取第%d页..." % self.page
        except:
            print "[INFO] %d 爬取失败..." % self.page

        # jsonpath返回列表，result本身就是列表，那么返回嵌套列表，所以先取下标里的列表
        try:
            result_list = jsonpath.jsonpath(json_obj, "$..result")[0]
                #print result_list
            for result in result_list:
                item = {}
                item["companyFullName"] = result["companyFullName"]
                item["positionName"] = result["positionName"]
                item["salary"] = result["salary"]
                item["city"] = result["city"]
                item["district"] = result["district"]
                item["createTime"] = result["createTime"]
                self.item_list.append(item)
        except:
            print "[INFO] %d 数据提取失败.." % self.page

        #print json_obj['content']

    def start_work(self):
        while self.page <= self.end_page:
            self.load_page()
            time.sleep(0)
            self.page += 1

        json.dump(self.item_list, open("lagou_info.json", "w"))


if __name__ == "__main__":
    spider = LagouSpider()
    spider.start_work()



