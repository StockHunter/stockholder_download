from multiprocessing import Process
from UpdateStocklist.AddStockList import AddStockListRun
from UpdateStockHolderInfo.AddStockHolderInfo import AddStockHolderInfoRun
from UpdateStockholderCount.AddHolderDataFile import AddHolderDataFileRun

if __name__ == '__main__':
    print("Start update StockList!")
    AddStockListRun()
    print("Completed update StockList!")
    p1 = Process(target=AddStockHolderInfoRun)
    print("Start updateStockHolderInfoRun!")
    p1.start()
    p2 = Process(target=AddHolderDataFileRun)
    print("Start UpdateHolderDateFileRun!")
    p2.start()
    p1.join()
    print("Completed updateStockHolderInfoRun!")
    p2.join()
    print("Completed UpdateHolderDateFileRun!")
