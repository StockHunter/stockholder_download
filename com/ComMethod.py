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
