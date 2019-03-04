# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for , make_response,Response
from flask_cors import CORS, cross_origin
from datetime import datetime
from processing import processing

# flask初期化しちゃいますよ、と。
# apo掛けもしちゃいますよ、と。
app = Flask(__name__)
CORS(app)

# / にアクセスしたとき、処理しちゃいますよ、と。
@app.route('/')
def index():
    return render_template('index.html')

#/post にアクセスしました、と。　結論、スクレイピングしますよ、と。
@app.route('/post', methods=['GET', 'POST'])
def make_data():
    # POSTの処理をしますよ、と。
    if request.method == 'POST':
        # もしHTTPSが入力されたら下記処理をしますよ、と。
        if "https" in request.form["URL"]:
            URL = request.form['URL']
            # 結論、ここでスクレイピング始めちゃうから。大丈夫エラーなんて出ないから。
            df = processing.first_scray(URL)
            # dataframeがゼロアポじゃなかったら、CSVダウンロードしちゃいますよ、と。
            if len(df):
                return processing.download(df)
    # URLに空白が入力されたら詰められますよ、と。
    shinjin = "新人「光のロマンで迫るからエラーが出ましたゾス」"
    boss = "ボス「いいから早くアポ取ってこいや」"
    return render_template('back.html',shinjin=shinjin, boss=boss)

if __name__ == '__main__':
    # 結論、apo掛けするから。ゼロアポなんて普通にないから。
    # 1日500コール普通だから。500コールでゼロアポなんてないから。
    app.run()
