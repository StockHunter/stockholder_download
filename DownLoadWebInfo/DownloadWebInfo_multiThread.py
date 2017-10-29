import time
import sys
sys.path.append("..")
from com.ComMethod import GetAllStockCodes, WriteFile, getHtml
import threading
import os

global FILEPATH_BASE2
global LOG
global list_StockCodes
global local_stockCode
global mutex
global THREAD_NUM
global record_thread

LOG = 1
list_StockCodes = []
FILEPATH_BASE2 = "D:\\python_SRC\\Stock_SRC\\tmpData\\20171028\\"
local_stockCode = threading.local()
mutex = threading.Lock()
THREAD_NUM = 5
record_thread = []

def DownloadWebInfoStart(sFilePath = FILEPATH_BASE2, mode = "continue"):
    global mutex
    global list_StockCodes
    while len(list_StockCodes) > 0:
        mutex.acquire()
        try:
            stockCode = list_StockCodes.pop()
        except Exception as err:
            print(err)
            break
        mutex.release()
        stockCode = str(stockCode).zfill(6)
        local_stockCode.stock = stockCode
        PathTmp = sFilePath + stockCode + ".txt"
        if mode == "continue":
            if os.path.exists(PathTmp) == False:
                downLoadWebInfo(PathTmp)
        else:
            downLoadWebInfo(PathTmp)

def downLoadWebInfo(PathTmp):
    global LOG
    stockCode = local_stockCode.stock
    web = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/%s.phtml" \
          % (stockCode)
    print("ThreadName:[%s], web:[%s]" % (threading.current_thread().name, web))
    mutex.acquire()
    time.sleep(5)
    mutex.release()
    timeStart1 = time.time()
    htmlinfo = getHtml(web)
    WriteFile(PathTmp, htmlinfo)
    print("ThreadName:[%s], FilePath: %s" % (threading.current_thread().name, PathTmp))
    print("ThreadName:[%s], time:[%d]" % (threading.current_thread().name, time.time() - timeStart1))

def run(basePath=FILEPATH_BASE2, mode="continue"):
    global list_StockCodes
    global record_thread
    print("GetWebInfo Start")
    list_StockCodes = GetAllStockCodes()
    for k in range(THREAD_NUM):
        new_thread = threading.Thread(target=DownloadWebInfoStart, args=(basePath, mode))
        new_thread.start()
        record_thread.append(new_thread)
    for thread in record_thread:
        thread.join()
    print("GetWebInfo End")

if __name__ == '__main__':
    print("GetWebInfo Start")
    list_StockCodes = GetAllStockCodes()
    for k in range(THREAD_NUM):
        new_thread = threading.Thread(target=DownloadWebInfoStart)
        new_thread.start()
        record_thread.append(new_thread)
    for thread in record_thread:
        thread.join()
    print("GetWebInfo End")