import re
import urllib.request
import pymysql
import time
import chardet
from com.ComMethod import *
import threading
import os
global BASE_FILEPATH
global mutex

DATE = 0
ANNOUNCE_DATE = 1
STOCK_HOLDER_INFO = 2
STOCK_AVG_NUM = 3
FILEPATH_BASE = "D:\\python_SRC\\Stock_SRC\\Ver2.0\\log\\"
FILEPATH_HTMLDATA_BASE = "D:\\python_SRC\\Stock_SRC\\Ver2.0\\htmldata\\"
BASE_FILEPATH = "D:\\python_SRC\\Stock_SRC\\tmpData\\20171001\\"
mutex = threading.Lock()

CNT = 0
LOG = 1

SQL = "no data"
conn = pymysql.connect(host='localhost',port='',user='root',passwd='yuanwei111',db='stockinfo',charset='utf8')
cur = conn.cursor()

def WriteFile(fname,data):
    f = open(fname, 'a')
    if f:
        f.write(data)
        f.close()
    else:
        return False

#stockcode
def updateStockHolderCnt(tid):
    global DATE
    global ANNOUNCE_DATE
    global STOCK_HOLDER_INFO
    global STOCK_AVG_NUM
    global LOG
    global CNT
    global FILEPATH_LOG
    global FILEPATH_BASE
    global FILEPATH_HTMLDATA_BASE
    global rows
    global rows_len
    global rows_cnt
    global g_StockCodesAll
    print("tid: ", tid, "start")
    while True:
        mutex.acquire()
        rows_cnt = rows_cnt + 1
        if LOG == 1:
            print("rows_cnt:", rows_cnt, "rows_len:", rows_len)
        if rows_cnt >= rows_len:
            print("Last Stock!")
            updateEnd()
            mutex.release()
            break
        stockcode = str(g_StockCodesAll[rows_cnt]).zfill(6)
        print("%s ,threading:%d ,mutex.acquire1" % (stockcode, tid))
        mutex.release()
        print("%s,threading:%d ,mutex.release1" % (stockcode, tid))
        FileFullPath = BASE_FILEPATH + stockcode + ".txt"
        if LOG == 1:
            print("%s threading(%s)" % (stockcode, tid))
        time1 = time.time()
        htmlinfo = ReadFile(FileFullPath)
        time2 = time.time()
        print("%s, Time:%f, threading:%d" % (stockcode, (time2-time1), tid))
        if htmlinfo == -1:
            return -1
        if htmlinfo == -2:
            return -2
        holderInfoSum = getHolderNum(htmlinfo)
        date = DivDate(holderInfoSum[DATE])
        announce_date = DivDate(holderInfoSum[ANNOUNCE_DATE])
        stockHolderNum = DivHldNum(holderInfoSum[STOCK_HOLDER_INFO])
        if stockHolderNum == "":
            stockHolderNum = 0
        stockHolderNum = int(stockHolderNum)
        stockAvgNum = DivAvgNum(holderInfoSum[STOCK_AVG_NUM])
        stockAvgNum = ''.join(stockAvgNum)
        if stockAvgNum == "":
            stockAvgNum = 0
        stockAvgNum = int(stockAvgNum)
        mutex.acquire()   #add lock
        SQL2 = "select MAX(holder_date) from stockholdercnt where stock_code = %s" % (str(int(stockcode)))
        FILEPATH_HTMLDATA_FILE_NAME="%s%s" %(FILEPATH_HTMLDATA_BASE,stockcode) + ".txt"
        WriteFile(FILEPATH_HTMLDATA_FILE_NAME,htmlinfo)
        print("%s, threading:%d ,mutex.acquire2" % (stockcode, tid))
        cur.execute(SQL2)
        date_now = cur.fetchone()
        if date > date_now[0] and stockAvgNum != 0 and stockHolderNum != 0:
            date_now_time = time.localtime()
            updateTime = "%d%02d%02d" % (date_now_time.tm_year, date_now_time.tm_mon, date_now_time.tm_mday)
            SQL3 = "insert into stockholdercnt(stock_code,holder_date,holder_date_announce,holder_cnt,stock_cnt_one_holder,update_Time) " \
                   "values (%s,%s,%s,%d,%d,%s)" % (stockcode, date, announce_date, stockHolderNum, stockAvgNum, updateTime)
            try:
                cur.execute(SQL3)
            except Exception as e:
                print(e)
                print("stock_code(%s),holder_date(%s),holder_date_announce(%s),holder_cnt(%d),stock_cnt_one_holder(%d)"
                      % (stockcode, date, announce_date, stockHolderNum, stockAvgNum))
            FILEPATH_LOG = "%s%d%02d%02d" \
                    % (FILEPATH_BASE, date_now_time.tm_year, date_now_time.tm_mon, date_now_time.tm_mday) + ".txt"
            logData = "%s    %s    %s    %d    %d \n" % (stockcode, date, announce_date, stockHolderNum, stockAvgNum)
            if LOG == 1:
                print(logData)
            CNT = CNT + 1
            if CNT % 1 == 0:
                iFunRet = WriteFile(FILEPATH_LOG, logData)
                print("WriteFile: %s by tid:%d " % (logData, tid))
                if iFunRet == False:
                    print("Error!! Write file failed!")
                    exit()
                conn.commit()
        else:
            print("No need to update! date(%s),date_now[0](%s),stockAvgNum(%d),stockHolderNum(%d)" % (date,date_now[0],stockAvgNum,stockHolderNum))
        mutex.release()
        print("%s, threading:%d ,mutex.release2" % (stockcode, tid))

def updateEnd():
    global time_start
    time_end = time.time()
    print("sum cost time: ", (time_end-time_start))
    print("Log path: %s" % (FILEPATH_LOG))
    print("Update OK.")

global FILEPATH_LOG
rows_cnt = -1
g_StockCodesAll =[]
record_thread = []
g_StockCodesAll = GetAllStockCodes()
rows_len = len(g_StockCodesAll)
print("Stock_sum:", rows_len)

print(g_StockCodesAll)

for k in range(1):
    new_thread = threading.Thread(target=updateStockHolderCnt, args=(k,))
    new_thread.start()
    record_thread.append(new_thread)

for thread in record_thread:
    thread.join()

print("Last commit and cur.close conn.close")
conn.commit()
cur.close()
conn.close()