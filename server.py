# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for , make_response,Response
from flask_cors import CORS, cross_origin
from datetime import datetime
from processing import processing

app = Flask(__name__)
CORS(app)

# index にアクセスしたときの処理
@app.route('/')
def index():
    title = "データ収集屋さん"
    return render_template('index.html',title=title)
    # return render_template('index1.html',title=title)

#/post にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def _make_data():
    if request.method == 'POST':
        if "https" in request.form["URL"]:
            URL = request.form['URL']
            """URLからスクレイピング"""
            df = processing.first_scray(URL)
            if len(df):
                return processing.download(df)
    shinjin = "新人「光のロマンで迫るからエラーが出ましたゾス」"
    boss = "ボス「いいから早くアポ取ってこいや」"
    return render_template('back.html',shinjin=shinjin, boss=boss)

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run()
