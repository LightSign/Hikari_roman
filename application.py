# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for , make_response,Response
from flask_cors import CORS, cross_origin
from datetime import datetime
from processing import processing

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)
CORS(app)

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    title = "データ収集屋さん"
    return render_template('index.html',title=title)

#/post にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def _make_data():
    if request.method == 'POST':
        URL = request.form['URL']
        """URLからスクレイピング"""
        browser = processing.headless_browser()
        df = processing.first_scray(URL, browser)
        if len(df):
            return processing.return_csv(df)
        return "エラーです"
    else:# エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run() # どこからでもアクセス可能に
