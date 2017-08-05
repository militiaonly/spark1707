from sqlalchemy import create_engine
import tushare as ts
import pymysql
import arrow
import os
import logging
import logging.config
import fileutil

abspath = os.path.abspath(__file__)
dirname = os.path.dirname(abspath)
logging.config.fileConfig(dirname + '/logging.conf')
# root
logger_root = logging.getLogger('root')
# mysql
logger_wrtnode = logging.getLogger('mysql2')
# mysql.__name__
logger = logging.getLogger('mysql2.' + __name__)


# mysql config
MySQLConfig = {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "example",
    "db": "spark17",
    "charset": "utf8"
}


# df = ts.get_tick_data('600000', date='2014-12-22')
# df = ts.get_k_data('600000', ktype='5', start='2016-01-01', end='2016-12-31')
# df = ts.get_stock_basics()

# df = ts.get_k_data('600000', ktype='D', start='2000-01-01', end='2016-12-31')
# engine = create_engine('mysql+pymysql://root:example@127.0.0.1/spark17?charset=utf8')

# 存入数据库
# df.to_sql('day_data', engine, schema='spark17', if_exists='append')

# 追加数据到现有表
# df.to_sql('tick_data',engine,if_exists='append')

# ---------------------------------------------------------------------------------------
# get stock list from mysql
mysqlp = MySQLConfig
dbconn = None
count = 0
# Connect to the database
if dbconn is None:
    try:
        dbconn = pymysql.connect(host=mysqlp['host'],
                                 port=mysqlp['port'],
                                 user=mysqlp['username'],
                                 password=mysqlp['password'],
                                 db=mysqlp['db'],
                                 charset=mysqlp['charset'],
                                 cursorclass=pymysql.cursors.DictCursor)
    except Exception as e:
        logger.error(e)

try:
    with dbconn.cursor() as cursor:
        # Read records
        sql = "SELECT `code`, `name` FROM `stock_basics`"
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        count = len(results)
        print("len(results)=%d" % count)
        # print(results[0])
        # {'code': '603063'}
finally:
    # pass
    dbconn.close()

# save history day data to mysql
engine = create_engine('mysql+pymysql://root:example@127.0.0.1/spark17?charset=utf8')
t1 = arrow.utcnow().float_timestamp

completed_stocks = []
i = 0
for r in results:
    # read json to get the last completed stocks list
    # skip if already exists
    jsonObject = fileutil.read_json_file('completed_stocks.json')
    for stock in jsonObject:
        if stock['code'] == r['code']:
            i += 1
            continue

    # get data from remote
    try:
        df = ts.get_k_data(r['code'], ktype='D', start='2001-01-01', end='2017-07-31')
    except Exception as e:
        info = r['code'] + ' ' + str(e)
        logger.error(info)
        # bypass the below procedures
        i += 1
        continue

    # 存入数据库
    try:
        df.to_sql('day_data', engine, schema='spark17', if_exists='append')
    except Exception as e:
        info = r['code'] + ' ' + str(e)
        logger.error(info)
    else:
        t2 = arrow.utcnow().float_timestamp
        delta_t = t2 - t1
        info = "%.2f%% %d/%d %s %s saved! Elapsed time: %.3f seconds" % (
            i * 100 / count, i, count, r['code'], r['name'], delta_t)
        logger.info(info)
        completed_stocks.append(r)
        # json to file needed
        fileutil.write_json_file('completed_stocks.json', completed_stocks)
    finally:
        i += 1

print('%d stocks are saved in %.3f seconds!' % (len(results), delta_t))
