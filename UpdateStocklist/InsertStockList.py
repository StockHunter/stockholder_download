import re
import urllib.request
import pymysql
import time
import chardet
import sys
sys.path.append("..")
from com.ComMethod import GetAllStockCodes, WriteFile, getHtml,DivAvgNum,DivHldNum,DivDate

LOG_FLAG = 0
STOCK_HOLDER_ALL_CNT = 0
STOCK_NUMBER_ALL_CNT = 0
DATA_ALL_CNT = 0

SQL = "no data"
conn = pymysql.connect(host='localhost',port='',user='root',passwd='yuanwei111',db='stockinfo',charset='utf8')
cur = conn.cursor()

#get http://quote.eastmoney.com/stocklist.html All data
def getAllStockNum(htmlEastMoney):
    reg_allStockNum = r""".html">(.*?)</a>"""
    reg_allStockNum_cmpiled = re.compile(reg_allStockNum,re.S)
    allStockNum = re.findall(reg_allStockNum_cmpiled, htmlEastMoney)
    return allStockNum

def insertStockList(DataAll):
    global DATA_ALL_CNT
    global STOCK_NUMBER_ALL_CNT
    date_now_time = time.localtime()
    updateTime = "%d%02d%02d" % (date_now_time.tm_year, date_now_time.tm_mon, date_now_time.tm_mday)
    for i in range(0, DATA_ALL_CNT-1):
        num = DivNum(DataAll[i])
        name = DivName(DataAll[i])
        num = ''.join(num)
        name = ''.join(name)
        if ((num.find('6') == 0) or (num.find('0') == 0) or (num.find('3') == 0)) and len(num) == 6:
            STOCK_NUMBER_ALL_CNT = STOCK_NUMBER_ALL_CNT + 1
            if i > 1100 :
                if checkStockCodeExist(num):
                    print("num: %s" % (num))
                    print("name: %s" % (name))
                    SQL = "insert into stocklist(stockname, stocknum, updatetime) values('%s','%s','%s')" % (name, num, updateTime)
                    cur.execute(SQL)
                    conn.commit()

def DivName(StockDataOne):
    StockDataOne = StockDataOne.replace("(","")
    StockDataOne = StockDataOne.replace(")","")
    regStr = r'\D.*\D'
    rulRegStr = re.compile(regStr)
    StockDataStr =re.findall(rulRegStr,StockDataOne)
    return StockDataStr

def DivNum(StockDataOne):
    StockDataOne = StockDataOne.replace("(","")
    StockDataOne = StockDataOne.replace(")","")
    reNum = r'\d.*\d'
    rulRegNum = re.compile(reNum)
    StockDataNum =re.findall(rulRegNum,StockDataOne)
    return StockDataNum

def insert():
    global DATA_ALL_CNT
    htmlAllData = getHtml("http://quote.eastmoney.com/stocklist.html")
    DataAll = getAllStockNum(htmlAllData)
    print("DataAll : [%s]" % DataAll)
    DATA_ALL_CNT = len(DataAll)
    iBool = insertStockList(DataAll)
    if iBool == -1:
        print("Program Error!")
    conn.commit()
    cur.close()
    conn.close()
    return True

def checkStockCodeExist(num):
    sql1 = "select * from stocklist where stocknum = %s" % num
    cur.execute(sql1)
    stockcode1 = cur.fetchone()
    if stockcode1 != None:
        return 0
    return 1

if __name__ == '__main__':
    insert()
    print("dataBase OK")
