import pymysql
import arrow
import os
import logging
import logging.config
import fileutil
import struct

abspath = os.path.abspath(__file__)
dirname = os.path.dirname(abspath)
logging.config.fileConfig(dirname + '/logging.conf')
# root
logger_root = logging.getLogger('root')
# mysql
logger_wrtnode = logging.getLogger('mysql2')
# mysql.__name__
logger = logging.getLogger('mysql2.' + __name__)

stockId = '600000'

# mysql config
MySQLConfig = {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "example",
    "db": "spark17",
    "charset": "utf8"
}

mysqlp = MySQLConfig
dbconn = None
count = 0
if 0:
    t1 = arrow.utcnow().float_timestamp
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
            sql = "SELECT `code` FROM `stock_basics`"
            print(sql)
            cursor.execute(sql)
            results0 = cursor.fetchall()
            # cursor.close()
            count = len(results0)
            print("len(results0)=%d" % count)
            # print(results0)
    finally:
        fileutil.write_json_file('stock_codes.json', results0)

    for stockCode in results0:
        stockId = stockCode['code']
        try:
            with dbconn.cursor() as cursor:
                # Read records
                sql = "SELECT * FROM `day_data` WHERE `code`='%s'" % stockId
                print(sql)
                cursor.execute(sql)
                results = cursor.fetchall()
                # cursor.close()
                count = len(results)
                print("len(results)=%d" % count)
                # print(results)
        finally:
            pass
            # dbconn.close()
        t2 = arrow.utcnow().float_timestamp
        delta_t = t2 - t1
        info = 'time cost read from MySQL %.3f seconds' % delta_t
        logger.info(info)
        # save StockId and its record number
        jsonObject = fileutil.read_json_file('stock_matrix.json')
        # update the count
        jsonObject[stockId] = count
        # save
        fileutil.write_json_file('stock_matrix.json', jsonObject)

        # write to rawB
        t1 = arrow.utcnow().float_timestamp
        # start date
        s = arrow.get('2001-01-01')
        ba = b''
        for r in results:
            d = arrow.get(r['date'])
            a = [0] * 10
            a[0] = (d - s).days
            a[1] = int(r['open'] * 100)
            a[2] = int(r['high'] * 100)
            a[3] = int(r['low'] * 100)
            a[4] = int(r['close'] * 100)
            a[5] = int(r['volume'] / 100000)
            stockbytes = struct.pack('6H', a[0], a[1], a[2], a[3], a[4], a[5])
            ba += stockbytes

        # write to file
        try:
            path = 'rawb_files/rawB' + stockId
            config_file = open(path, "wb")
            config_file.write(ba)
        except IOError as err:
            errorStr = 'File Error:' + str(err)
            logger.error(errorStr)
        else:
            logger.info('write %s completed' % stockId)
        finally:
            if 'config_file' in locals():
                config_file.close()
        t2 = arrow.utcnow().float_timestamp
        delta_t = t2 - t1
        info = 'time cost write to rawB %.3f seconds' % delta_t
        logger.info(info)

# read from rawB
if 0:
    t1 = arrow.utcnow().float_timestamp
    file_error = False
    try:
        path = 'rawb_files/rawB' + stockId
        jfile = open(path, "rb")
        rawB = jfile.read()
    except IOError as err:
        logger.error('read_txt_file: ' + str(err))
        file_error = True
    finally:
        if 'jfile' in locals():
            jfile.close()

    if not file_error:
        jsonObject = fileutil.read_json_file('stock_matrix.json')
        if stockId in jsonObject:
            records_count = jsonObject[stockId]
            fmt = '%dH' % 6 * records_count
            r = struct.unpack(fmt, rawB)
            # print(r)
    t2 = arrow.utcnow().float_timestamp
    delta_t = t2 - t1
    info = 'time cost read from rawB %.3f seconds' % delta_t
    logger.info(info)
