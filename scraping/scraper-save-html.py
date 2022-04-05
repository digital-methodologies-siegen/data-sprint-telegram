# -*- coding: utf-8 -*-
import csv
import requests
import re
import os.path
import time
from bs4 import BeautifulSoup
import lxml
import pandas as pd

MAX_NUMBER = 1


path_html_sites = "../data/html-sites/"
OUT_PATH_ERR = "../data/html-files-scraping-errors.csv"

### first function to be called:

def iterate_channels():
    channel_list = pd.read_csv("channels.csv")
    for index, row in channel_list.iterrows():
        print(str(index) + " " + row[1])
        get_channel(row["name"], row[1])

def get_channel(channel_name, base_page):

    init_page = get_server_response(base_page)
    print("xxxxxxxxxxxxx")
    save_html(init_page, channel_name, "")
    next_page_link = get_page_link(init_page, base_page)
    
    while next_page_link != None:
        content = get_server_response(next_page_link)

        save_html(content, channel_name, next_page_link)
        next_page_link = get_page_link(content, base_page)
  

def save_html(page, channel, path_to_save_at):

    current_message_nr = re.search(r"before.*$", path_to_save_at)
    if current_message_nr is not None: 
        file_path = path_html_sites + channel + "-" + current_message_nr[0] + ".html"
    else:
        file_path = path_html_sites + channel +".html"

    if True != os.path.isfile(file_path):
        try:
            # xml = get_xml(content)
            file = open(file_path, "w", encoding = "utf-8")
            file.write(str(page))
            file.close()
        
        except Exception as e:
                print ("error with " + file_path)
                temp_df = pd.DataFrame({"link":[file_path], "error":[e.args]})
                temp_df.to_csv(path_or_buf = OUT_PATH_ERR, index=False, mode = "a", header = False)


def get_page_link(page, base_page):
    base_page = re.sub(r"[\\?]before.*$", "", base_page)
    # print(base_page)
    message_nr = [] 
    bubbles = page.find_all("div", {"class":"tgme_widget_message_wrap js-widget_message_wrap"})
    for bubble in bubbles:
        message_nr_raw = bubble.find("div", {"class": "tgme_widget_message"})["data-post"]
        message_nr_cleaned = int(re.findall(r"\d{1,}$", message_nr_raw)[0])
        message_nr.append(message_nr_cleaned)

    # print("xxxxxxxxxxxxxxx")s
    oldest_message_index = min(message_nr)
    # print("oldest message scraped: " + str(oldest_message_index))

    if oldest_message_index > MAX_NUMBER:
        new_link = base_page + "?before=" + str(oldest_message_index)
    else:
        new_link = None

    return (new_link)

def get_server_response(link):
    # print("in server response " + link)
    init_page = requests.get(link)
    init_page.raise_for_status()
    # if status_code == 500:
    #     sleep(10)
    #     get_server_response(link)
    init_page = init_page.text.encode("utf-8")
    page = BeautifulSoup(init_page, "lxml")
    page.prettify() 
    return page

iterate_channels()

