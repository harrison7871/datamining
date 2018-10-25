from selenium import webdriver
from bs4 import BeautifulSoup, SoupStrainer
from selenium.webdriver.common.keys import Keys
import pandas as pd
import requests
import forum_data
import time
import sqlalchemy
from sqlalchemy import create_engine
start_time = time.time()


web = []
driver = webdriver.Chrome()
driver.get("http://www.astronomyforum.net/celestron-telescope-forums/")
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'lxml')

def text(soup):
    y = []
    body = soups.find_all("blockquote", class_="postcontent restore")
    if body == None:
        return y.clear()
    else:    
        for tess in body:
            hi = tess.text.strip()
            hii = hi.replace('\r\n', ' ')
            hiii = hii.replace('\n', ' ')
            y.append(hiii)
        return y

threadtitle = soup.find_all("h3", class_="threadtitle")
pages = soup.find_all("a", class_="popupctrl")
justwords = []
for i in pages:
    justwords.append(i.text)

words = justwords[-1]
last_pages = words.split(' ')[-1]
thread_links = []
titles = []
body_text, _main_ = [], []
for k in range(int(last_pages)-1): #range(int(last_pages))
    link = driver.current_url
    try:
        linkk = requests.get(link)
    except:
        print("==============================Connection error===================================")
        time.sleep(3)
        continue
    time.sleep(2)
    url = linkk.text
    #trial = SoupStrainer("h3", class_="threadtitle")
    soup = BeautifulSoup(url, "lxml")
    threadtitle = soup.find_all("h3", class_="threadtitle") #get the links from each catagories
    thread_link = forum_data.get_link(threadtitle) #make a list of all those links
    next_pages = soup.find_all("a", class_="title")
    for j in thread_link:
        print("looking at {}".format(j))
        try:
            source_code = requests.get(j)
            time.sleep(5)
        except:
            print("Connection error-=-=-=-=-=--=-=-=-=-=-=-=--")
            time.sleep(10)
            try:
                source_code = requests.get(j)
            except:
                pass
        plain_text = source_code.text
        soups = BeautifulSoup(plain_text, "lxml")
        title = soups.find("span", class_="threadtitle")
        if title == None:
            fix_title = "The site has been moved"
            print(fix_title)
            body_text = "N/A"
        else:
            fix_title = title.text.strip()
            print(fix_title)
            body_text = text(soups)
            
        titles.append(fix_title)
        print(body_text)
        _main_.append(body_text)
        print("=============================================================================================")
    try:
        driver.get(forum_data.next_page(link))
        time.sleep(3)
    except:
        print("=======================================Connection Error======================================")
        time.sleep(10)
        try:
            driver.get(forum_data.next_page(link))
            time.sleep(3)
        except:
            continue
        
main = "'" + "','".join(map(str, _main_))
datas = []
for s in range(len(titles)):
    data = [titles[s], str(_main_[s])]
    datas.append(data)
    
df = pd.DataFrame(datas)
df.columns = ['Thread titles', 'Thread text']
df.to_csv('Thread with text.csv')
df.to_sql(name='Thread_plus_text', con=engine, if_exists='replace', index=False,
          dtype = {'Thread titles': sqlalchemy.types.VARCHAR(length=255),
                   'Thread text': sqlalchemy.types.Text})

print("--- %s seconds ---" % (time.time() - start_time))
driver.close()
