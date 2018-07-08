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
from bs4 import BeautifulSoup as bs
import requests
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
    title = "ATOM : 実行ページ"
    return render_template('index.html',title=title)

#/post にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def _make_data():
    title = "ATOM : 結果ページ"
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
        # site = "https://www.mercari.com/jp/search/?keyword=iPhone+SE+SIM%E3%83%95%E3%83%AA%E3%83%BC"
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",}
        df = pd.DataFrame(index=[] , columns=[])
        req = requests.get(URL ,headers=headers)
        all_html = bs(req.content,"lxml")
        posts = all_html.select(".items-box")

        for post in posts:
            title = post.select("h3.items-box-name")[0].getText()
            price = post.select(".items-box-price")[0].getText()
            price = price.replace('¥', '').replace(",","")
            sold = 0
            if len(post.select(".item-sold-out-badge")) > 0:
                sold = 1
            url = post.a.get("href")
            se = pd.Series([title, price, sold,url],['title','price','sold','url'])
            df = df.append(se, ignore_index=True)
        df["title"] = df["title"].str.replace(r"\W"," ")
        # browser.close()

        def _make_file(data):
            """
            データを CSV 形式に変換
            """
            print("make file")
            csv_file = cStringIO.StringIO()
            writer = csv.writer(csv_file, quoting=csv.QUOTE_NONE, delimiter=',', quotechar=',')
            writer.writerow(data)
            writer.writerows(data.values)
            return csv_file.getvalue()

        def make_csv(file_csv):
            """
            CSV 出力
            """
            print("make csv")
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
