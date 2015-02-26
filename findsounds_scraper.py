''' Scraper for sound samples from findsounds.com'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import wget

file_names = []
j = 0 #File name is an index

def getNextPageElement( driver ):
    for k in driver.find_elements_by_tag_name("input"):
        if( k.get_attribute("value") == "Next Page" ):
            return k
    return None

if __name__=='__main__':
    query = input("Enter the keyword : ")
    driver = webdriver.Chrome()
    driver.get("http://www.findsounds.com/ISAPI/search.dll")
    keyw = driver.find_element_by_name("keywords")
    keyw.send_keys(query)
    keyw.send_keys(Keys.RETURN)
    next_page = getNextPageElement(driver)

    while( next_page ):
        elems = driver.find_elements_by_tag_name("a")
        for i in elems:
            filename = re.match( "(http://.*)?(?P<url>http://.*\.wav)", r""+str( i.get_attribute("href") ) )
            if( filename ):
                f = filename.group("url")
                if f not in file_names:
                    try:
                        j = j+1
                        wget.download(f,str(j)+".wav")
                        file_names.append(f)
                    except:
                        print("\nError downloading "+f)
                        j = j-1
        next_page.click()
        next_page = None
        next_page = getNextPageElement(driver)

    driver.close()

