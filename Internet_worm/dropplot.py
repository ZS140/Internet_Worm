from datetime import datetime

import matplotlib.pyplot as plt
from Internet_worm import nasdaq_mysql
import mpl_finance as mpl
from matplotlib.pylab import date2num
import matplotlib.dates as mdata

# 设置字体
plt.rcParams['font.family'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

#生成图表
def drop(symbol):
    #设置图表大小
    plt.figure(figsize=(10, 5))
    #获取数据库数据
    data = nasdaq_mysql.getData(symbol)
    x = []
    y = []
    open = []
    high = []
    low = []
    close = []
    for row in data:
        x.append(row[0])
        open.append(row[1])
        high.append(row[2])
        low.append(row[3])
        close.append(row[4])
        y.append(row[5])
    #x,y轴标题
    plt.xlabel('时间')
    plt.ylabel('股价（元）')
    #绘制折线
    # plt.plot(x,y,'r',label='成交金额',linewidth='2')
    plt.plot(x,open,'b',label='Open', linewidth='2')
    plt.plot(x,high,'m',label='high', linewidth='2')
    plt.plot(x,low,'g',label='low', linewidth='2')
    plt.plot(x, close, 'y', label='close', linewidth='2')
    #设置图例
    plt.legend()
    #图表标题
    plt.title('股票代码：{0}近三个月历史记录'.format(symbol))
    plt.savefig('股票折线图.png')
    plt.show()
#绘制K线图
def drop_k(symbol):
    #获取数据，并将日期类型转换为matplotlib日期
    data = nasdaq_mysql.getData(symbol)
    new_data = []
    for row in data:
        row = list(row)
        row[0] = mdata.date2num(datetime.strptime(str(row[0]),"%Y-%m-%d"))
        new_data.append(row)


    #创建子图,得到一个二元组，图表对象和坐标轴对象
    fig,ax = plt.subplots(figsize = (10,5))
    #调整子图参数，bottom是设置图表到底部的距离
    fig.subplots_adjust(bottom = 0.2)

    plt.ylabel('股价（元）')
    plt.xlabel('时间')
    plt.title('股票代码：{0}近三个月历史记录'.format(symbol))
    mpl.candlestick_ohlc(ax,new_data,width=1.0,colorup='r',colordown='g')
    #设置坐标轴属性
    ax.xaxis_date() #日期类型
    plt.xticks(rotation=45)#显示刻度值旋转45度
    plt.savefig('股票K线图.png')
    plt.show()

if __name__ == '__main__':
    drop('APPL')
    drop_k('APPL')
