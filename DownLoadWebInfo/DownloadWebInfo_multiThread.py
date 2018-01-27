import time
import sys
import logging
import threading
import random
import os
sys.path.append("..")
from proxy.proxy import get_proxy
from com.ComMethod import GetAllStockCodes, WriteFile, getHtml, getBaseFilePath
from UpdateStocklist.AddStockList import AddStockListRun

logging.basicConfig(level=logging.DEBUG,
                    format = '%(asctime)s %(filename)s %(process)d %(thread)d [line:%(lineno)d]  %(levelname)s  %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

global FILEPATH_BASE2
global LOG
global list_StockCodes
global local_stockCode
global mutex
global THREAD_NUM

LOG = 1
list_StockCodes = []
FILEPATH_BASE2 = getBaseFilePath()
local_stockCode = threading.local()
mutex = threading.Lock()
THREAD_NUM = 5
Proxy_list = []


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
    global Proxy_list
    stockCode = local_stockCode.stock
    web = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/%s.phtml" \
          % (stockCode)
    logging.info("web:[%s]" % (web))
    mutex.acquire()
    print("sleep 0.1s!")
    time.sleep(0.1)
    mutex.release()
    timeStart1 = time.time()
    htmlinfo = getHtml(web, Proxy_list)
#    htmlinfo = getHtml(web)

    if htmlinfo == -1:
        logging.info("WEB ERROR!! web:[%s]" % web)
        return False
    WriteFile(PathTmp, htmlinfo)
    logging.info("FilePath: %s" % PathTmp)
    logging.info("time:[%d]" % (time.time() - timeStart1))

def run(basePath=FILEPATH_BASE2, mode="continue"):
    logging.info("GetWebInfo Start")
    list_StockCodes = GetAllStockCodes()
    downloadAllRun(list_StockCodes)
    nRet = checkFileSize(list_StockCodes)
    if nRet == False:
        downloadAllRun(list_StockCodes)
    logging.info("GetWebInfo End")

def downloadAllRun(list_StockCodes):
    global FILEPATH_BASE2
    global THREAD_NUM
    record_thread = []
#    AddStockListRun()
    logging.info("Completed update StockList!")
    if os.path.exists(FILEPATH_BASE2) == False:
        os.mkdir(FILEPATH_BASE2, 777)
    for k in range(THREAD_NUM):
        new_thread = threading.Thread(target=DownloadWebInfoStart)
        new_thread.start()
        record_thread.append(new_thread)
    for thread in record_thread:
        thread.join()
    return True

def checkFileSize(list_StockCodes):
    global FILEPATH_BASE2
    errFlag = 0
    for stockcode in list_StockCodes:
        path = FILEPATH_BASE2 + stockcode + ".txt"
        if os.stat(path).st_size < 5000:
            os.remove(path)
            errFlag = -1
    if errFlag == -1:
        return False
    return True

if __name__ == '__main__':
#    logging.info("Start update StockList!")
    print(os.path.split(os.path.realpath(__file__))[0])
    Proxy_list = get_proxy(6)
    list_StockCodes = GetAllStockCodes()
    downloadAllRun(list_StockCodes)
    nRet = checkFileSize(list_StockCodes)
    if nRet == False:
        downloadAllRun(list_StockCodes)
    logging.info("GetWebInfo End")
