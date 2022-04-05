# -*- coding: utf-8 -*-
import csv
import requests
import re
import os.path
import time
from bs4 import BeautifulSoup
import lxml
import pandas as pd
from os import walk
import glob

MAX_NUMBER = 1
path_html_sites = "../data/html-sites/*"
PATH_TO_SAVE_AT = "../data/parsed/parsed-data.csv"

### first function to be called:

def iterate_files():

    # init the dataframe column names, it's getting filled later on with data 
    df_init = pd.DataFrame({"message_nr": [], "message_views": [], "message_sent": [], "message_text": [], "message_fwd_from_name": [], "message_fwd_from_link": [], "message_link_preview": [], "prev_link_site": [], "prev_link_title": [], "prev_link_description": [], "prev_link_image": [], "message_photo_link" : [], "message_video" : [], "message_round_video": [], "message_video_link" :[]})
    # storing the empty dataframe
    df_init.to_csv(PATH_TO_SAVE_AT, mode = "w")

    filenames = glob.glob(path_html_sites)
    for file_path in filenames:
        get_channel(file_path)
    
## second function being called from iterate_channels()

def get_channel(file_path):
    
    file_name_raw = file_path.split("/")
    file_name_raw = file_name_raw[len(file_name_raw)-1]
    file_name = re.sub(r"-before.*$", "", file_name_raw)

    page = get_server_response(file_path)
    print("xxxxxxxxxxxxx " + file_path)

    get_messages(page)
  

