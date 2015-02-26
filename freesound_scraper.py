''' Scraper to extract sounds from freesound.org'''
''' Requires user auth'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import wget
import traceback
import time
links = []
next_page = None
def get_audio( driver, url ):
    '''To download sound sample. Will download to downloads directory'''
    driver.get(url)
    download = driver.find_element_by_id("download_button")
    try:
        download.click()
    except:
        print("\nError downloading file")
        print(traceback.format_exc())
    return

print("For findsound.org")
usr = input("Enter your username : ")
pas = input("Enter your password : ")
query = input("Enter keyword to search : ")
driver = webdriver.Chrome()
driver.get("https://www.freesound.org/home/login/?next=/")
username = driver.find_element_by_name("username")
passwd = driver.find_element_by_name("password")
username.send_keys(usr)
passwd.send_keys(pas)
passwd.send_keys(Keys.RETURN)

search_word = query
q = driver.find_element_by_name("q")
q.send_keys(search_word)
q.send_keys(Keys.RETURN)
search_url = "https://www.freesound.org/search/?q="+search_word

while( True ):
    elems = driver.find_elements_by_tag_name("a")
    '''Find all links to download and append them to a list'''
    for elem in elems:
        if( elem.get_attribute("class") == "title" ):
            links.append(elem.get_attribute("href"))
    '''Download all the links in the list'''
    for i in links:
        driver.get(i)
        get_audio(driver, i)
        driver.back()

    '''Find the Next page button and navigate to the next page'''
    driver.get(search_url)
    elems = driver.find_elements_by_tag_name("a")
    for j in elems:
        if( j.get_attribute("title") == "Next Page" ):
            next_page = j
    if next_page is None:
        print("Breaking")
        break
    search_url = next_page.get_attribute("href")
    driver.get(search_url)
    next_page = None
    '''Clear the list'''
    l = []

driver.close()
