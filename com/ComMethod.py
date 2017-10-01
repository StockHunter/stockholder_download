import re
import urllib.request
import chardet
import threading
import os
import pymysql

def WriteFile(fname,data):
    f = open(fname, 'w')
    if f:
        f.write(data)
        f.close()
    else:
        return False

def lGetStockCodes():
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
