# -*- coding: utf-8 -*-
import pandas as pd
from pandas import Series,DataFrame
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime,timedelta
import time
from time import sleep
import re
import random

class crawler:
    def __init__(self, query, price_min, price_max):
        self.queries = query.split(',')
        self.price_min = price_min
        self.price_max = price_max

        # # ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
        self.options = Options()
        self.options.binary_location = '/app/.apt/usr/bin/google-chrome'
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=options)
        self.date = datetime.today().strftime("%Y%m%d_")

    def srch_scray_test(self, query, price_min, price_max):
        # df = pd.read_csv('default.csv', index_col=0)
        df = pd.DataFrame(index=[] , columns=[])
        url_df = pd.DataFrame(index=[] , columns=[])
        #販売中＆売り切れ選定用
        self.browser.get("https://www.mercari.com/jp/search/?sort_order=&keyword={0}&category_root=&brand_name=&brand_id=&size_group=&price_min={1}&price_max={2}".format(query,price_min,price_max))

        #販売中のみ選定用
        #self.browser.get("https://www.mercari.com/jp/search/?sort_order=&keyword={0}&category_root=&brand_name=&brand_id=&size_group=&price_min={1}&price_max={2}&status_on_sale={3}".format(query,price_min,price_max,sale_st))
        page = 1

        while True: #continue until getting the last page
            if len(self.browser.find_elements_by_css_selector("li.pager-next .pager-cell:nth-child(1) a")) > 0:
                #print("######################page: {} ########################".format(page))
                #print("Starting to get posts...")

                posts = self.browser.find_elements_by_css_selector(".items-box")

                for post in posts:
                    title = post.find_element_by_css_selector("h3.items-box-name").text

                    price = post.find_element_by_css_selector(".items-box-price").text
                    price = price.replace('¥', '')

                    sold = 0
                    if len(post.find_elements_by_css_selector(".item-sold-out-badge")) > 0:
                        sold = 1

                    url = post.find_element_by_css_selector("a").get_attribute("href")
                    se = pd.Series([title, price, sold,url],['title','price','sold','url'])
                    df = df.append(se, ignore_index=True)
                    #input_list1 = pd.concat([input_list1,input_num_list],ignore_index=True)
                page+=1
                btn = self.browser.find_element_by_css_selector("li.pager-next .pager-cell:nth-child(1) a").get_attribute("href")
                #print("next url:{}".format(btn))
                self.browser.get(btn)
                time = random.uniform(0,2)
                sleep(time)
                #print("Moving to next page......")
                break
            else:
                print("no pager exist anymore")
                break
        print("First list done then next")
        print("Total items are " + str(len(df)))
        date = datetime.today().strftime("%Y%m%d_")

        for i in range(0,len(df)):
            self.browser.get(df["url"][i])
            print(str(i) + " " +"page")
            time = random.uniform(1,5)
            sleep(time)

            if self.browser.find_elements_by_css_selector(".owl-dot-inner"):
            #########################写真複数
                #スクショ取得
                #pc_title = self.browser.find_element_by_css_selector("h2.item-name").text
                #self.browser.get_screenshot_as_file("/Users/satohikaru/Documents/Practice analysis/pictures/{}.png".format(pc_title))
                #スクショ取得

                photos = self.browser.find_elements_by_css_selector(".owl-dot-inner")
                p_url = []
                pc_url = ""
                #写真URLを１個ずつ取得するループ文
                for i in range(0,len(photos)):
                    picuture = photos[i]
                    p_url.append(picuture.find_element_by_css_selector("img").get_attribute("src"))
                    pc_url = ','.join(p_url)
                #########################写真複数

                #########################商品ステータス取得
                tb_elem = self.browser.find_element_by_class_name("item-detail-table")
                trs = tb_elem.find_elements(By.TAG_NAME, "tr")
                col_name = []
                ele_name = []
                for i in range(0,len(trs)):
                    tds = trs[i].find_elements(By.TAG_NAME, "td")
                    for j in range(0,len(tds)):
                        ele_name.append("%s," % (tds[j].text))
                #########################商品ステータス取得

                #########################商品説明取得
                descrip = self.browser.find_element_by_css_selector(".item-description.f14").text
                #########################商品説明取得

                #########################コメント＆出品日＆直近日取得
                coments = []
                coms = self.browser.find_elements_by_css_selector("li.clearfix")

                # whether coments or not
                if len(coms) > 0:
                    for i in range(0,len(coms)):
                        coments.append("%s" % (coms[i].find_element_by_css_selector(".message-body-text").text + " " +  coms[i].find_element_by_tag_name("span").text) + " " + str(i))

                    amt_cmts = len(coments)
                    # get the first and last coments
                    fir_c = ",".join([c for c in coments if c.endswith(' 0')])
                    last_c = ",".join([c for c in coments if c.endswith(str(len(coments) - 1))])
                    match_fir = re.search(r"\d{1,4}\s(時|日|分|秒)",fir_c).group()
                    match_last = re.search(r"\d{1,4}\s(時|日|分|秒)",last_c).group()

                    #get first and last day integers
                    first_d = re.search(r"\d{1,4}",match_fir).group()
                    last_d = 0
                    if match_last.endswith("日"):
                        last_d = int(re.search(r"\d{1,4}",match_last).group())
                    elif match_last.endswith("時"):
                        last_d = 1
                    else:
                        print("Nothing")

                    #culculate btw first and last date
                    now = datetime.now().date()
                    fir_d = timedelta(days=int(first_d))
                    last_d = timedelta(days=int(last_d))
                    first_date = (now - fir_d).strftime("%Y/%m/%d")
                    last_date = (now - last_d).strftime("%Y/%m/%d")
                    #########################コメント＆出品日＆直近日取得

                    todays = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
                    status_ser = pd.Series([ele_name,pc_url,first_date,last_date,todays,descrip,coments,amt_cmts],["ele_name","pc_url","first_date","last_date","date","descrip","coments","amt_cmts"])
                    url_df = url_df.append(status_ser , ignore_index=True)
                else:
                    first_date = " "
                    last_date = " "
                    amt_cmts = " "
                    todays = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
                    status_ser = pd.Series([ele_name,pc_url,first_date,last_date,todays,descrip,coments,amt_cmts],["ele_name","pc_url","first_date","last_date","date","descrip","coments","amt_cmts"])
                    url_df = url_df.append(status_ser , ignore_index=True)
            #########################写真複数

            elif self.browser.find_elements_by_css_selector("div.item-main-content.clearfix"):
            #########################写真1枚取得
                #スクショ取得
                #pc_title = self.browser.find_element_by_css_selector("h2.item-name").text
                #self.browser.get_screenshot_as_file("/Users/satohikaru/Documents/Practice analysis/pictures/{}.png".format(pc_title))
                #スクショ取得

                #########################写真1枚取得
                pc_url = []
                photos = self.browser.find_elements_by_css_selector("div.item-main-content.clearfix")
                pc_url.append(photos[0].find_element_by_css_selector("img").get_attribute("src"))


                #########################商品ステータス取得
                tb_elem = self.browser.find_element_by_class_name("item-detail-table")
                trs = tb_elem.find_elements(By.TAG_NAME, "tr")
                col_name = []
                ele_name = []
                for i in range(0,len(trs)):
                    tds = trs[i].find_elements(By.TAG_NAME, "td")
                    for j in range(0,len(tds)):
                        ele_name.append("%s," % (tds[j].text))
                #########################商品ステータス取得

                #########################商品説明取得
                descrip = self.browser.find_element_by_css_selector(".item-description.f14").text
                #########################商品説明取得


                #########################コメント＆出品日＆直近日取得
                coments = []
                coms = self.browser.find_elements_by_css_selector("li.clearfix")

                # whether coments or not
                if len(coms) > 0:
                    for i in range(0,len(coms)):
                        coments.append("%s" % (coms[i].find_element_by_css_selector(".message-body-text").text + " " +  coms[i].find_element_by_tag_name("span").text) + " " + str(i))

                    amt_cmts = len(coments)
                    # get the first and last coments
                    fir_c = ",".join([c for c in coments if c.endswith(' 0')])
                    last_c = ",".join([c for c in coments if c.endswith(str(len(coments) - 1))])
                    match_fir = re.search(r"\d{1,4}\s(時|日|分|秒)",fir_c).group()
                    match_last = re.search(r"\d{1,4}\s(時|日|分|秒)",last_c).group()

                    #get first and last day integers
                    first_d = re.search(r"\d{1,4}",match_fir).group()
                    last_d = 0
                    if match_last.endswith("日"):
                        last_d = int(re.search(r"\d{1,4}",match_last).group())
                    elif match_last.endswith("時"):
                        last_d = 1
                    else:
                        print("Nothing")

                    #culculate btw first and last date
                    now = datetime.now().date()
                    fir_d = timedelta(days=int(first_d))
                    last_d = timedelta(days=int(last_d))
                    first_date = (now - fir_d).strftime("%Y/%m/%d")
                    last_date = (now - last_d).strftime("%Y/%m/%d")
                #########################コメント＆出品日＆直近日取得

                    todays = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
                    status_ser = pd.Series([ele_name,pc_url,first_date,last_date,todays,descrip,coments,amt_cmts],["ele_name","pc_url","first_date","last_date","date","descrip","coments","amt_cmts"])
                    url_df = url_df.append(status_ser , ignore_index=True)
                else:
                    first_date = " "
                    last_date = " "
                    amt_cmts = " "
                    todays = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
                    status_ser = pd.Series([ele_name,pc_url,first_date,last_date,todays,descrip,coments,amt_cmts],["ele_name","pc_url","first_date","last_date","date","descrip","coments","amt_cmts"])
                    url_df = url_df.append(status_ser , ignore_index=True)
            #########################写真１枚

            else:
                #########################商品削除ページ
                pc_url = " "
                col_name = " "
                ele_name = " "
                descrip = " "
                first_date = " "
                last_date = " "
                amt_cmts = " "
                todays = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
                status_ser = pd.Series([ele_name,pc_url,first_date,last_date,todays,descrip,coments,amt_cmts],["ele_name","pc_url","first_date","last_date","date","descrip","coments","amt_cmts"])
                url_df = url_df.append(status_ser , ignore_index=True)
                #########################商品削除ページ

            ################ テスト用 ############################
            if i > 0:
                self.browser.close()
                break
            ################ テスト用 ############################

        print("Finished all lists")
        all_df = pd.concat([df,url_df], axis=1)
        all_df.to_csv("./data/{0}{1}_table.csv".format(self.date,query))

    def run(self):
        df = pd.DataFrame(index=[] , columns=[])
        for i in range(0,len(self.queries)):
            new_df = self.srch_scray_test(self.queries[0], self.price_min, self.price_max)
            df = pd.concat([df,new_df],ignore_index=True)
        return df
