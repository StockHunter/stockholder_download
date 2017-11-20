import time
import sys
import logging
sys.path.append("..")
from com.ComMethod import GetAllStockCodes, WriteFile, getHtml, getBaseFilePath
import threading
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s %(process)d %(thread)d [line:%(lineno)d]  %(levelname)s  %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

global FILEPATH_BASE2
global LOG
global list_StockCodes
global local_stockCode
global mutex
global THREAD_NUM
global record_thread

LOG = 1
list_StockCodes = []
FILEPATH_BASE2 = getBaseFilePath()
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
            logging.error(err)
            mutex.release()
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
    logging.info("web:[%s]" % (web))
    mutex.acquire()
    time.sleep(4)
    mutex.release()
    timeStart1 = time.time()
    htmlinfo = getHtml(web)
    if htmlinfo == -1:
        logging.info("WEB ERROR!! web:[%s]" % web)
        return False
    WriteFile(PathTmp, htmlinfo)
    logging.info("FilePath: %s" % PathTmp)
    logging.info("time:[%d]" % (time.time() - timeStart1))

def run(basePath=FILEPATH_BASE2, mode="continue"):
    global list_StockCodes
    global record_thread
    global FILEPATH_BASE2
    logging.info("GetWebInfo Start")
    if os.path.exists(FILEPATH_BASE2) == False:
        os.mkdir(FILEPATH_BASE2, 777)
    list_StockCodes = GetAllStockCodes()
    for k in range(THREAD_NUM):
        new_thread = threading.Thread(target=DownloadWebInfoStart, args=(basePath, mode))
        new_thread.start()
        record_thread.append(new_thread)
    for thread in record_thread:
        thread.join()
    logging.info("GetWebInfo End")

if __name__ == '__main__':
    logging.info("GetWebInfo Start")
    if os.path.exists(FILEPATH_BASE2) == False:
        os.mkdir(FILEPATH_BASE2, 777)
    list_StockCodes = GetAllStockCodes()
    for k in range(THREAD_NUM):
        new_thread = threading.Thread(target=DownloadWebInfoStart)
        new_thread.start()
        record_thread.append(new_thread)
    for thread in record_thread:
        thread.join()
    logging.info("GetWebInfo End")