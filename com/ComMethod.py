import re
import urllib.request
import chardet
import threading
import os
import pymysql
import time

def WriteFile(fname,data):
    f = open(fname, 'w')
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
    conn = pymysql.connect(host='localhost',port='',user='root',passwd='yuanwei111',db='stockinfo',charset='utf8')
    cur = conn.cursor()
    lStockCode = []
    SQL = "SELECT distinct(stock_code) from" \
          " stockholdercnt"
    cur.execute(SQL)
    rows = cur.fetchall()
    for row in rows:
        lStockCode.append(row[0])
    cur.close()
    conn.close()
    return lStockCode

#get web all data
def getHtml(url):
    error = 0
    cnt = 1
    while error == 0 and cnt < 10:
        error = 1
        try:
            page = urllib.request.urlopen(url, timeout=2000)
        except urllib.request.HTTPError as e:
            time.sleep(15)
            print("sleep 15 seconds. url:%s cnt:%d" % (url, cnt))
            if e.code == 500:
                print(e.msg)
                return -2
            print(e.code)
            print(e.msg)
            print(url)
            cnt = cnt +1
            error = 0
    if cnt == 10:
        return -1
    html_tmp = page.read()
##    codetype = chardet.detect(html_tmp)['encoding']
##    html = decodeFunc(html_tmp)
    html = html_tmp.decode('gbk','ignore')
    page.close()
    return html

def getNewestDateDB(stockcode):
    Conn = pymysql.connect(host='localhost', port='', user='root', passwd='yuanwei111', db='stockinfo', charset='utf8')
    Cur = Conn.cursor()
    SQL1 = "select max(holder_date) from " \
           "holderinfo where " \
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

