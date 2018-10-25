from selenium import webdriver
from bs4 import BeautifulSoup, SoupStrainer
# from selenium.webdriver.common.keys import Keys
import requests
import time
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
start_time = time.time()


driver = webdriver.Chrome()
driver.get("https://www.telescopesplus.com/pages/celestron-telescopes")
time.sleep(3)
# soupstrainerr = SoupStrainer('a', {'class'='view-all'})
soup = BeautifulSoup(driver.page_source, 'lxml')
# elems = driver.find_elements_by_xpath("//h2[@class='forumtitle']")
view_all = soup.find_all("a", class_="view-all")


def model_name(soup):
    model = soup.find("h1", itemprop="name")
    return model.text


def specs(soup):
    """
    Return a dict with subtitle: description
    """
    subtitle = soup.find_all("h4")
    description = soup.find_all("p")
    spec = []
    des = []
    y = {}
    if len(subtitle) == 0 or len(description) == 0:
        y['Details and specifications'] = "None specify"
    else:
        for i in subtitle:
            hey = i.text
            hey = hey.replace('\n', '')
            spec.append(hey)

        for j in description:
            k = j.text
            hi = k.replace('  ', '')
            des.append(hi)

        y = {spec[i]: des[i] for i in range(len(des))}

    print(y)
    return y


def old_spec(soup):
    description = soup.find_all("li")
    y = {}
    if len(description) == 0:
        y['Details and specifications'] = "None specify"

    else:
        for i in description:
            dj = i.text
            dj = dj.replace('\n', '')
            if ':' not in dj:
                continue
            j = dj.split(':')
            keys, value = j[0], j[1]  # this create a bunch of dicts
            y[keys] = value

    print(y)
    return y


web = []

for sub_links in view_all:  # this will grab link to view telescopes for each types
    sub = sub_links.get('href')
    links = "https://www.telescopesplus.com" + sub
    web.append(links)

models_name = []
specifications = []
dictionary = {}
titles = []

for i in web:
    driver.get(i)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    title = soup.find_all("a", class_="product-wrapper")  # get the link of each telescope model
    titles.append(title)
    for i in title:
        link = "https://www.telescopesplus.com" + str(i.get('href'))
        try:
            source_code = requests.get(link)
        except:
            time.sleep(10)
            try:
                source_code = requests.get(link)
            except:
                print("Connection error")
                break
        time.sleep(5)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'lxml')
        soups = BeautifulSoup(plain_text, 'lxml', parse_only=SoupStrainer('div', {'class': 'specs row'}))
        models_name.append(model_name(soup))  # grab the model number
        print("Looking at model: {}".format(model_name(soup)))
        try:
            if len(soups) == 1:
                dictionary['Details and specifications'] = "None specify"
                print(dictionary)
                specifications.append(dictionary)
            elif soups.find("p").text == '\n' or len(soups.find("p").text) == 2:
                dands = old_spec(soups)
                specifications.append(dands)
            else:
                sandd = specs(soups)
                specifications.append(sandd)
        except Exception as e:
            print(e)
            sd = old_spec(soups)
            specifications.append(sd)

keys, values = [], []
models = []
for dictionary in specifications:
    for j in dictionary.keys():
        keys.append(j)  # long list of keys in string
    for k in dictionary.values():
        values.append(k)  # long list of values in string

for i in range(len(models_name)):
    for j in range(len(specifications[i])):
        models.append(models_name[i])

new = []
modell = []
for abc in models:
    y = abc.rpartition('-')[0]
    modell.append(y)
    
for k in range(len(models)):
    data = [str(modell[k]), keys[k], values[k]]
    new.append(data)

df = pd.DataFrame(new)
df.to_csv('Celestron telescope.csv', sep='\t')
df.to_sql('Telescope_specs', con=engine, if_exists='replace', index=False,
          dtype = {'telescopes': sqlalchemy.types.VARCHAR(length=255),
                   'specifications': sqlalchemy.types.VARCHAR(length=255),
                   'descriptions': sqlalchemy.types.VARCHAR(length=255)})
# print(spec)
# print(models_name)
# =============================================================================
# df1 = pd.DataFrame(models_name)
# df2 = pd.DataFrame(spec) #problem cuz spec is a mixture of list and dict
# df = pd.DataFrame({})
# =============================================================================
# =============================================================================
# df = pd.DataFrame(
#         {'Model name': models_name,
#          'Specifications': specifications,
#          'Descriptions': descriptions})
#
# df.to_csv('Telescope models and specs.csv', sep = '\t')
# df.merge(dff, how="outer")
# df.set_index('Model name')
# =============================================================================

print("--- %s seconds ---" % (time.time() - start_time))
print("We have looked at {} models".format(len(models_name)))
# not sure why I keep getting different model number
# =============================================================================
# for i in web:
#     model = model_name(i)
#     print(model)
# =============================================================================

driver.close()
