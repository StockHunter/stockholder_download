from multiprocessing import Process
from UpdateStocklist.AddStockList import AddStockListRun
from UpdateStockHolderInfo.AddStockholderDetails import AddStockholderDetailsRun
from UpdateStockholderData.AddStockholderData import AddStockholderDataRun
from UpdateStockholderData.UpdateStockholderData import *

if __name__ == '__main__':
    print("Start update StockList!")
    AddStockListRun()
    print("Completed update StockList!")
    p1 = Process(target=AddStockholderDetailsRun)
    print("Start AddStockholderDetailsRun!")
    p1.start()
    p2 = Process(target=AddStockholderDataRun)
    print("Start AddStockholderDataRun!")
    p2.start()
    p1.join()
    print("Completed AddStockholderDetailsRun!")
    p2.join()
    print("Completed AddStockholderDataRun!")
    UpdateStockholderData()
    print("Completed UpdateStockholderData!")
