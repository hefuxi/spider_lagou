#!usr/bin/python3
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#处理json文件的模块
import json
#处理csv文件的模块
import csv
def main():
    #创建json文件对象
    json_file = file("lagou_info.json", "r")
    #json.load()读取json文件里的数据并返回python数据类型
    content_list = json.load(json_file)
    #创建csv文件对象
    csv_file = file("lagou_csv.csv","w")
    #创建csv文件读写对象
    csv_writer = csv.writer(csv_file)

    #keys()取出字典的所有的jian[],作为csv文件的表头
    head_list = content_list[0].keys()
    #values()取出字典所有的zhi
    data_list = [content.values() for content in content_list]
    # writerow() 写一行数据,给单层列表
    csv_writer.writerow(head_list)

    # writerows() 写多行数据,给多层嵌套列表
    csv_writer.writerows(data_list)


    csv_file.close()
    json_file.close()
if __name__ == "__main__":
    main()