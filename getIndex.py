# coding = utf-8

import requests
from bs4 import BeautifulSoup
import csv
import time
import random

def getIndexHtml(req):
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

#这个显示的是最近七天的信息
def showDetail(url):
    # 不过就算你这么说也没有什么用啊，毕竟你每天刷新的话，新增的数据只有一个啊
    if (url == ""):
        return
    textName = url.split("com/")
    textName = textName[1].split(".")
    textName = textName[0] + ".csv"

    req = requests.get(url)
    req.encoding = 'gbk'
    try:
        soup = BeautifulSoup(req.text, "html.parser")
        div = soup.find(id="Div2")
        poptableWrap = div.find(class_="poptableWrap")
        trs = poptableWrap.find_all("tr")
        for tr in trs:
            index = 0
            tds = tr.find_all("td")
            while index < len(tds):
                try:
                    wFile = open(textName, "a")
                    writer = csv.writer(wFile)
                    writer.writerow([tds[0].text, tds[1].text, tds[2].text, tds[3].text])
                    print(textName + "写入文件成功")
                except:
                    print("写入文件过程中出现异常")
                finally:
                    wFile.close()
                index += 4
    except:
        print("网络连接出错")


if __name__ == '__main__':
    # 写入文件
    url = "http://fund.eastmoney.com/allfund.html"
    headers = {"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) App leWebKit/537.51.2 (KHTML, like Gecko)"
                            " Version/7.0 Mobile/11D257 Safari/9537.53"}

    req = requests.get(url, headers = headers)
    req.encoding = 'gbk'
    getIndexHtml(req)

    # 读取文件
    str = readFromCsv()
    num = 20
    for i, j in enumerate(str):
        if i % 2 == 0 and i < num:
            time.sleep(random.randint(3, 5))
            showDetail(str[i + 1])


