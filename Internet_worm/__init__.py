import hashlib
import threading
import urllib.request
import os
from datetime import datetime
import time
import re
import logging
from bs4 import BeautifulSoup
from Internet_worm import nasdaq_mysql

url = 'https://www.nasdaq.com/symbol/aapl/historical#.UWdnJBDMhHk'
old_md = ''
isrunning = True
sleep_time = 5
#自定义日志对象
logging.basicConfig(level=logging.DEBUG,format='%(threadName)s-%(asctime)s-%(message)s')
logger = logging.getLogger()

#判断是否处于交易时间，交易时间不获取数据
def istrade():
    now = datetime.now()
    now_str = datetime.strftime(now,'%H%M%S')
    start_time = '093000'
    end_time = '153000'
    if now.weekday() == 5 or now.weekday() == 6 or (start_time > now_str or end_time < now_str):
        # logger.info("处于非交易时间")
        return False
    else:
        logger.info("正处于交易时间")
        nasdaq_mysql.getData()
        return True
#判断数据是否更新的函数
def validataUpdate(divstr):
    global old_md

    #创建MD5对象
    m = hashlib.md5()
    m.update(divstr.encode(encoding='utf-8'))
    new_md = m.hexdigest()

    if os.path.exists('md5.txt'):
        with open('md5.txt','r') as r:
            old_md = r.read()
    else:
        with open('md5.txt', 'w') as w:
            w.write(new_md)
    if new_md == old_md:
        # print("数据未更新,md5:{0}".format(new_md))
        return False
    else:
        # print('数据更新了,md5:{0}'.format(new_md))
        with open('md5.txt', 'w') as w:
            w.write(new_md)
        return True
#获取网页信息函数
def get_data(htmlstr):
    bs = BeautifulSoup(htmlstr,'html.parser')
    div = bs.select('div#quotes_content_left_pnlAJAX')

    if validataUpdate(div[0]):#检测更新
        tbody = bs.select('#quotes_content_left_pnlAJAX table tbody tr')
        data = []
        for i in tbody:
            field = {}
            data_str = i.text.strip()
            if data_str == '':
                continue
            row =re.split(r'\s+',data_str)

            try: #因为交易时间当天日期不是月/日/年格式，会产生时间转换异常
                field['Date'] = datetime.strptime(row[0],'%m/%d/%Y')
                field['Open'] = float(row[1])
                field['High'] = float(row[2])
                field['Low'] = float(row[3])
                field['Close'] = float(row[4])
                field['Volume'] = float(row[5].replace(',', ""))
                field['Symbol'] = 'APPL'
                data.append(field)
            except ValueError:
                pass
        #存入新数据前删除旧数据
        nasdaq_mysql.delData()
        for row in data:
            count = nasdaq_mysql.putData(row)
            # print("影响{0}行数据".format(count))


#爬虫工作线程体
def Work():
    global isrunning,sleep_time
    while isrunning:
        if istrade():#如果处于交易时间则不获取数据
            time.sleep(60 * 60)
            continue
        logger.info('爬虫工作...')
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode()
            get_data(html)
        logger.info("爬虫工作间隔{0}秒".format(sleep_time))
        time.sleep(sleep_time)#爬虫执行间隔时间

#爬虫控制线程体
def Control():
    global isrunning, sleep_time
    while isrunning:
        if istrade():
            logger.info("交易时间,爬虫处于休眠状态...")
            time.sleep(60*60)
            continue

        i = input("爬虫执行间隔时间，单位：秒\n")
        try:
            sleep_time = int(i)
        except ValueError:
            if i.lower() == 'bye':
                logger.info("结束...")
                isrunning = False
#主函数
def main():
    workthread = threading.Thread(target=Work, name='WorkThread')
    workthread.start()
    controlthread = threading.Thread(target=Control, name='ControlThread')
    controlthread.start()

if __name__ == '__main__':
   main()

