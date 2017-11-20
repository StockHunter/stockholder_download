import re
import urllib.request
import pymysql
import time
import chardet
import sys
import logging
sys.path.append("..")
from com.ComMethod import *
import threading
import os
global BASE_FILEPATH
global mutex
global time_start
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s %(process)d %(thread)d [line:%(lineno)d]  %(levelname)s  %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
DATE = 0
ANNOUNCE_DATE = 1
STOCK_HOLDER_INFO = 2
STOCK_AVG_NUM = 3
FILEPATH_BASE = "D:\\python_SRC\\Stock_SRC\\Ver2.0\\log\\"
FILEPATH_HTMLDATA_BASE = "D:\\python_SRC\\Stock_SRC\\Ver2.0\\htmldata\\"
BASE_FILEPATH = getBaseFilePath()
FILEPATH_LOG = FILEPATH_BASE
mutex = threading.Lock()

CNT = 0
LOG = 0

SQL = "no data"
conn = pymysql.connect(host='localhost',port='',user='root',passwd='yuanwei111',db='stockinfo',charset='utf8')
cur = conn.cursor()

#stockcode
def updateStockholderData(tid):
    global DATE
    global ANNOUNCE_DATE
    global STOCK_HOLDER_INFO
    global STOCK_AVG_NUM
    global LOG
    global FILEPATH_LOG
    global FILEPATH_BASE
    global FILEPATH_HTMLDATA_BASE
    global rows
    global rows_len
    global rows_cnt
    global g_StockCodesAll
    while True:
        mutex.acquire()
        rows_cnt = rows_cnt + 1
        if LOG == 1:
            logging.info('rows_cnt:[%s] rows_len:[%d]' % (rows_cnt, rows_len))
        if rows_cnt >= rows_len:
            mutex.release()
            break
        stockcode = str(g_StockCodesAll[rows_cnt]).zfill(6)
        mutex.release()
        FileFullPath = BASE_FILEPATH + stockcode + ".txt"
        if LOG == 1:
            logging.info("stockcode:[%s]" % (stockcode))
        htmlinfo = ReadFile(FileFullPath)
        if htmlinfo == -1:
            return -1
        if htmlinfo == -2:
            return -2
        holderInfoSum = getHolderNum(htmlinfo)
        if holderInfoSum == []:
            logging.warning("No holderInfo stockcode:[%s]" % (stockcode))
            continue
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
        SQL2 = "select MAX(holder_date) from stockholderdata where stock_code = %s" % (str(int(stockcode)))
        FILEPATH_HTMLDATA_FILE_NAME="%s%s" %(FILEPATH_HTMLDATA_BASE,stockcode) + ".txt"
        WriteFile(FILEPATH_HTMLDATA_FILE_NAME,htmlinfo)
        cur.execute(SQL2)
        date_now = cur.fetchone()
        if date_now[0] == None:
            insertDate(stockcode,date,announce_date,stockHolderNum,stockAvgNum, tid)
        elif date > date_now[0] and stockAvgNum != 0 and stockHolderNum != 0:
            insertDate(stockcode,date,announce_date,stockHolderNum,stockAvgNum, tid)
        else:
            pass
        mutex.release()

def insertDate(stockcode, date, announce_date, stockHolderNum, stockAvgNum, tid):
    global CNT
    global FILEPATH_LOG
    global LOG
    date_now_time = time.localtime()
    if announce_date == "":
        announce_date = "0"
    updateTime = "%d%02d%02d" % (date_now_time.tm_year, date_now_time.tm_mon, date_now_time.tm_mday)
    SQL3 = "insert into stockholderdata(stock_code,holder_date,holder_date_announce,holder_cnt,stock_cnt_one_holder,update_Time) " \
           "values(%s,%s,%s,%d,%d,%s);" % (stockcode, date, announce_date, stockHolderNum, stockAvgNum, updateTime)
    try:
        cur.execute(SQL3)
    except Exception as e:
        logging.info(e)
        logging.info("stock_code(%s),holder_date(%s),holder_date_announce(%s),holder_cnt(%d),stock_cnt_one_holder(%d),update_Time(%s)"
              % (stockcode, date, announce_date, stockHolderNum, stockAvgNum, updateTime))
    FILEPATH_LOG = "%s%d%02d%02d" \
                   % (FILEPATH_BASE, date_now_time.tm_year, date_now_time.tm_mon, date_now_time.tm_mday) + ".txt"
    logData = "%s    %s    %s    %d    %d \n" % (stockcode, date, announce_date, stockHolderNum, stockAvgNum)
    if LOG == 1:
        logging.info(logData)
    CNT = CNT + 1
    if CNT % 1 == 0:
        iFunRet = WriteFile(FILEPATH_LOG, logData)
        logging.info("LogFile:[%s]" % logData)
        if iFunRet == False:
            logging.info("Error!! Write file failed!")
            exit()
        conn.commit()

def updateEnd():
    global time_start
    global FILEPATH_LOG
    time_end = time.time()
    logging.info("sum cost time: %f " % (time_end - time_start))
    logging.info("Log path: %s" % (FILEPATH_LOG))

def AddStockholderDataRun():
    global rows_cnt
    global FILEPATH_LOG
    global time_start
    global rows_len
    rows_cnt = -1
    global g_StockCodesAll
    g_StockCodesAll = []
    record_thread = []
    g_StockCodesAll = GetAllStockCodes()
    rows_len = len(g_StockCodesAll)
    logging.info("Stock_sum:[%d]" % rows_len)
    time_start = time.time()
    logging.info(g_StockCodesAll)
    for k in range(8):
        new_thread = threading.Thread(target=updateStockholderData, args=(k,))
        new_thread.start()
        record_thread.append(new_thread)
    for thread in record_thread:
        thread.join()
    updateEnd()
    logging.info("Last commit and cur.close conn.close")
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    rows_cnt = -1
    g_StockCodesAll =[]
    record_thread = []
    g_StockCodesAll = GetAllStockCodes()
    rows_len = len(g_StockCodesAll)
    logging.info("Stock_sum:[%d]" % rows_len)
    time_start = time.time()
    logging.info(g_StockCodesAll)
    for k in range(8):
        new_thread = threading.Thread(target=updateStockholderData, args=(k,))
        new_thread.start()
        record_thread.append(new_thread)
    for thread in record_thread:
        thread.join()
    updateEnd()
    logging.info("Last commit and cur.close conn.close")
    conn.commit()
    cur.close()
    conn.close()
