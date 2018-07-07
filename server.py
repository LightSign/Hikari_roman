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

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)
CORS(app)

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    title = "神ツール : 実行ページ"
    return render_template('index.html',title=title)

#/post にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def _make_data():
    title = "神ツール : 結果ページ"
    if request.method == 'POST':
        # リクエストフォームから「名前」を取得して
        # ebay_id = request.form['ebay_id']
        # ebay_pass = request.form['ebay_pass']
        # query = request.form['search_keyword']
        # price_min = int(request.form['price_lower'])
        # price_max = int(request.form['price_upper'])
        # search_weight = request.form['search_weight']
        # tmp1 = request.form['tmp1']
        # tmp2 = request.form['tmp2']
        # tmp3 = request.form['tmp3']
        URL = request.form['URL']

        """
        書き込みデータ作成
        """
        # make data

        options = Options()
        ### for local pc
        # options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        options.binary_location = '/app/.apt/usr/bin/google-chrome'
        # options.add_argument('--disable-gpu')
        # options.add_argument("--no-sandbox")
        # options.add_argument('headless')
        # options.add_argument('window-size=1200x600')
        # browser = webdriver.Chrome(chrome_options=options)
        browser = webdriver.Chrome(chrome_options=options)
        browser.implicitly_wait(20)

        df = pd.DataFrame(index=[] , columns=[])
        date = datetime.today().strftime("%Y%m%d_")
        browser.get(URL)
        #browser.get("https://www.mercari.com/jp/search/?sort_order=&keyword={0}&category_root=&brand_name=&brand_id=&size_group=&price_min={1}&price_max={2}".format(query,price_min,price_max))
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

        def _make_file(data):
            """
            データを CSV 形式に変換
            """
            csv_file = cStringIO.StringIO()
            writer = csv.writer(csv_file, quoting=csv.QUOTE_NONE, delimiter=',', quotechar='')
            writer.writerow(data)
            writer.writerows(data.values)
            return csv_file.getvalue()

        def make_csv(file_csv):
            """
            CSV 出力
            """
            response = make_response()
            response.data = file_csv
            response.headers['Content-Type'] = 'application/octet-stream'
            response.headers['Content-Disposition'] = 'attachment; filename=ATOM_test.csv'
            return response

        file_csv = _make_file(df)
        csv_data = make_csv(file_csv)
        return csv_data
    else:
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0') # どこからでもアクセス可能に
