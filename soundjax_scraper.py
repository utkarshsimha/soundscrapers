''' Scraper to get sound samples from soundjax.com'''
import requests
import re
import wget
from bs4 import BeautifulSoup

page_num = 2; #Index to next page
index = 1; #Index for file name
links = []
query = input("Enter your query : ")
url = "http://soundjax.com/?q="+query
soundjax = requests.get(url)
page = soundjax.text

while( re.search("No results found matching your search.",page) is None ):
    soup = BeautifulSoup(page)
    for i in soup.find_all("a"):
        m = re.match(r".*\"(?P<url>.*.\.(mp3|wav))", str(i))
        if m is not None:
            download_url = str(m.group("url"))
            download_url = download_url.replace("^","%5E")
            links.append(download_url)

    for i in links:
        try:
            wget.download("http://soundjax.com/"+str(i), str(index)+".wav")
            index+=1
        except:
            print("\nError downloading")
            index-=1

    soundjax = requests.get("http://soundjax.com/"+query+"-"+str(page_num)+".html")
    page_num+=1
    page = soundjax.text

soundjax.close()
