# Flask などの必要なライブラリをインポートする
from flask import Flask, render_template, request, redirect, url_for , send_file
from datetime import datetime,timedelta
import subprocess
from crawler import crawler

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# メッセージをランダムに表示するメソッド
# def exec_crawler():

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    title = "神ツール : 実行ページ"
    return render_template('index.html',title=title)

# @app.route('/return_file/')
# def return_file():
#     date = datetime.today().strftime("%Y%m%d_")
#     PATH_to_file = "/Users/satohikaru/Documents/Practice_analysis/ebay/new_ATOM/data/"
#     return send_file(PATH_to_file + "{0}_{1}_tb.csv".format(date,search_keyword) ,attachment_filename="{0}_{1}_tb.csv".format(date,search_keyword))

# @app.route('/file-downloads/')
# def file_downloads():
#     return render_template("downloads.html")

#/post にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "神ツール : 結果ページ"
    if request.method == 'POST':
        # リクエストフォームから「名前」を取得して
        ebay_id = request.form['ebay_id']
        ebay_pass = request.form['ebay_pass']
        search_keyword = request.form['search_keyword']
        price_lower = request.form['price_lower']
        price_upper = request.form['price_upper']
        search_weight = request.form['search_weight']
        tmp1 = request.form['tmp1']
        tmp2 = request.form['tmp2']
        tmp3 = request.form['tmp3']

        c = crawler(search_keyword, int(price_lower), int(price_upper))
        df = c.run()

        date = datetime.today().strftime("%Y%m%d_")
        PATH_to_file = "./data/"
        # index.html をレンダリングする
        return send_file(df ,attachment_filename="{0}{1}_table.csv".format(date,search_keyword))
        return render_template('finish.html',
                               ebay_id = ebay_id,
                               ebay_pass = ebay_pass,
                               search_keyword = search_keyword,
                               price_lower = price_lower,
                               price_upper = price_upper,
                               search_weight = search_weight,
                               tmp1=tmp1,
                               tmp2=tmp2,
                               tmp3=tmp3,
                               )
    else:
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0') # どこからでもアクセス可能に
