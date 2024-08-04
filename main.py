from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Importing the urls
piteå = 'https://www.hemnet.se/bostader?item_types%5B%5D=villa&item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=18015'
älsvbyn = 'https://www.hemnet.se/bostader?item_types%5B%5D=radhus&item_types%5B%5D=villa&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=17834'
boden = 'https://www.hemnet.se/bostader?item_types%5B%5D=villa&item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=17879'
luleå = 'https://www.hemnet.se/bostader?item_types%5B%5D=villa&item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=18045'

# ======================== Get the data from the website ========================

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)


titles = []
prices = []
locations = []
sizes = []
rooms = []
yards = []

def get_page_data(url):
    driver.get(url)
    time.sleep(5)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    ads = soup.find_all('a', class_='hcl-card')

    for ad in ads:
        #print(ad.prettify())
        try:
            title = ad.find('div', class_='Header_truncate__ebq7a').text.strip()
        except:
            title = None

        try:
            location = ad.find('div', class_='Location_address___eOo4').text.strip()
        except:
            location = None
        
        try:
            attributes = ad.find_all('span', class_='ForSaleAttributes_primaryAttributes__tqSRJ')
            if len(attributes) >= 3:
                price = attributes[0].text.strip().replace('\xa0', ' ')
                size = attributes[1].text.strip().replace('\xa0', ' ')
                room = attributes[2].text.strip().replace('\xa0', ' ')
            else:
                price = size = room = None
        except:
            price = size = room = None


        titles.append(title)
        prices.append(price)
        locations.append(location)
        sizes.append(size)
        rooms.append(room)

get_page_data(älsvbyn)

print(titles)
print("")
print(prices)
print("")
print(locations)
print("")
print(sizes)
