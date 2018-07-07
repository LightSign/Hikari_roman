# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for , make_response,Response
from datetime import datetime,timedelta
import subprocess
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime,timedelta
from time import sleep
import re
import random
import codecs
import csv
import io as cStringIO

app = Flask(__name__)

@app.route("/")
def root():
    return Response("<a href='/dl/'>Download now</a>")


@app.route("/dl/")
def make_csv():
    """
    CSV 出力
    """
    print("make csv")
    response = make_response()
    response.data = _get_csv_data()
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=sample.csv'
    return response


def _get_csv_data():
    """
    CSV データ作成
    """
    data = _make_data()
    csv_file = _make_file(data)
    return csv_file


def _make_data():
    """
    書き込みデータ作成
    """
    browser = webdriver.Chrome()
    df = pd.DataFrame(index=[] , columns=[])
    date = datetime.today().strftime("%Y%m%d_")
    browser.get("https://www.mercari.com/jp/search/?keyword=iPhone+SE+SIM%E3%83%95%E3%83%AA%E3%83%BC")
    posts = browser.find_elements_by_css_selector(".items-box")
    for post in posts:
        title = post.find_element_by_css_selector("h3.items-box-name").text
        price = post.find_element_by_css_selector(".items-box-price").text
        price = price.replace('¥', '').replace(",","")
        sold = 0
        if len(post.find_elements_by_css_selector(".item-sold-out-badge")) > 0:
            sold = 1
        url = post.find_element_by_css_selector("a").get_attribute("href")
        se = pd.Series([title, price, sold,url],['title','price','sold','url'])
        df = df.append(se, ignore_index=True)
    df = df.astype("str")
    print(type(df))
    print("return df")
    # df = pd.DataFrame({ 'A' : 1.,
    #                         'B' : pd.Timestamp('20130102'),
    #                         'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
    #                         'D' : np.array([3] * 4,dtype='int32'),
    #                         'E' : pd.Categorical(["test","train","test","train"]),
    #                         'F' : 'foo' })
    return df
    print("finish df")
def _make_file(data):
    """
    データを CSV 形式に変換
    """
    print("convert to csc")
    csv_file = cStringIO.StringIO()
    writer = csv.writer(csv_file, quoting=csv.QUOTE_NONE, delimiter=',', quotechar='')
    writer.writerow(data)
    writer.writerows(data.values)
    return csv_file.getvalue()


if __name__ == '__main__':
    app.run(debug=True)
