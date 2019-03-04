from flask import make_response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

def headless_browser():
    options = webdriver.chrome.options.Options()
    options.binary_location = '/app/.apt/usr/bin/google-chrome'
    options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=options)
    browser.set_page_load_timeout(10)
    return browser

def first_scray(URL, browser):
    df = pd.DataFrame(index=[] , columns=[])
    try:
        browser.get(URL)
        items = browser.find_elements_by_css_selector("div.s-item-container")
        for item in items:
            try:
                title = item.find_element_by_css_selector("h2").text
                item_url = item.find_element_by_css_selector("a").get_attribute("href")
                # check whether prime or not
                if item.find_elements_by_css_selector("i.a-icon.a-icon-jp.a-icon-prime-jp.a-icon-small.s-align-text-bottom"):
                    prime = "prime"
                else:
                    prime = "no prime"
                pic_split = item.find_element_by_css_selector("img").get_attribute("srcset").split(",")
                pic_txt = ",".join(pic_split).split()
                pic_list = []
                for p_txt in pic_txt:
                    if "jpg" in p_txt:
                        pic_list.append(p_txt)
                se = pd.Series(
                    [title, item_url, prime, pic_list],
                    ["title", "item_url", "prime", "pic_list"]
                )
                df = df.append(se, ignore_index=True)
            except:
                pass
        df = df.head(10).reset_index(drop=True)
        browser.quit()
    except Exception as e:
        pass
    return df

import csv
import io as cStringIO
def return_csv(data):
    def toCSV_format(data):
        """データを CSV 形式に変換"""
        csv_file = cStringIO.StringIO()
        writer = csv.writer(csv_file, quoting=csv.QUOTE_NONE, delimiter=',', quotechar=',')
        writer.writerow(data)
        writer.writerows(data.values)
        return csv_file.getvalue()

    def make_csv(csv_format_df):
        """CSV 出力"""
        response = make_response()
        response.data = csv_format_df
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = 'attachment; filename=ATOM_test.csv'
        return response

    csv_format_df = toCSV_format(data)
    csv_data = make_csv(csv_format_df)
    return csv_data
