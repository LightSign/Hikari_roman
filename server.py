# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for , send_file
import pandas as pd
from pandas.io import gbq
from pandas import Series,DataFrame
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime,timedelta
from time import sleep
import re
import random
from google.cloud import translate
import os
# import csv
# import io as cStringIO
import requests
from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome, ChromeOptions

app = Flask(__name__)

@app.route('/')
def index():
    title = "神ツール : 実行ページ"
    return render_template('index.html',title=title)

@app.route('/post', methods=['GET', 'POST'])
def _make_data():
    title = "神ツール : 結果ページ"
    if request.method == 'POST':
        # リクエストフォームから「名前」を取得して
        # ATOM_id = request.form['ATOM_id']
        URL = request.form['URL']
        # search_keyword = request.form['search_keyword']
        # price_lower = request.form['price_lower']
        # price_upper = request.form['price_upper']
        # search_weight = request.form['search_weight']
        # tmp1 = request.form['tmp1']
        # tmp2 = request.form['tmp2']
        # tmp3 = request.form['tmp3']

        ##TranslateAPI用にJSONファイル読み込み
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='/app/My_First_Project-c39e439a3d08.json'
        #os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='/Users/satohikaru/Documents/new_atom/My_First_Project-c39e439a3d08.json'

        # サンプルURL
        #URL = "https://auctions.yahoo.co.jp/search/search?auccat=&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=iphonese+SIM%E3%83%95%E3%83%AA%E3%83%BC+%E6%96%B0%E5%93%81+32GB+%E3%82%B7%E3%83%AB%E3%83%90%E3%83%BC&x=0&y=0&fixed=0"

        # ヘッドレスモードを有効にする
        options = ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)
        # browser = webdriver.Chrome()
        browser.get(URL)

        kw = "test_iphone_se3"
        date = datetime.today().strftime("%Y%m%d")
        df = pd.DataFrame(index=[] , columns=[])
        while True:
            if len(browser.find_elements_by_css_selector("#ASsp1 > p.next > a")) == 0:
                # get Npage of all tables
                tables = browser.find_elements_by_css_selector("td.a1")
                curr_price_tb = browser.find_elements_by_css_selector("td.pr1")
                buy_now_price_tb = browser.find_elements_by_css_selector("td.pr2")
                bitter_tb = browser.find_elements_by_css_selector("td.bi")
                rest_date_tb = browser.find_elements_by_css_selector("td.ti")
                # get each element
                for i in range(len(tables)):
                    all_string = tables[i].text
                    title = all_string[:all_string.index("\n出品者")].replace("\W","")
                    url = tables[i].find_element_by_css_selector("a").get_attribute("href")
                    crr_pr = curr_price_tb[i].text
                    crr_price = crr_pr[:crr_pr.index("\n")].replace("円","").replace(",","")
                    buy_now_price = buy_now_price_tb[i].text
                    ctgr = re.search(r"(?<=\nカテゴリ)(.*)",all_string).group().replace(" ","").split(">")
                    bitter = bitter_tb[i].text
                    rest_time = rest_date_tb[i].text
                    try:
                        ## get item categories
                        fir_ctg = ctgr[0]
                        sec_ctg = ctgr[1]
                        final_ctg = ctgr[2]
                    except Exception:
                        ## get item categories
                        fir_ctg = ctgr[0]
                        sec_ctg = ctgr[1]
                        final_ctg = "Nothing"
                    # put all elements into dataframe
                    se = pd.Series([title, url, crr_price,buy_now_price,fir_ctg,sec_ctg,final_ctg,bitter,rest_time],['title','url','crr_price','buy_now_price',"fir_ctg","sec_ctg","final_ctg","bitter","rest_time"])
                    df = df.append(se, ignore_index=True)
                break
            else:
                # get Npage of all tables
                tables = browser.find_elements_by_css_selector("td.a1")
                curr_price_tb = browser.find_elements_by_css_selector("td.pr1")
                buy_now_price_tb = browser.find_elements_by_css_selector("td.pr2")
                bitter_tb = browser.find_elements_by_css_selector("td.bi")
                rest_date_tb = browser.find_elements_by_css_selector("td.ti")
                # get each element
                for i in range(len(tables)):
                    all_string = tables[i].text
                    title = all_string[:all_string.index("\n出品者")].replace("\W","")
                    url = tables[i].find_element_by_css_selector("a").get_attribute("href")
                    crr_pr = curr_price_tb[i].text
                    crr_price = crr_pr[:crr_pr.index("\n")].replace("円","").replace(",","")
                    buy_now_price = buy_now_price_tb[i].text
                    ctgr = re.search(r"(?<=\nカテゴリ)(.*)",all_string).group().replace(" ","").split(">")
                    bitter = bitter_tb[i].text
                    rest_time = rest_date_tb[i].text
                    try:
                        ## get item categories
                        fir_ctg = ctgr[0]
                        sec_ctg = ctgr[1]
                        final_ctg = ctgr[2]
                    except Exception:
                        ## get item categories
                        fir_ctg = ctgr[0]
                        sec_ctg = ctgr[1]
                        final_ctg = "Nothing"
                    # put all elements into dataframe
                    se = pd.Series([title, url, crr_price,buy_now_price,fir_ctg,sec_ctg,final_ctg,bitter,rest_time],['title','url','crr_price','buy_now_price',"fir_ctg","sec_ctg","final_ctg","bitter","rest_time"])
                    df = df.append(se, ignore_index=True)
                # move to next page
                next_url = browser.find_elements_by_css_selector("#ASsp1 > p.next > a")[0].get_attribute("href")
                browser.get(next_url)
                time = random.uniform(2,3)
                sleep(time)


        df["rest_time"] = df["rest_time"].apply(lambda x : x.replace("日","") if x.endswith("日") else str(1))
        print(len(df))
        url_df = pd.DataFrame(index=[] , columns=[])
        for i in range(len(df)):
            browser.get(df["url"][i])
            time = random.uniform(2,3)
            sleep(time)

            pics = browser.find_elements_by_css_selector("li.ProductImage__thumbnail")
            p_url = []
            pc_url = ""
            for i in pics:
                p_url.append(i.find_element_by_css_selector("img").get_attribute("src"))
                pc_url = '|'.join(p_url)

            #get all status elements
            status_ele = browser.find_elements_by_css_selector("dd.ProductDetail__description")
            #get all status elements

            # get each elements
            status = status_ele[0].text.replace(r"：","")
            quantity = status_ele[1].text.replace(r"：","")
            start_tm = status_ele[2].text.replace(r"：","")
            end_tm = status_ele[3].text.replace(r"：","")
            enchou = status_ele[4].text.replace(r"：","")
            early_end = status_ele[5].text.replace(r"：","")
            return_item = status_ele[6].text.replace(r"：","")
            evaluate = status_ele[7].text.replace(r"：","")
            auth = status_ele[8].text.replace(r"：","")
            max_buyer = status_ele[9].text.replace(r"：","")
            start_price = status_ele[10].text.replace(r"：","")
            auction_id = status_ele[11].text.replace(r"：","")

            user_id ="https://auctions.yahoo.co.jp/seller/" + browser.find_elements_by_css_selector("span.Seller__name")[0].text.replace(u"さん","")
            good = browser.find_elements_by_css_selector("span.Seller__ratingGood")[0].text
            bad = browser.find_elements_by_css_selector("span.Seller__ratingBad")[0].text
            # area = browser.find_elements_by_css_selector("dd.Seller__areaName")[0].text
            descrip = browser.find_elements_by_css_selector("div.ProductExplanation__commentBody.js-disabledContextMenu")[0].text.replace("\n"," ")

            ship_ways = browser.find_elements_by_css_selector(".ProductProcedure__items")[1].text.splitlines()
            se = pd.Series([
                kw
                ,pc_url
                ,status
                ,quantity
                ,start_tm
                ,end_tm
                ,enchou
                ,early_end
                ,return_item
                ,evaluate
                ,auth
                ,max_buyer
                ,start_price
                ,auction_id
                ,user_id
                ,good
                ,bad
                ,descrip
                ,ship_ways
                ],
                [
                "kw"
                ,"pc_url"
                ,"status"
                ,"quantity"
                ,"start_tm"
                ,"end_tm"
                ,"enchou"
                ,"early_end"
                ,"return_item"
                ,"evaluate"
                ,"auth"
                ,"max_buyer"
                ,"start_price"
                ,"auction_id"
                ,"user_id"
                ,"good"
                ,"bad"
                ,"descrip"
                ,"ship_ways"
                ])
            url_df = url_df.append(se, ignore_index=True)

        all_df = pd.concat([df,url_df], axis=1)
        all_df["title"] = all_df["title"].str.replace(r'\W', " ").str.replace(r'遊戯王', "Yu-Gi-Oh").str.replace(r'東京喰種', "Tokyo Ghoul").str.replace(r'イッセイミヤケ', "ISSEY MIYAKE")
        all_df["descrip"] = all_df["descrip"].str.replace(r'\W', " ")
        # all_df["ship_ways"] = all_df["ship_ways"].str.replace(r"\W"," ")
        all_df = all_df.astype("str")
        # all_df.to_csv("{0}_{1}.csv".format(date,kw),index=False)
        browser.quit()
        print("finish all df")

        # bq_table = 'For_test_tb.sample'
        # gbq.to_gbq(all_df,bq_table, project_id='my-first-project-166403',if_exists="append")
        #
        # query="""
        # SELECT
        #     *
        # FROM {0}
        # WHERE kw = "{1}"
        # """.format(bq_table,kw)
        # new_df = gbq.read_gbq(query, project_id='my-first-project-166403', verbose=False,dialect="standard")

        new_df = all_df
        translate_client = translate.Client()
        target = 'en'
        for i in range(len(new_df)):
            new_df.loc[i,"title"] = translate_client.translate(new_df.loc[i,"title"],target_language=target)['translatedText']

        # print("start make data")
        # def _make_file(data):
        #     """
        #     データを CSV 形式に変換
        #     """
        #     csv_file = cStringIO.StringIO()
        #     writer = csv.writer(csv_file, quoting=csv.QUOTE_NONE, delimiter=',', quotechar=',')
        #     writer.writerow(data)
        #     writer.writerows(data.values)
        #     return csv_file.getvalue()
        #
        # print("data to CSV")
        # def make_csv(file_csv):
        #     """
        #     CSV 出力
        #     """
        #     response = make_response()
        #     response.data = file_csv
        #     response.headers['Content-Type'] = 'application/octet-stream'
        #     response.headers['Content-Disposition'] = 'attachment; filename=ATOM_test.csv'
        #     return response
        #
        # file_csv = _make_file(new_df)
        # csv_data = make_csv(file_csv)
        # return csv_data
        new_df.to_csv("{0}_{1}.csv".format(date,kw),index=False)
        return send_file("/app/{0}_{1}.csv".format(date,kw),attachment_filename="{0}_{1}.csv".format(date,kw))
        #return send_file("/Users/satohikaru/Documents/new_ATOM/{0}_{1}.csv".format(date,kw),attachment_filename="{0}_{1}.csv".format(date,kw))

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0') # どこからでもアクセス可能に
