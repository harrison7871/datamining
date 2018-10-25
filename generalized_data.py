import requests
from bs4 import BeautifulSoup

header = {}
#duplicate need to be solved
#efficiency
#code seems forced, lookup more website to generalized the download code
#improve it so it could download all files in multiple pages
forbidden = ["?", "<", ">", "*", ",", "=", ":", ";", "[", "]", "|"]

def download_file(url):
    local_filename = url.split('/')[-1]
    for characters in forbidden:
        if characters in local_filename:
            local_filename = local_filename.replace(characters, "")
    local_filename = local_filename.partition("jpg")[0] + "jpg"
    print("Downloading {} ---> {}".format(url, local_filename))
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename

def Download_Image_from_Web(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for link in soup.findAll('a'):
        image_links = link.get('href')
        if image_links is None:
            continue
        if not image_links.startswith('http'):
            if 'gif' in image_links:
                image_links = image_links.split('..')[-1]
                image_links = "http://www.eso.org/~tcsmgr/vlti/atcsdoc" + image_links
                download_file(image_links)
            if 'pdf' in image_links:
                image_links = url.split('/')[2] + '/' + image_links
                download_file(image_links)
    for link in soup.findAll('img'):
        image_links = link.get('src')
        if not image_links.startswith('http'):
            image_links = 'http:' + image_links
        download_file(image_links)


Download_Image_from_Web("https://www.celestron.com/collections/astronomy#")