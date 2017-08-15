#!/usr/bin/env python
# -*- encoding=utf-8 -*-

########################################################
# DataSave Class to save daily curves and 5-min curves #
########################################################

import os
import time
import threading
import json
import sqlite3
# import arrow
# import datetime
# import fileutil
import struct
# from pytz import utc
# from apscheduler.schedulers.background import BackgroundScheduler

abspath = os.path.abspath(__file__)
dirname = os.path.dirname(abspath)

# datetime.datetime(2016, 1, 1, tzinfo=datetime.timezone.utc).timestamp()
TS_2016_UTC = 1451606400.0
DAILY_PATH = "C:\\Users\\Shaohua\\Documents\\export\\daily-qfq-20130304-20170814"
FIVE_MIN_PATH = "C:\\Users\\Shaohua\\Documents\\export\\5-min-20170502-20170814"


class DataSave(threading.Thread):
    """
    @brief      DataSave Class to save daily curves and 5-min curves
    """

    def __init__(self):
        super(DataSave, self).__init__()
        self._stop = threading.Event()
        self._stop.clear()
        print(DAILY_PATH)
        print(FIVE_MIN_PATH)

    def run(self):
        # self.create_5m_table()
        self.save_5m()
        while not self._stop.is_set():
            time.sleep(1)
            self.stop()

    def stop(self):
        self._stop.set()

    def save_5m(self):
        five_min_files = os.listdir(FIVE_MIN_PATH)
        print(len(five_min_files))
        for five_min_file in five_min_files:
            print(five_min_file)
            filePath = FIVE_MIN_PATH + "\\" + five_min_file
            self.save_5m_file(filePath)

    def save_5m_file(self, filePath):
        stockCode = filePath[:len(filePath) - 4]
        stockCode = stockCode.split("#")[1]
        stockCodeInt = int(stockCode)
        try:
            jfile = open(filePath, "r")
            lines = jfile.readlines()
        except IOError as err:
            print('read file: ' + str(err))
        else:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            for line in lines:
                print(line.strip())
                stockDate = '2017-01-01 09:45'
                stockOpen = 1.00
                stockHigh = 1.02
                stockLow = 0.99
                stockClose = 1.01
                stockVol = 1112212.00
                stockAmount = 1256895.00
                sql1 = 'INSERT INTO "main"."daydata5m" ("stockCode", "stockDate", "stockOpen", "stockHigh", "stockLow", "stockClose", "stockVol", "stockAmount")'
                sql2 = "VALUES ('%d', '%s', '%.2f', '%.2f', '%.2f', '%.2f', '%.2f', '%.2f');" % (stockCodeInt, stockDate, stockOpen, stockHigh, stockLow, stockClose, stockVol, stockAmount)
                c.execute(sql1 + " " + sql2)
                break
            conn.commit()
            conn.close()
        finally:
            if 'jfile' in locals():
                jfile.close()

    def create_5m_table(self):
        conn = sqlite3.connect('stock.db')
        print("Opened database successfully")
        c = conn.cursor()
        # stockCode,stockDate,stockOpen,stockHigh,stockLow,stockClose,stockVol,stockAmount
        c.execute("PRAGMA foreign_keys = false;")
        c.execute('''DROP TABLE IF EXISTS "daydata5m";''')
        c.execute('''
        CREATE TABLE "daydata5m" (
        "ID" integer NOT NULL,
        "stockCode" integer NOT NULL,
        "stockDate" text NOT NULL,
        "stockOpen" real,
        "stockHigh" real,
        "stockLow" real,
        "stockClose" real,
        "stockVol" real,
        "stockAmount" real,
        PRIMARY KEY ("ID")
        );''')
        c.execute("PRAGMA foreign_keys = true;")
        conn.commit()
        print("Table created successfully")
        conn.close()


if __name__ == '__main__':
    da = DataSave()
    da.start()
    da.join()
