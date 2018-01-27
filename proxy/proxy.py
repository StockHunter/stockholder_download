from urllib import request
import datetime
import random
import time
import re
import os
import codecs

proxy_list_all = []
proxy_list_ok = []
path = ""
file = ""

def get_proxy_web(page):
    global proxy_list_all
    for i in range(1, page):
        print("i = %d" % i)
        url = r'http://www.xicidaili.com/nn/{}'.format(i)
        headers = {
            'User-Agent':r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        print("url:" + url)
        req = request.Request(url, headers=headers)
        html = request.urlopen(req).read()
        html = html.decode('utf-8')
        get_AllProxy(html)
        proxy_check()
        writefile(proxy_list_ok)

def get_AllProxy(html):
    global proxy_list_all
    proxy_list_all = []
    ip_port_list = re.findall(r'<tr class.*?>(.*?)</tr>', html, re.S)
    for i in ip_port_list:
        ip = re.findall(r'\d+\.\d+\.\d+\.\d+', i)[0]
        if ip == '':
            print("no data ! exit!")
            return
        port = re.findall(r'<td>(\d+)</td>', i)[0]
        proxy = '{}:{}'.format(ip, port)
        proxy_list_all.append(proxy)
    print(proxy_list_all)

def proxy_check():
    global proxy_list_ok
    for proxy_i in proxy_list_all:
        sleep_time = random.random()
        print("sleep:{}s ip:{}".format(sleep_time,proxy_i))
        time.sleep(sleep_time)
        proxy_suport = request.ProxyHandler({'http':proxy_i})
        opener = request.build_opener(proxy_suport)
        try:
            r = opener.open("http://www.baidu.com", timeout=2)
            proxy_list_ok.append(proxy_i)
        except Exception as ep:
            print("error! delete:{}, len:{}".format(proxy_i, len(proxy_list_all)))
            print(ep)
    print("proxy_OK :%s " % proxy_list_ok)

def writefile(info):
    global path
    global file
    path1 = os.path.split(os.path.realpath(__file__))[0]
    today = datetime.date.today()
    info1 = '/{}{}{}'.format(today.year, today.month, today.day)
    path = path1+info1+".txt"
    f = codecs.open(path, 'a', 'utf-8')
    for info2 in info:
        f.write(str(info2)+',')
    f.close()
    print(path)

def get_proxy_file():
    global file
    global path
    path1 = os.path.split(os.path.realpath(__file__))[0]
    today = datetime.date.today()
    info1 = '/{}{}{}'.format(today.year, today.month, today.day)
    path = path1+info1+".txt"
    f = codecs.open(path, 'r', 'utf-8')
    proxy = f.read()
    proxy = proxy.split(",")
    proxy.pop()
    print(proxy)
    return proxy

def get_proxy(page):
    get_proxy_web(page+1)
    return get_proxy_file()


if __name__ == '__main__':
    page = 1
    get_proxy_web(page+1)
    listProxy = get_proxy_file()
