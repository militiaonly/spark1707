from django.shortcuts import render
from django.http import HttpResponse, Http404
import sqlite3
import json
import arrow
# import hashlib
# import requests
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
        data_points = get_stock_daydata(stock_code)
        json_data = {}
        json_data['stock_name'] = stock_name
        json_data['stock_code'] = stock_code
        json_data['data_points'] = data_points
        json_data_str = json.dumps(json_data, 'utf-8')
        # print(json_data_str)
        return render(request, 'dashboard2/detail.html', {'json_data_str': json_data_str})
    else:
        raise Http404("Stock code does not exist")


def stock_info_api(request):
    raise Http404("Stock code does not exist")


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
        print('read_json_file: ' + str(e))

    return jsonObject


def get_stock_daydata(stock_code):
    data_points = []
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    sql = "SELECT * FROM daydata WHERE stockCode=%d ORDER BY ID DESC LIMIT 0, 3000" % int(stock_code)
    cursor = c.execute(sql)
    for row in cursor:
        # print(row)
        data_point = {}
        data_point['x'] = arrow.get(row[2]).format("YYYY-MM-DD")
        # data_point['x'] = arrow.get(row[2]).datetime
        # open / high / low / close
        data_point['y'] = [row[3], row[4], row[5], row[6]]
        data_points.append(data_point)
    conn.close()
    # print(data_points)
    return data_points
