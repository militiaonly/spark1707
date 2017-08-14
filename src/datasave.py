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
        # self.save_5m()
        self.create_5m_table()
        while not self._stop.is_set():
            time.sleep(1)

    def stop(self):
        self._stop.set()

    def save_5m(self):
        five_min_files = os.listdir(FIVE_MIN_PATH)
        print(len(five_min_files))
        for five_min_file in five_min_files:
            print(five_min_file)
    
    def create_5m_table(self):
        conn = sqlite3.connect('stock.db')
        print("Opened database successfully")
        c = conn.cursor()
        # stockCode,stockDate,stockOpen,stockHigh,stockLow,stockClose,stockVol,stockAmount
        c.execute('''CREATE TABLE COMPANY
            (ID INT PRIMARY KEY     NOT NULL,
            stockCode CHAR(20)      NOT NULL,
            stockDate DATETIME      NOT NULL,
            stockOpen REAL,
            stockHigh REAL,
            stockLow REAL,
            stockClose REAL,
            stockVol REAL,
            stockAmount REAL
            );''')
        print("Table created successfully")
        conn.commit()
        conn.close()

if __name__ == '__main__':
    da = DataSave()
    da.start()
    da.join()
