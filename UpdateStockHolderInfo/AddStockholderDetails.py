# get web all data
import re
from bs4 import BeautifulSoup
import pymysql
import time
import threading
import sys
import logging
sys.path.append("..")
from com.ComMethod import GetAllStockCodes, ReadFile, getNewestDateDB,getBaseFilePath

global countOK
global countNG
global DEBUG_LOG
global ERROR_LEN_LOG
global POPLIST_HOLDER_TYPE
global StockCodesAll
global BASE_FILEPATH
global Local_Stock
global ErrMsg
global UpdateGenrate
global InsertStockCode
global mutex
global THREAD_NUM

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s %(process)d %(thread)d [line:%(lineno)d]  %(levelname)s  %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

UpdateGenrate = [0, 1, 2, 3]
Local_Stock = threading.local()
g_StockCodesAll = []
ERROR_LEN_LOG = [0]
DEBUG_LOG = 0
countNG = 0
countOK = 0
THREAD_NUM = 5
BASE_FILEPATH = getBaseFilePath()
mutex = threading.Lock()
InsertStockCode = []
Header = {}
Header[
    'User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19'
SQL = "no data"
ErrMsg = []

POPLIST_HOLDER_TYPE = ["未流通法人股", "不详", "境内法人股", '截至日期', "公告日期", "股东说明", "股东总数", "境外法人股",
           "平均持股数", "编号", "股东名称", "持股数量(股)", "社会公众股", "国家股,境内法人股",
           "持股比例(%)", "国有法人股", "股本性质", '', "流通A股", "公告日期", "限售流通股", "已流通A股", "外资股",
           "A股流通", "流通A股,限售流通股", "法人股", "限售流通股,流通A股", "流通股", "国有股`",
           "国有股,境内法人股", "国有法人股,流通A股", "境内法人股，国有法人股", "国有股,流通A股", "一般法人股",
           "外资法人股", "社会法人股", "流通H股", "其它未流通股", "未流通A股", "H股", "A股", "流通A股,流通H股",
            "外资H股", "社会流通股", "限售流通股,流通H股", "限售流通股，流通A股","境内法人股`",
           "流通A股,限售流通股,流通H股", "流通B股", "发起人法人股", "国家股,法人股", "流通受限股份", "流通", "B股",
           "境外法人股,流通B股", "国有法人股,法人股", "可转让股份,境内法人股", "B股流通", "法人股,流通股", "B股流通股",
           "国有股、境内法人股", "已流通B股", "可转让股份,自然人股", "境内法人股,可转让股份", "自然人股", "定向法人股",
           "流通A股,流通B股", "定向法人国家股", "定向募集法人股", "国有法人股,境内法人股", "募集法人股",
           '限售流通股,流通A股,流通H股', "国家股,社会法人股", "发起人国家股", "流通A股,流通H股,限售流通股",
           "国有股,法人股", "境内法人股，流通股", "国有股,可转让股份", "可转让股份", "限售流通股,流通A股,流通B股",
           "公众股", "流通股A股", "流通股B股", "发起法人股", "A、B股", "人民币普通股", "流通B股,限售流通股",
           "境内法人股,流通股", "国有股,法人股,流通A股", "社会法人股份", "限售流通股,流通B股", "A股法人股,B股法人股",
           "流通B股,流通A股", "外资法人股及B股", "定向境内法人股", "发起人国有股", "发起人境内法人股", "限售流通B股",
           "定向法人国有法人股", "国家股，境内法人股", "国有股，境内法人股", "A股公众股", "发起人国有股东", "定向法人境内法人股",
           "定向法人境内法人股", "境外社会公众股", "境内社会公众股", "发起人境外法人股", "法人股,国家股", "境外上市外资股",
           "境内定向法人股", "国有股,流通股", "境内发起人法人股", "境外发起人法人股", "国有股东", "国家股,国有法人股,流通A股",
           "流通H股,限售流通股", "发起人股份", "国家股,流通股", "流通B股,流通H股", "已流通", "境内法人股,流通A股", "境内法人股、流通A股",
           "发起人股", "发起法人股,法人股", "境内上市外资股", "法人股,流通A股", "公众股A股", "境内外资股（B股）", "流通A股,限售流通A股",
           "流通A股,其它未流通股", "国家股,法人股,流通股", "法人股,国家股,流通A股,流通B股", "自然人股,流通A股", "国有股,境内法人股,流通A股",
           "国家股,非流通法人股,流通股", "国家股等", "其它未流通股,流通A股", "国有股，法人股，流通A股", "自然人流通股", "定向国有法人股",
           "法人股/流通A股", "流通股，其它未流通股", "国有股，法人股", "国有股、法人股", "国有股/法人股", "流通A股,其他未流通股",
           "境外流通股", "A股流通股", "发起人国有法人股", "外资法人股，B股", "境内上市外资股（B股）", "外资法人股、B股", "国有股,国有法人股,流通A股",
           "上市流通股", "国家股,国有法人股,流通股", "普通股", "国有法人股,国家股", "国有股、国有法人股","国家股,国有法人股",
           "国有股，国有法人股", "自然人持有的未流通股", "个人", "国家股，国有法人股", "国有法人股、法人股", "国有法人", "法人股、社会公众股",
           "非国有股", "可转让股份,流通受限股份", "流通股,法人股", "发起法人股、法人股", "流通股、法人股", "香港上市H股", "流通A股,流通B股,限售流通股",
           "定向法人境内法人股,流通股", "定向法人境内法人股,发起人境内法人股", "国家持有股份", "国有法有股", "国有法人股（未流通A股）", "法人股（未流通A股）",
           "流通受限股份,可转让股份", "A股社会流通股", "未流通国有股", "发起人境内法人股,定向法人境内法人股", "国家股、法人股", "发起国有法人股",
           "外资法人股,流通B股", "未流通", "境内法人股f", "发起人法人股,定向法人股", "发起人国家股及发起人国有法人股", "募集法人股,流通股",
           "内部职工股,A股", "法人股、流通股", "非上市流通股", "国有法人股，流通股", "国家股，法人股", "发起人法人股/定向法人股", "国家股、国有法人股",
           "法人股、公众股", "发起人法人股，定向法人股", "法人股，流通股", "境内外资股", "H股流通", "境内法人股、流通股", "社会公众股（已流通A股）",
           "发起人境内法人股、定向法人境内法人股", "已流通社会公众股", "社会法人股、社会公众股", "国家法人股", "法人A股", "社会法人股,社会公众股",
           "募集法人股、社会公众股", "募集法人股,社会公众股", "发起人募集法人股", "国家持有股", "社会法股", "配股包销内部职工股", "国有股法人股",
           "已流通法人股", "社会公众、流通股", "境内地人股", "其他流通股", "上市流通股份", "流通股东", "流通流", "国有法人未流通股", "法人未流通股",
           "流通A股\n", "Ａ股流通股", "H股流通股", "国有法人股,社会法人股", "定向法人境内法人股和流通股", "法人股,国有股", "流股股", "国家股,定向法人股",
           "社会公众股股", "发起人国有法人股,定向法人股", "国有法人股,定向法人股", "国家股、境内法人股", "发起人国家股,定向法人国家股", "发起人国有法人股、定向法人股",
           "发起人国家股、定向法人股", "国有法人股、定向法人股", "国家股、定向法人股", "发起人国有法人股，定向法人股", "发起人国家股，定向法人股", "发起人国家股,发起人境内法人股",
           "发起人国家股，定向法人国家股", "流通股及高管股", "其他法人股", "一般法人持股", "国有股、未流通", "法人股、未流通", "国有法人股，社会公众股", "流通A股,国有股",
           "发起国有股", "有限售股份,流通A股", "发起人国家股、定向境内法人股", "国有法人股,社会公众股", "发起人自然人股", "发起自然人股", "发起自然人股,流通股",
           "内资法人股", "非流通股", "非国有法人股", "国有法人股、社会法人股", "国有股、流通股", "国有股股东", "未流通境内法人股", "境内发起人股", "国家股,国有法人股,法人股",
           "募集国有法人股", "社会流通股\x7f", "未流通境内法人持有股份", "已上市流通股", "发起人国家股,定向境内法人股", "流通A股,境内法人股", "流通A股，境内法人股",
           "国家股,流通A股", "法人股、A股", "非流通股份", "自然人", "国有法人股、国家股", "国有股、A股", "国内法人股", "国有股、流通A股", "发起人社会法人股",
           "个人股", "发起人一般法人股", "未流通境内法人持有股", "国有股，国有法人股，法人股", "未流通国有法人股", "发起人国家股,流通股", "社会股", "限售流通股\\x7f", "企业法人股",
           "未流通股", "流通股份", "发起人国家股,流通股", "未流通B股", "社会股", "国有股，流通股","未上市流通股", "普通流通股", "定向法人境内法人股,流通A股",
           "发起人国家股，流通股", "已流通股", "发起人国家股、流通股", "发起人国家股,流通A股", "已流通社会公众股、A股", "发起人外资股", "发起人境内自然人股", "自然有人股",
           "境内自然人股", "境内社会法人股", "国有股人股", "发起自然人", "发起人自然人股,流通股", "发起人自然人股、流通股", "发起人自然人股，流通股", "社会法人股,流通股",
           "流通社会公众股", "国有股,境内法人股,社会公众股", "法人股、国家股", "外资流通股", "国家股及法人股", "社会法人股,优先股", "国有法人股,社会法人股,流通股",
           "职工股", "社会法人股,流通股", "限售流通A股", "国有法人股、流通股", "法人股,社会公众股", "法人股、流通A股", "发起人、法人股", "境内法人股，流通A股", "限售流通股,流通Ａ股",
           "国家股,境内法人股,流通A股", "国家股,法人股,社会公众股", "流通股，法人股", "社会法人股、流通股", "国有法人股，境内法人股", "转配股", "国家股,境内法人股,流通股",
           "社会公众股、法人股", "社会公众股、国有法人股、社会法人股", "国有法人股、法人股、社会公众股", "国有法人股，社会法人股", "境内发起人股及社会法人股",
           "境内发起人股、及社会法人股", "境内发起人股,社会法人股", "境内发起人股，社会法人股", "法人股，流通A股", "外资发起人法人股", "发起人法人股，募集法人股",
           "国有发起人法人股", "国有股，流通A股", "外资股B股", "发起人法人外资股", "未流通A股,流通A股", "流通A股,限售流通股,流通B股", "非发起人国有法人股",
           "国家股,国有法人股,社会法人股,流通股", "境外社会公众股（H股）", "外资股,流通B股", "法人股，社会公众股", "社会法人股，流通股", "国有股,法人股,流通股",
           "流通A股,未流通股", "公募法人股", "境内募集法人股", "募集人法人股", "法人股,流通B股", "非流通国有法人股", "已流通(A股)", "境内法人股,国有股", "H股外资股",
           "外资法人", "国家股,募集法人股", "国有法人股,流通股", "H股（社会公众股）", "社会募集法人股", "国有股、法人股、流通股\n", "流通H股,流通A股", "境外法人股、流通B股",
           "流通H股,流通A股", "流通H股,限售流通H股", "限售流通H股", "国有股、社会法人股、流通股", "外资股、境内上市外资股", "募集法人股,国家股", "国有法人股,社会法人股,国家股,流通股",
           "A股（国有法人股）", "非流通国家股", "外资股、境内上市外资股", "非流通法人股", "流通A股,流通H股,限售流通A股", "社会公众股,社会法人股", "非外资法人股",
           "流通H股,限售流通A股", "限售流通H股,流通A股", "流A通股", "社会公众股H股", "流通B股,境外法人股", "A股国有法人股", "限售流通H股,流通A股", "流通外资股", "内资流通股",
           "限售流通H股,流通H股", "人民币自然人股", "吸收合并形成", "社会法人股,流通A股", "外资法人股,外资流通股", "流通A股、法人股", "其他未流通股", "社会法人", "社会公共股",
           "社会法人股，流通A股", "流通A股,流通S股", "国有法人股，法人股", "非流通外资股", "发起人个人股", "自然人股、流通股", "国有股,社会法人股", "国家股、社会法人股", "非流通外资股",
           "社会法人股,发起人法人股", "发起人非流通股", "国有发人股", "外资股,社会法人股", "社会发起人法人股", "国有法人股、募集法人股、流通股", "受让发起人法人股",
           "境外法人股,B股", "上市流通人民币普通股", "自然人持有的非流通股", "非流通自然人股", "国家股、流通股", "境外法人股,B股", "国有发起人股", "境内社会法人股,流通A股",
           "流通S股", "外资发起法人股", "非国有股/法人股", "自然人股,流通股", "其他发起人股", "其它未流通股,社会公众股", "境外发起人个人股", "外资股,B股", "外资自然人股",
           "其它非流通股", "已流通A股,其它未流通股", "职工股、流通股", "已上市流通股份", "自然人持有的非流通股,社会公众股", "募集法人股,流通A股", "募集法人股，流通股",
           "其他未流通", "ADR代表的H股", "自然人股", "自然人股,职工股", "内部职工股、自然人持有的非流股", "法起人境内法人股", "法人股,优先股", "法人股/流通股",
           "发起人国家股，发起人境内法人股", "限售流通股\x7f","发起人国家股，定向法人境内法人股","法人股，优先股","募集法人股、流通股","可转让股份,国有股",
            "社公公众股","自然人股","非国有股,社会法人股","自然人股`","自然人非流通股","自然人股及内部职工股","自然人股,社会公众股","流通股、社会法人股",
            "境内法人股","NET置换后形成的股份","法人","固有法人股","置换后形成的股份","流通A股、社会法人股","境内法人股","国有法人股,A股","国有法人股,A股流通股",
            "境内法人股","境内法人股","境内法人股`","自然人股,可转让股份"]

def DivDate(date):
    date = date.replace("-", "")
    return date

def transToBS_stockBasic(webInfo):
    try:
        bsObj = BeautifulSoup(webInfo, "lxml")
    except AttributeError as e:
        logging.info("AttributeError!!")
        return None
    return bsObj

def getHolderNum(html):
    reg = r"""colspan="4">(.*?)<"""
    hd_num = re.compile(reg, re.S)
    html = html.replace("\t", "")
    html = html.replace("\n", "")
    html = html.replace("\r", "")
    num = re.findall(hd_num, html)
    for a in range(len(num)):
        num[a] = num[a].replace("股(按总股本计算)", "")
    return num

def dataCheck(list1):
    global ERROR_LEN_LOG
    global DEBUG_LOG
    global countOK
    global countNG
    for a in range(len(list1)):
        len1 = len(list1[a])
        if len1%4 != 0:
            list1[a].append("NG")
            if DEBUG_LOG == 2:
                logging.info("Data Error!!! errLen[%d]" % len1 )
                logging.info("Count[%d]: %s " % (a, list1[a]))
                errString = "Count[" + str(a) + "] len[" + str(len1) + "]  code[" + Local_Stock.code + "]: " + str(list1[a])
                ERROR_LEN_LOG.append(errString)
                logging.info("Sum Error Info:")
                logging.info(ERROR_LEN_LOG)
                for n in range(len(ERROR_LEN_LOG)):
                    logging.info(ERROR_LEN_LOG[n])
            if DEBUG_LOG == 1:
                logging.info("=============InputData Start===============")
                for n in range(len(list1)):
                    logging.info("Count[%d]:%s " % (n,list1[n]))
                logging.info("=============InputData End  ===============")
            countNG = countNG + 1
            logging.info("countOK: %d,countNG:%d code:%s " % (countOK, countNG, Local_Stock.code))
            break
        countOK = countOK + 1
#        logging.info("countOK: %d,countNG:%d code:%s " % (countOK, countNG, Local_Stock.code))
        list1[a].append("OK")
    return list1

def delFaultCode(listLocal):
    count = len(listLocal)
    for index1 in range(count):
        listLocal[index1] = listLocal[index1].replace("\xa0", "")
        listLocal[index1] = listLocal[index1].replace("↓", "")
        listLocal[index1] = listLocal[index1].replace("↑", "")
        listLocal[index1] = listLocal[index1].replace("\\x7", "")
        listLocal[index1] = listLocal[index1].replace("\\n", "")
    return listLocal

def delErrCode(listObj):
    cnt = 0
    perLen = len(listObj)
    while cnt < perLen:
        len2 = len(listObj[cnt])
        cnt2 = 0
        while True:
            if cnt2 > (len2-1):
                break
            if listObj[cnt][cnt2] == '':
                listObj[cnt].remove('')
                cnt2 = cnt2 -1
                len2 = len(listObj[cnt])
            cnt2 = cnt2 + 1
        if(listObj[cnt] == [0]):
            del listObj[cnt]
            perLen = len(listObj)
            cnt = cnt - 1
        cnt = cnt + 1
    return listObj

def swichMarkTo1(listObj):
    for cnt1 in range(len(listObj)):
        for cnt2 in range(len(listObj[cnt1])):
            if listObj[cnt1][cnt2] == "*":
                listObj[cnt1][cnt2] = "1"
    return listObj

def delNotUsedinfo(listObj):
    allDataLen = len(listObj)
    itm = 0
    while True:
        if listObj[itm] in POPLIST_HOLDER_TYPE:
            del listObj[itm]
            itm = itm - 1
            allDataLen = len(listObj)
        if itm < allDataLen -1 and listObj[itm] in ("国家股","其它","国有股份","国有股","香港(中央结算)代理人有限公司","内部职工股","其他","未知") and len(listObj[itm+1]) <= 3:
            del listObj[itm]
            itm = itm -1
            allDataLen = len(listObj)
        if itm == allDataLen - 1:
            break
        itm = itm + 1
    return listObj

def cutListToArrayList(countSeason,ListObj):
    global DEBUG_LOG
    countPers1 = 0
    listArrayObj = [[0] for count in range(countSeason-1)]
    for count in range(1, countSeason):
        index1 = ListObj.index("1")
        if DEBUG_LOG == 1:
            logging.info("ListObj[%d] : [%s]" %(index1+1, ListObj[index1+1]))
        if (ListObj[index1+1] > "9"):
            ListObj[index1] = ListObj[index1].replace('1',"*")
            index2 = ListObj.index("1")
            if index2 < len(ListObj)-1:
                while ListObj[index2+1] <= "9":
                    if index2 < len(ListObj) - 1:
                        countPers1 = countPers1 + 1
                        ListObj[index2] = ListObj[index2].replace('1', "*")
                        index2 = ListObj.index("1")
                        if DEBUG_LOG == 1:
                            logging.info("I count:[%d] countSeason:[%d]" % (count, countSeason))
                            logging.info("I countPers1:[%d], len:[%d]" % (countPers1, len(ListObj)))
                            logging.info("I index1:[%s],list[index1]:[%s]" % (index1, ListObj[index1]))
                            logging.info("I index2:[%s],list[index2]:[%s]" % (index2, ListObj[index2]))
                            logging.info("I listArrayObj[%d]:[%s]" % (count-1, ListObj[index1:index2]))
                            logging.info("I ListObj[index2]:[%s]" % ListObj[index2])
                        if index2 == len(ListObj)-1:
                            break
            listArrayObj[count - 1] = ListObj[index1:index2]
            if DEBUG_LOG == 1:
                logging.info("II count:%d countSeason:%d" % (count, countSeason))
                logging.info("II index1:%d, len:%d " % (index1,len(ListObj)))
                logging.info("II index2:%d, len:%d " % (index2,len(ListObj)))
                logging.info("II listArrayObj[%d]:%s" % (count-1,ListObj[index1:index2]))
                logging.info("II ListObj[%d]: %s " % (index1+1, ListObj[index1+1]))
        if DEBUG_LOG == 1:
            logging.info("III count:%d countSeason:%d" % (count, countSeason))
            logging.info("III index2:%d, len:%d " % (index2,len(ListObj)))
            logging.info("III listArrayObj[%d]:%s" % (count-1, ListObj[index1:index2]))
            logging.info("****ALL:%s **** " % ListObj)
        if count == countSeason - countPers1:
            break
    return listArrayObj

def getholderInfo(obj):
    global DEBUG_LOG
    holderinfo_orig = []
    holderinfos = obj.div.findAll("div", {"align": "center"})
    for info in holderinfos:
        holderinfo_orig.append(info.text)
# 删除异常符号
    holderinfo_orig = delFaultCode(holderinfo_orig)
#删除链表成员，多余的信息和股票种类
    if len(holderinfo_orig) == 0:
        logging.warning("holderinfo_orig is Null. Stockcode : [%s] " % Local_Stock.code)
        return False
    holderinfo_orig = delNotUsedinfo(holderinfo_orig)
    holderinfo_orig.append("1")
    countSeason = holderinfo_orig.count("1") - 1
    holderinfo_list = cutListToArrayList(countSeason, holderinfo_orig)
    if DEBUG_LOG == 1:
        for tmp in holderinfo_list:
            logging.info("tmp: %s" % tmp)
#删除链表里面''成员；
    holderinfo_list = delErrCode(holderinfo_list)
#转换链表成员from * to 1
    holderinfo_list = swichMarkTo1(holderinfo_list)
    if DEBUG_LOG == 1:
        for tmp in holderinfo_list:
            logging.info("tmp: %s" % tmp)
#检验链表长度并添加OK，NG标志
    holderinfo_list_OK_NG = dataCheck(holderinfo_list)
    if DEBUG_LOG == 1:
        for tmp2 in holderinfo_list_OK_NG:
            logging.info("tmp2: %s" % tmp2)
    return holderinfo_list_OK_NG

def updateHolderInfo(listObj,listDate):
    newestDataDB = getNewestDateDB(Local_Stock.code)
    newStockflag = 0
    if newestDataDB == None:
        newStockflag = 1
    for cnt1 in (range(len(listObj))):
        try:
            index1 = listObj[cnt1].index("OK")
            del listObj[cnt1][index1]
            len1 = len(listObj[cnt1])
            listDate[cnt1*4] = DivDate(listDate[cnt1 * 4])
            if DEBUG_LOG == 1:
                logging.info("listDate[%d] : [%s]" % (cnt1*4, listDate[cnt1*4]))
            #判断是不是新股票的数据
            if newStockflag == 1:
                insertData(listObj, listDate, len1, cnt1)
            elif listDate[cnt1*4] > newestDataDB:       #判断网站来的数据是不是原本存在的数据
                insertData(listObj, listDate, len1, cnt1)
            else:
                break
        except Exception as e:
            logging.info(e)
            break

def insertData(listObj, listDate, len1, cnt1):
    global ErrMsg
    global mutex
    global InsertStockCode
    conn = pymysql.connect(host='localhost', port='', user='root', passwd='yuanwei111', db='stockinfo', charset='utf8')
    cur = conn.cursor()
    logging.info("stockCode:[%s]insert Data: %s" % (Local_Stock.code, listObj))
    mutex.acquire()
    InsertStockCode.append(Local_Stock.code)
    mutex.release()
    date_now_time = time.localtime()
    updateTime = "%d%02d%02d" % (date_now_time.tm_year, date_now_time.tm_mon, date_now_time.tm_mday)
    for cnt2 in range(int(len1 / 4)):
        if DEBUG_LOG == 1:
            logging.info("code[%s] date[%s] num[%s] name[%s] mount[%s] per[%s] " %
                  (Local_Stock.code,
                   listDate[cnt1 * 4],
                   listObj[cnt1][cnt2 * 4],
                   listObj[cnt1][cnt2 * 4 + 1],
                   listObj[cnt1][cnt2 * 4 + 2],
                   listObj[cnt1][cnt2 * 4 + 3]))
        SQL = "insert into stockholderdetails(stockCode," \
              "holder_date," \
              "holder_date_no," \
              "holder_name," \
              "stock_mount," \
              "stock_per," \
              "updatetime) " \
              "values ('%s'," \
              "'%s'," \
              "'%s'," \
              "'%s'," \
              "'%s'," \
              "'%s'," \
              "'%s')" % \
              (
                  Local_Stock.code,
                  listDate[cnt1 * 4],
                  listObj[cnt1][cnt2 * 4],
                  listObj[cnt1][cnt2 * 4 + 1].replace("'", "''"),
                  listObj[cnt1][cnt2 * 4 + 2],
                  listObj[cnt1][cnt2 * 4 + 3],
                  updateTime
              )
        if DEBUG_LOG == 1:
            logging.info(SQL)
        try:
            mutex.acquire()
            cur.execute(SQL)
            mutex.release()
        except Exception as e:
            logging.info("SQL Exception : [%s]" % (e))
            logging.info("Err!! code[%s] date[%s] num[%s] name[%s] mount[%s] per[%s] updatetime[%s]" %
                  (
                    Local_Stock.code,
                   DivDate(listDate[cnt1 * 4]),
                   listObj[cnt1][cnt2 * 4],
                   listObj[cnt1][cnt2 * 4 + 1].replace("'", "''"),
                   listObj[cnt1][cnt2 * 4 + 2],
                   listObj[cnt1][cnt2 * 4 + 3],
                   updateTime
                  )
                  )
            mutex.acquire()
            ErrMsg.append("e:[%s] code[%s] date[%s] num[%s] name[%s] mount[%s] per[%s]" %
                          (e,
                           Local_Stock.code,
                           listDate[cnt1 * 4],
                           listObj[cnt1][cnt2 * 4],
                           listObj[cnt1][cnt2 * 4 + 1].replace("'", "''"),
                           listObj[cnt1][cnt2 * 4 + 2],
                           listObj[cnt1][cnt2 * 4 + 3])
                          )
            mutex.release()
            conn.rollback()
            return
    conn.commit()
    return


def startReadAndExc(BaseFilePath = BASE_FILEPATH):
    global g_StockCodesAll
    global mutex
    while len(g_StockCodesAll) > 0:
        mutex.acquire()
        stockcode = g_StockCodesAll.pop()
        mutex.release()
        stockcode = str(stockcode).zfill(6)
        Local_Stock.code = stockcode
        FileFullPath = BaseFilePath + stockcode + ".txt"
        fileInfo = ReadFile(FileFullPath)
        if fileInfo == False:
            logging.error("ReadFile Error: [%s]" % (FileFullPath))
            return False
        obj = transToBS_stockBasic(fileInfo)
        holderinfo_list = getholderInfo(obj)
        if holderinfo_list == False:
            continue
        result = getHolderNum(fileInfo)
        # insert the HolderInfo data
        nRet = updateHolderInfo(holderinfo_list, result)

def AddStockholderDetailsRun():
    global g_StockCodesAll
    record_thread = []
    time_start = time.time()
    g_StockCodesAll = GetAllStockCodes()
    logging.info("Stock_sum:[%s]" % g_StockCodesAll)
    for k in range(THREAD_NUM):
        new_thread = threading.Thread(target=startReadAndExc)
        new_thread.start()
        record_thread.append(new_thread)
    for thread in record_thread:
        thread.join()
    logging.info("InsertStockCode: [%s] " % InsertStockCode)
    logging.info("All time : [%d]" % (time.time() - time_start))
    for em in ErrMsg:
        logging.info("ErrMsg:[%s]" % em)

if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', port='', user='root', passwd='yuanwei111', db='stockinfo', charset='utf8')
    cur = conn.cursor()
    record_thread = []
    time_start = time.time()
    g_StockCodesAll = GetAllStockCodes()
    logging.info("Stock_sum:", g_StockCodesAll)
    for k in range(THREAD_NUM):
        new_thread = threading.Thread(target=startReadAndExc)
        new_thread.start()
        record_thread.append(new_thread)
    for thread in record_thread:
        thread.join()
    logging.info("InsertStockCode: [%s] " % InsertStockCode)
    logging.info("All time : [%d]" % (time.time() - time_start))
    for em in ErrMsg:
        logging.info("ErrMsg:[%s]" % em)
