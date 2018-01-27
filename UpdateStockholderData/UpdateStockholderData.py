import pymysql

conn = pymysql.connect(host='localhost',port='',user='root',passwd='adency',db='stockdb',charset='utf8')
cur = conn.cursor()

def update_StockAvgPer():
    sql1 = '''update stockholderdata s, 
           (select h.stockCode, h.holder_date, sum(stock_per) sumper
           from stockholderdetails h 
           group by h.stockCode,h.holder_date) h
           set s.stock_avg_per = h.sumper
           where
           s.stock_code = h.stockCode 
           and
           s.holder_date = h.holder_date'''
    cur.execute(sql1)

def update_StockAvgAmount():
    sql2 = "update stockholderdata " \
           "set " \
           "stock_avg_amount = stock_cnt_one_holder * (100-stock_avg_per-5)/100  "
    cur.execute(sql2)

def UpdateStockholderData():
    update_StockAvgPer()
    update_StockAvgAmount()
    conn.commit()

if __name__ == "__main__":
    update_StockAvgPer()
    update_StockAvgAmount()
    conn.commit()
