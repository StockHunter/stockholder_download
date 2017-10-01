import time
from com.ComMethod import lGetStockCodes, WriteFile, getHtml

global FILEPATH_LOG
global LOG
LOG = 1
FILEPATH_BASE2 = "D:\\python_SRC\\Stock_SRC\\tmpData\\20171001\\"

def DownloadWebInfo(list_rows, sFilePath = FILEPATH_BASE2):
    global LOG
    global FILEPATH_LOG
    print ("BaseFilePath: " + sFilePath )
    for stockCode in list_rows:
        print ("code:[%s]" % stockCode)
        stockCode = str(stockCode).zfill(6)
        if stockCode > "600703" and stockCode < "603355":
#        if stockCode > "600323" or stockCode < "600000":
            web = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/%s.phtml" \
                           % (stockCode)
            print("web:[%s]" % web)
            timeStart1 = time.time()
            htmlinfo = getHtml(web)
            PathTmp = sFilePath + stockCode + ".txt"
            print("FilePath: " + PathTmp)
            WriteFile(PathTmp, htmlinfo)
            print("time: %d " % (time.time() - timeStart1))

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
    lStockCode = []
    lStockCode = lGetStockCodes()
    nStockCodeListLen = len(lStockCode)
    if LOG == 1:
        print("nStockCodeListLen:", nStockCodeListLen)
        print(lStockCode)
    DownloadWebInfo(lStockCode)
    print("GetWebInfo End")
