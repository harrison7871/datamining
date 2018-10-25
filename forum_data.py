from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import requests
import time
    
def text(soup):
    text = soup.find_all("blockquote", class_="postcontent restore")
    for body in text:
        return (body.text)
        
def next_page(url):
    source_code = requests.get(url)
    time.sleep(3)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")
    nextpage = soup.findAll("a", rel="next")
    for nextt in nextpage:
        return(nextt.get('href'))

def titles(soup):
    nextpage = soup.findAll("a", class_="title")
    title = []
    for nextt in nextpage:
        print(nextt.text)
        title.append(nextt.text)
    
    return title

def get_link(soupstuff, web):
    '''Input
    ============================================================================================
    soupstuff = the location of all the forum click
    web = just a empty list to save all the link found
    ============================================================================================
    Output
    ============================================================================================
    List with all the links
    ============================================================================================
    '''
    for forum_title in soupstuff:
        if 'Sticky' in forum_title.text:
            continue
        else:
            for link in forum_title("a"):
                if link == None:
                    continue
                print(link.get('href'))
                web.append(link.get('href'))
    return web
# =============================================================================
#         for i in nextt("a"):
#             if i == None:
#                 continue
#             print(i.get('href'))
#         return(i.get('href'))
# =============================================================================
            