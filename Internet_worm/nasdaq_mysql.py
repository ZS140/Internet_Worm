import pymysql

def putData(row):
    #连接数据库
    connection = pymysql.connect(host='localhost',user='root',passwd='1402929679zs',db='test',charset='utf8')

    #创建游标
    try:
        with connection.cursor() as cursor:
            #插入数据
            sql = 'insert into nasdaq_data' \
                  '(Date,Open ,High,Low,Close ,Volume,Symbol)' \
                  ' VALUES(%(Date)s,%(Open)s,%(High)s,%(Low)s,%(Close)s,%(Volume)s,%(Symbol)s)'
            count = cursor.execute(sql,row)
            connection.commit()
        return count
    except pymysql.DatabaseError as e:
        connection.rollback()
        print(e)
    finally:
        connection.close()

def getData(symbol):
    #连接数据库
    connection = pymysql.connect(host='localhost',user='root',passwd='1402929679zs',db='test',charset='utf8')

    #创建游标
    try:
        with connection.cursor() as cursor:
            sql = 'select * from nasdaq_data WHERE Symbol = %s'
            cursor.execute(sql,[symbol])
            data = cursor.fetchall()
            return data
    except pymysql.DatabaseError as e:
        print(e)
        return []
    finally:
        connection.close()
def delData():
    # 连接数据库
    connection = pymysql.connect(host='localhost', user='root', passwd='1402929679zs', db='test', charset='utf8')

    # 创建游标
    try:
        with connection.cursor() as cursor:
            sql = 'delete from nasdaq_data'
            cursor.execute(sql)
            connection.commit()
    except pymysql.DatabaseError as e:
        connection.rollback()
        print(e)
    finally:
        connection.close()
