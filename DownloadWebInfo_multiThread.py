import time
from com.ComMethod import lGetStockCodes, WriteFile, getHtml
import threading

global FILEPATH_BASE2
global LOG
global list_StockCodes
global local_stockCode
global mutex

LOG = 1
list_StockCodes = []
FILEPATH_BASE2 = "D:\\python_SRC\\Stock_SRC\\tmpData\\20171001\\"
local_stockCode = threading.local()
mutex = threading.Lock()

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
        print("ThreadName:[%s], stock:[%s]" % (threading.current_thread().name, local_stockCode.stock ))
        if stockCode > "600979" and stockCode < "603309":
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


'''
    global LOG
    global FILEPATH_LOG
    print ("BaseFilePath: " + sFilePath )
    for stockCode in list_StockCodes:
        print ("code:[%s]" % stockCode)
        stockCode = str(stockCode).zfill(6)
        if stockCode > "600703" and stockCode < "603355":
            web = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/%s.phtml" \
                           % (stockCode)
            print("web:[%s]" % web)
            timeStart1 = time.time()
            htmlinfo = getHtml(web)
            PathTmp = sFilePath + stockCode + ".txt"
            print("FilePath: " + PathTmp)
            WriteFile(PathTmp, htmlinfo)
            print("time: %d " % (time.time() - timeStart1))
'''

def run():
    global LOG
    print("GetWebInfo Start")
    lStockCode = []
    lStockCode = lGetStockCodes()
    nStockCodeListLen = len(lStockCode)
    if LOG == 1:
        print("nStockCodeListLen:", nStockCodeListLen)
        print(lStockCode)
    DownloadWebInfo(lStockCode)
    print("GetWebInfo End")

if __name__ == '__main__':
    print("GetWebInfo Start")
    list_StockCodes = lGetStockCodes()
    t1 = threading.Thread(target = DownloadWebInfoStart)
    t2 = threading.Thread(target = DownloadWebInfoStart)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("GetWebInfo End")
