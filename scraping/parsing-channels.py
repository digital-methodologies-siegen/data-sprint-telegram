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
import pathlib

path_html_sites = "../data/"
PATH_TO_SAVE_AT = "../data/parsed"
NAME_TO_SAVE = "parsed-data.csv"

### first function to be called:

def iterate_files():

    # init the dataframe column names, it's getting filled later on with data 
    df_init = pd.DataFrame({"message_nr": [], "message_user": [], "message_sent": [], "message_reply_to_nr": [], "message_text": [], "message_has_photo": [], "message_photo_link": [], "message_has_video": [], "message_video_link" :[], "parsed_file": []})

    pathlib.Path(PATH_TO_SAVE_AT).mkdir(parents=True, exist_ok=True)

    df_init.to_csv(PATH_TO_SAVE_AT + "/" + NAME_TO_SAVE, mode = "w")
    
    for html_file in pathlib.Path(path_html_sites).rglob('*.html'):
        print(html_file)
        get_channel(html_file)
   

def get_channel(file_path):
    
    page = get_server_response(file_path)
    print("xxxxxxxxxxxxx " + str(file_path))
    # print(page)

    bubble_data = []
    bubbles = page.find_all("div", {"class":"message default clearfix"})
    # print(bubbles)
    message_nr=[]
    message_user=[]
    message_text = []
    # message_views = []
    message_sent = []
    message_reply_to_nr = []
    # message_fwd_from_name = []
    # message_fwd_from_link = []
    # message_link_preview = []
    # message_round_video = []
    message_has_video = []
    # message_video = []
    message_video_link = []
    # prev_link_site = []
    # prev_link_title = []
    # prev_link_description = []
    # prev_link_image = []
    message_has_photo = []
    message_photo_link = []
    parsed_file = []

    

    for bubble in bubbles:
        
        parsed_file.append(file_path)

        message_nr_raw = bubble["id"]
        message_nr.append(re.findall(r"\d{1,}$", message_nr_raw)[0])
        body = bubble.find("div", {"class": "body"})

        # print(re.findall(r"\d{1,}$", message_nr_raw)[0])
        message_sent.append(body.find("div", {"class": "pull_right date details"})["title"])
        message_user.append(body.find("div", {"class": "from_name"}).text)
        
        has_text = bubble.find("div", {"class": "text"})
        if has_text != None:
            message_text.append(has_text.text)
        else:
            message_text.append("NA")

        is_answer = body.find("div", {"class": "reply_to details"})
        if is_answer != None:
            link = is_answer.find("a")["href"]
            message_reply_to_nr.append(re.findall(r"\d{1,}$", link)[0])
        else:
            message_reply_to_nr.append("NA")
            
        photo_linked = bubble.find("a", {"class" : "photo_wrap"})
        if photo_linked != None:
            message_photo_link.append(photo_linked["href"])
            message_has_photo.append("TRUE")
        else:
            message_photo_link.append("NA")
            message_has_photo.append("FALSE")

        contains_video = bubble.find("a", {"class": "video_file_wrap"})
        if contains_video != None:
            message_video_link.append(contains_video["href"])
            message_has_video.append("TRUE")
        else:
            message_video_link.append("NA")
            message_has_video.append("FALSE")

    # bubble_data = {"message_nr": message_nr, "message_user": message_user, "message_sent": message_sent, "message_text": message_text, "message_fwd_from_name": message_fwd_from_name, "message_fwd_from_link": message_fwd_from_link, "message_link_preview": message_link_preview, "prev_link_site": prev_link_site, "prev_link_title": prev_link_title, "prev_link_description": prev_link_description, "prev_link_image": prev_link_image, "message_photo_link" : message_photo_link, "message_video" : message_video, "message_round_video": message_round_video, "message_video_link" :message_video_link}
    bubble_data = {"message_nr": message_nr, "message_user": message_user, "message_sent": message_sent, "message_reply_to_nr": message_reply_to_nr, "message_text": message_text, "message_has_photo": message_has_photo, "message_photo_link": message_photo_link, "message_has_video": message_has_video, "message_video_link" :message_video_link, "parsed_file": parsed_file}
    df_bubbles_data = pd.DataFrame(data = bubble_data)  
    # print(path_to_save_at)
    df_bubbles_data.to_csv(PATH_TO_SAVE_AT + "/" + NAME_TO_SAVE, mode = "a", header = False)

def get_server_response(link):
    with open(link) as fp:
        contents = fp.read()
        page = BeautifulSoup(contents, "lxml")

    page.prettify() 
    return page

iterate_files()

