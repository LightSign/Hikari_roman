# -*- coding: utf-8 -*-
from flask import make_response
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

def first_scray(URL):
    # header偽装？？　いや、結論、お客さんが喜べば、それイイことだから。
    headers = {
    "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
    }
    # dataframe定義しちゃうから。
    df = pd.DataFrame(index=[] , columns=[])
    # これお客さんからのresponseで受注だから。
    res = requests.get(URL ,headers=headers)
    # ここで、落ち着いてhtml見積書解析しちゃいますよ、と。
    soup = bs(res.content, "html.parser")
    try:
        # ここでページ全体のコールリスト取っちゃうから。
        items = soup.select("div.s-item-container")
        # そのリストからfor無限アポ掛けしますよ、と。
        for item in items:
            ## 全国のコールリスト取っちゃうから。
            try:
                title = item.select("img")[0].get("alt")
                item_url = "https://www.amazon.co.jp" + item.select("a")[0].get("href")
                if item.find(class_="a-icon a-icon-jp a-icon-prime-jp a-icon-small s-align-text-bottom"):
                    prime = "prime"
                else:
                    prime = "no prime"
                pic_split = item.select("img")[0].get("srcset").split()
                pic_txt = ",".join(pic_split).split()
                picures_list = []
                for p_txt in pic_txt:
                    if "jpg" in p_txt:
                        picures_list.append(p_txt)
                se = pd.Series(
                    [title, item_url, prime, picures_list],
                    ["title", "item_url", "prime", "picures_list"]
                )
                df = df.append(se, ignore_index=True)
            ## リストないところはスルーして、次行くっしょ。
            except Exception as e:
                pass
    ## リスト取れないときは、passしちゃうってこと。
    except:
        pass
    ## まとめたリストに早くアポ掛けしてよ。
    return df

import csv
import io as cStringIO
import random
def download(df):
    # ここに名言ファイル名あるから。
    txt = """
    MoshiMoshiWatakushyyyyy
    NttnohoukaraOdenwashiteorimasu
    Zosu
    Osu
    HikariNoRoman
    KanzenOrderYarimasu
    DokkoiKiaideAgeteYaru
    ShigetaGod
    KonoyodeIppikiHikarXXXXXXXNoEigyomanHa
    """
    txt_split = txt.split()
    # ランダムで名言出ちゃうから。　普通に。
    file_name = random.choice(txt_split)

    # まあ、ここよくわかんないけど、結論大丈夫だから。
    f = cStringIO.StringIO()
    writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL, lineterminator="\n")
    # ココでカラム名指定してるから。
    writer.writerow(['item_url','pic_list','prime','title'])
    # リスト上から全部掛けちゃうよ。
    for i in range(len(df)):
        writer.writerow([
            df.item_url[i],
            df.picures_list[i],
            df.prime[i],
            df.title[i]
        ])
    # response作ってるらしいよ。　まあアポ取れればいいでしょ。細かいことは。
    res = make_response()
    res.data = f.getvalue()
    res.headers['Content-Type'] = 'text/csv'
    # ここで名言ファイル名csv出来ちゃいますよ、と。
    res.headers['Content-Disposition'] = 'attachment; filename='+ file_name +'.csv'
    return res
