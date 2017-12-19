# coding = utf-8

import requests
from bs4 import BeautifulSoup
import csv

def getIndexHtml():
    # 打开csv
    csvFile = open("instance.csv", "w")
    try:
        writer = csv.writer(csvFile)

        soup = BeautifulSoup(req.text, "html.parser")
        boxs = soup.find_all(class_="num_box")
        for str in boxs:
            uls = str.find(class_="num_right")
            lis = uls.find_all("li")
            for li in lis:
                hrefs = li.find_all("a")
                if len(hrefs) == 3:
                    writer.writerow([hrefs[0].text, hrefs[0]['href']])
                    print(hrefs[0].text + " " + hrefs[0]['href'] + "写入文件成功")
    except :
        print("将数据写入文件出错")
    finally:
        # 关闭文件
        csvFile.close()

def readFromCsv():
    ret = []
    try:
        csvFile = open("instance.csv", "r")
        try:
            infos = csv.reader(csvFile)
            for info in infos:
                if info:
                    ret += [info[0]] + [info[1]]
        except:
            print("读取数据出错")
        finally:
            csvFile.close()
            return ret
    except:
        print("找不到文件")
    return ""


if __name__ == '__main__':
    # 写入文件
    url = "http://fund.eastmoney.com/allfund.html"
    req = requests.get(url)
    req.encoding = 'gbk'
    getIndexHtml()

    # 读取文件
    str = readFromCsv()
    for i, j in enumerate(str):
        if i % 2 == 0:
            print(str[i], str[i + 1])

    # i = 0
    # while i < len(str):
    #     print(str[i], str[i])
    #     i += 2