def get_messages(page):
    bubble_data = []
    bubbles = page.find_all("div", {"class":"tgme_widget_message_wrap js-widget_message_wrap"})
    
    message_nr=[]
    message_text = []
    message_views = []
    message_sent = []
    message_fwd_from_name = []
    message_fwd_from_link = []
    message_link_preview = []
    message_round_video = []
    message_video = []
    message_video_link = []
    prev_link_site = []
    prev_link_title = []
    prev_link_description = []
    prev_link_image = []
    message_photo_link = []

    for bubble in bubbles:

        message_nr_raw = bubble.find("div", {"class": "tgme_widget_message"})["data-post"]
        message_nr_cleaned = re.findall(r"\d{1,}$", message_nr_raw)[0]
        # print((message_nr_cleaned))
        message_nr.append(message_nr_cleaned)
        message_sent.append(bubble.find("a", {"class": "tgme_widget_message_date"}).find("time", {"class": "time"})["datetime"])
        
        has_views_attr = bubble.find("span", {"class": "tgme_widget_message_views"})
        if has_views_attr != None:
            message_views.append(has_views_attr.text)
        else:
            message_views.append("NA")
        
        
        has_text = bubble.find("div", {"class": "tgme_widget_message_text js-message_text"})
        if has_text != None:
            message_text.append(has_text.text)
        else:
            message_text.append("NA")

        is_forwarded = bubble.find("span", {"class": "tgme_widget_message_forwarded_from_name"})
        is_forwarded_linked = bubble.find("a", {"class": "tgme_widget_message_forwarded_from_name"})
        if(is_forwarded != None or is_forwarded_linked != None):
            if is_forwarded != None:
                message_fwd_from_name.append(is_forwarded.string)
                message_fwd_from_link.append("NA")

            if(is_forwarded_linked != None):
                message_fwd_from_name.append(is_forwarded_linked.string)
                message_fwd_from_link.append(is_forwarded_linked["href"])
        else:
            message_fwd_from_name.append("NA")
            message_fwd_from_link.append("NA")

        photo_linked = bubble.find("a", {"class" : "tgme_widget_message_photo_wrap"})
        if photo_linked != None:
            raw_link = photo_linked["style"]
            link_cleaned = re.findall(r"https.*jpg", raw_link)[0]
            message_photo_link.append(link_cleaned)
        else:
            message_photo_link.append("NA")

        is_round_video_message = bubble.find("div", {"class": "tgme_widget_message_roundvideo_wrap"})
        if is_round_video_message != None:
            message_round_video.append("TRUE")
        else:
            message_round_video.append("FALSE")

        contains_video = bubble.find("a", {"class": "tgme_widget_message_video_player"})
        if contains_video != None:
            message_video.append("TRUE")
        else:
            message_video.append("FALSE")

        contains_embedded_video = bubble.find("video", {"class" : "tgme_widget_message_video"})
        if contains_embedded_video != None:
            # raw_link = 
            # link_cleaned = re.findall()
            message_video_link.append(contains_embedded_video["src"])
        else:
            message_video_link.append("NA")


        prev_available = bubble.find("a", {"class": "tgme_widget_message_link_preview"})
        if(prev_available != None):
            message_link_preview.append(prev_available["href"])
            
            # prev_link_site.append("NA")
            # prev_link_title.append("NA")
            # prev_link_description.append("NA")
            # prev_link_image.append("NA")

            link_site = prev_available.find("div", {"class": "link_preview_site_name accent_color"})
            if (link_site != None):
                prev_link_site.append(link_site.text)
            else:
                prev_link_site.append("NA")

            link_title = prev_available.find("div", {"class": "link_preview_title"})
            if link_title != None:
                prev_link_title.append(link_title.text)
            else: 
                prev_link_title.append("NA")

            link_description = prev_available.find("div", {"class": "link_preview_description"})
            if link_description != None:
                prev_link_description.append(link_description.text)
            else:
                prev_link_description.append("NA")

            link_image = prev_available.find("i")
            if link_image != None:
                raw_link = link_image["style"].strip("background-image:url('")
                cleaned_link = raw_link.strip("')")
                prev_link_image.append(cleaned_link)
            else:
                prev_link_image.append("NA")

        else:
            message_link_preview.append("NA")
            prev_link_site.append("NA")
            prev_link_title.append("NA")
            prev_link_description.append("NA")
            prev_link_image.append("NA")

    bubble_data = {"message_nr": message_nr, "message_views": message_views, "message_sent": message_sent, "message_text": message_text, "message_fwd_from_name": message_fwd_from_name, "message_fwd_from_link": message_fwd_from_link, "message_link_preview": message_link_preview, "prev_link_site": prev_link_site, "prev_link_title": prev_link_title, "prev_link_description": prev_link_description, "prev_link_image": prev_link_image, "message_photo_link" : message_photo_link, "message_video" : message_video, "message_round_video": message_round_video, "message_video_link" :message_video_link}
    df_bubbles_data = pd.DataFrame(data = bubble_data)  
    # print(path_to_save_at)
    df_bubbles_data.to_csv(PATH_TO_SAVE_AT, mode = "a", header = False)
    # print("iiiiiiiiiiiiiii")

def get_page_link(page, base_page):
    base_page = re.sub(r"[\\?]before.*$", "", base_page)
    # print(base_page)
    message_nr = [] 
    bubbles = page.find_all("div", {"class":"tgme_widget_message_wrap js-widget_message_wrap"})
    for bubble in bubbles:
        message_nr_raw = bubble.find("div", {"class": "tgme_widget_message"})["data-post"]
        message_nr_cleaned = int(re.findall(r"\d{1,}$", message_nr_raw)[0])
        message_nr.append(message_nr_cleaned)

    # print("xxxxxxxxxxxxxxx")
    oldest_message_index = min(message_nr)
    # print("oldest message scraped: " + str(oldest_message_index))

    if oldest_message_index > MAX_NUMBER:
        new_link = base_page + "?before=" + str(oldest_message_index)
    else:
        new_link = None
    
    print(new_link)
    return (new_link)

def get_server_response(link):
    # init_page = requests.get(link)
    # init_page.raise_for_status()
    # # if status_code == 500:
    # #     sleep(10)
    # #     get_server_response(link)
    # init_page = init_page.text.encode("utf-8")
    with open(link) as fp:
        contents = fp.read()
        page = BeautifulSoup(contents, "lxml")

    # page = BeautifulSoup(link, "lxml")
    page.prettify() 
    return page

iterate_files()

