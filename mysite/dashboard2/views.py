from django.shortcuts import render
from django.http import HttpResponse
import sqlite3
# import requests
import json
# import hashlib
# import arrow
# import random
# HttpResponseRedirect
# from django.urls import reverse
# from django.views import generic


def index(request):
    stock_list = []
    stock_json = read_json_file("stock_list.json")
    if isinstance(stock_json, list):
        stock_list = stock_json
    # stock = {"name": "浦发银行", "code": 60000}
    # stock_list.append(stock)
    template = 'dashboard2/index.html'
    context = {'stock_list': stock_list}
    return render(request, template, context)

def detail(request, stock_code):
    stock_json = read_json_file("stock_list.json")
    stocks = {}
    if isinstance(stock_json, list):
        for item in stock_json:
            stocks[item['code']] = item['name']
    if stock_code in stocks.keys():
        stock_name = stocks[stock_code]
    else:
        stock_name = ""
    return render(request, 'dashboard2/detail.html', {'stock_name': stock_name, "stock_code": stock_code})

def stock_info_api(request):
    machine_list = []
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    print("Opened database successfully")
    cursor = c.execute("SELECT stockCode, stockDate from daydata LIMIT 10")
    for row in cursor:
        # print(row)
        machine_list.append(row)
    print("Operation done successfully")
    conn.close()
    return HttpResponse(json.dumps(machine_list))

def read_json_file(path):
    #######################
    # read JSON file
    #######################
    json_string = ""
    file_error = False
    try:
        jfile = open(path, "r", encoding='utf-8')
        lines = jfile.readlines()
    except IOError as err:
        print('read_json_file: ' + str(err))
        file_error = True
    else:
        for line in lines:
            json_string = json_string + line.strip()
        # allow comma in the last line
        json_string = json_string.replace(',}', '}')
    finally:
        if 'jfile' in locals():
            jfile.close()

    if file_error:
        return None

    try:
        jsonObject = json.loads(json_string)
    except Exception as e:
        jsonObject = None
        logger.error('read_json_file: ' + str(e))

    return jsonObject
