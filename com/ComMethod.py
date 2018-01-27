import re
from urllib import request
import chardet
import threading
import os
import pymysql
import time
import random
import codecs

BASE_FILEPATH = "/Users/yuanwei/Downloads/pythonPro/stocksys/20180127/"

def getBaseFilePath():
    global BASE_FILEPATH
    return BASE_FILEPATH

def WriteFile(fname,data):
#    f = open(fname, 'a')
    f = codecs.open(fname, 'a', 'utf-8')
    if f:
        f.write(data)
        f.close()
    else:
        return False

def ReadFile(fname):
    try:
        f = open(fname, 'r')
        if f:
            return f.read()
        else:
            return False
    except IOError as err:
        print(str(err))
        return False

def GetAllStockCodes():
    conn = pymysql.connect(host='localhost',port='',user='root',passwd='adency',db='stockdb',charset='utf8')
    cur = conn.cursor()
    lStockCode = []
    SQL = "SELECT stocknum from" \
          " stocklist"
    cur.execute(SQL)
    rows = cur.fetchall()
    for row in rows:
        lStockCode.append(row[0])
    cur.close()
    conn.close()
    return lStockCode

#get web all data
def getHtml(url, proxy = None):
    error = 0
    cnt = 1
    print("proxy: %s" % proxy)
    headers = {
        'User-Agent':r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    while error == 0 and cnt < 4:
        error = 1
        try:
            if proxy == None:
                req = request.Request(url, headers=headers)
                html = request.urlopen(req, timeout=2000).read()
            else:
                proxy_suport = request.ProxyHandler({'http':random.choice(proxy)})
                opener = request.build_opener(proxy_suport)
                r = opener.open("http://www.baidu.com", timeout=2)
                html = r.read()
        except urllib.request.HTTPError as e:
            time.sleep(5)
            print("sleep 5 seconds. url:%s cnt:%d" % (url, cnt))
            if e.code == 500:
                print(e.msg)
                return -2
            print(e.code)
            print(e.msg)
            print(url)
            cnt = cnt + 1
            error = 0
    if cnt == 4:
        return -1
##    codetype = chardet.detect(html_tmp)['encoding']
##    html = decodeFunc(html_tmp)
    html = html.decode('gbk', 'ignore')
    return html

def getNewestDateDB(stockcode):
    Conn = pymysql.connect(host='localhost', port='', user='root', passwd='adency', db='stockdb', charset='utf8')
    Cur = Conn.cursor()
    SQL1 = "select max(holder_date) from " \
           "stockholderdetails where " \
           "stockCode = '%s'" % stockcode
    try:
        Cur.execute(SQL1)
    except Exception as e:
        print(e)
    Cur.execute(SQL1)
    date_now = Cur.fetchone()
    Cur.close()
    Conn.close()
    return date_now[0]

def getHolderNum(html):
    reg = r"""colspan="4">(.*?)<"""
    hd_num = re.compile(reg, re.S)
    html = html.replace("\t", "")
    html = html.replace("\n", "")
    html = html.replace("\r", "")
    num = re.findall(hd_num, html)
    return num

def DivDate(date):
    date = date.replace("(", "")
    date = date.replace(")", "")
    date = date.replace("-", "")
    return date

def DivHldNum(HolderNum):
    HolderNum = HolderNum.replace("(", "")
    HolderNum = HolderNum.replace(")", "")
    return HolderNum

def DivAvgNum(AvgNum):
    AvgNum = AvgNum.replace("(", "")
    AvgNum = AvgNum.replace(")", "")
    reNum = r'\d.*\d'
    rulRegNum = re.compile(reNum)
    AvgNum =re.findall(rulRegNum,AvgNum)
    return AvgNum

#codec swicth
def Code_detect(url):
    urldet = getHtml(url)
    if (urldet != -1):
        codede = chardet.detect(urldet)['encoding']
        print('%s <- %s' %(url,codede))
        return codede