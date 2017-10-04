import time
from com.ComMethod import lGetStockCodes, WriteFile, getHtml
import threading

global FILEPATH_BASE2
global LOG
global list_StockCodes
global local_stockCode
global mutex
global THREAD_NUM

LOG = 1
list_StockCodes = []
FILEPATH_BASE2 = "D:\\python_SRC\\Stock_SRC\\tmpData\\20171001\\"
local_stockCode = threading.local()
mutex = threading.Lock()
THREAD_NUM = 4

def DownloadWebInfoStart(sFilePath = FILEPATH_BASE2):
    global mutex
    global list_StockCodes
    while len(list_StockCodes) > 0:
        mutex.acquire()
        stockCode = list_StockCodes.pop()
        mutex.release()
        timeStart1 = time.time()
        stockCode = str(stockCode).zfill(6)
        local_stockCode.stock = stockCode
        local_stockCode.timeStart = timeStart1
        print("ThreadName:[%s], stock:[%s]" % (threading.current_thread().name, local_stockCode.stock))
        if stockCode > "600979" and stockCode < "603268":
            time.sleep(3)
            downLoadWebInfo(sFilePath)

def downLoadWebInfo(sFilePath):
    global LOG
    stockCode = local_stockCode.stock
    web = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/%s.phtml" \
          % (stockCode)
    print("web:[%s]" % web)
    htmlinfo = getHtml(web)
    PathTmp = sFilePath + stockCode + ".txt"
    print("FilePath: " + PathTmp)
    WriteFile(PathTmp, htmlinfo)
    print("time: %d " % (time.time() - local_stockCode.timeStart))

def run(listStockCodes):
    global list_StockCodes
    print("GetWebInfo Start")
    list_StockCodes = listStockCodes
    for k in range(THREAD_NUM):
        new_thread = threading.Thread(target = DownloadWebInfoStart)
        new_thread.start()
        record_thread.append(new_thread)
    for thread in record_thread:
        thread.join()
    print("GetWebInfo End")

if __name__ == '__main__':
    print("GetWebInfo Start")
    list_StockCodes = lGetStockCodes()
    for k in range(THREAD_NUM):
        new_thread = threading.Thread(target = DownloadWebInfoStart)
        new_thread.start()
        record_thread.append(new_thread)
    for thread in record_thread:
        thread.join()
    print("GetWebInfo End")