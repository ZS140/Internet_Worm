# Internet_Worm

### 一、爬取股票网页数据
  #### 1、创建爬虫工作线程：
    a、创建一个判断是否处于交易时间的函数，使用urllib.request模块读取网页信息
    b、使用BeautifulSoup模块对获取的网页信息进行解析提取
    c、创建一个判断数据是否更新的函数：使用md5模块对数据进行加密保存，通过判断加密值是否相同进行判断
    d、通过re模块对数据进行过滤，去除多余数据，使用datetime模块转换时间格式
    e、新建一个mysql数据库
    f、新建一个使用数据库的模块，创建存储数据的函数：使用pycharm连接数据库，创建游标执行SQL语句存入数据
  #### 2、创建爬虫控制线程：
     使用while循环读取键盘输入，设置爬虫执行时间间隔和是否终止
  #### 3、创建主函数，启动线程
### 二、根据数据库数创建图表
  #### 1、创建折线图表
     a、引入matplotlib.pyplot模块
     b、设置图表大小：plt.figure(figsize=(10, 5))
     c、获取数据生成数据列表：x,y
     d、设置x,y轴标题： plt.xlabel('时间')   plt.ylabel('股价（元）')
     e、设置折线参数： plt.plot(x,y,'r',label='成交金额',linewidth='2')
     f、设置图例：plt.legend()
     g、设置标题：plt.title('股票代码：{0}近三个月历史记录'.format(symbol))
     h、保存图表：plt.savefig('股票折线图.png')
     i、显示图表：plt.show()
  #### 2、创建股票K线图
     a、引入mpl_finance、matplotlib.pyplot、matplotlib.dates模块
     b、获取数据库数据，使用matplotlib.dates模块的date2num方法将数据转换为candlestick_ohlc方法可用的类型
     c、创建子图，返回图表对象和坐标对象：fig,ax = plt.subplots(figsize = (10,5))
     d、调整子图参数，设置图表到底部的距离：fig.subplots_adjust(bottom = 0.2)
     e、设置x,y轴标题
     f、给mpl_finance模块的candlestick_ohlc()方法设置参数，进行数据分析：mpl.candlestick_ohlc(ax,new_data,width=1.0,colorup='r',colordown='g')
     g、将坐标横轴设为日期类型：ax.xaxis_date()
     h、将图表横轴坐标刻度旋转45度：plt.xticks(rotation=45)
     i、保存图表
     j、显示图表
