# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for , make_response,Response
from flask_cors import CORS, cross_origin
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
    return Response("<a href='/dl/'>DL</a>")


@app.route("/dl/")
def make_csv():
    """
    CSV 出力
    """
    response = make_response()
    response.data = _get_csv_data()
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = u'attachment; filename=データ.csv'
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
    options = Options()
    ### for local pc
    options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
    #options.binary_location = '/app/.apt/usr/bin/google-chrome'
    options.add_argument('--disable-gpu')
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')
    options.add_argument('window-size=1200x600')
    browser = webdriver.Chrome(chrome_options=options)

    browser.get("http://www.qq.pref.ehime.jp/qq38/qqport/kenmintop/")
    driver.find_element_by_css_selector("div.group2 > input.each-menu-citizen__button-hover").click()
    driver.find_element_by_id("id_blockCd000004").click()
    driver.find_element_by_name("forward_next").click()
    html = driver.page_source
    print()
    driver.quit()
    return df


def _make_file(data):
    """
    データを CSV 形式に変換
    """
    csv_file = cStringIO.StringIO()
    writer = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerows(data)
    writer.writerows(data.values)
    return csv_file.getvalue()


if __name__ == '__main__':
    app.run(debug=True)
