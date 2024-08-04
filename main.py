from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Importing the urls
piteå = 'https://www.hemnet.se/bostader?item_types%5B%5D=villa&item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=18015&page={page}'
älsvbyn = 'https://www.hemnet.se/bostader?item_types%5B%5D=radhus&item_types%5B%5D=villa&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=17834&page={page}'
boden = 'https://www.hemnet.se/bostader?item_types%5B%5D=villa&item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=17879&page={page}'
luleå = 'https://www.hemnet.se/bostader?item_types%5B%5D=villa&item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=18045&page={page}'

# ======================== Get the data from the website ========================

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)

lock = False
titles = []
prices = []
locations = []
sizes = []
rooms = []
yards = []
page_nums = ['1']

def get_page_data(url, page_number):
    url = url.format(page=page_number)
    driver.get(url)
    time.sleep(5)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    ads = soup.find_all('a', class_='hcl-card')
    try: 
        page_num = soup.find('div', class_='hcl-pagination-items').text.strip()
        page_nums.append(page_num)
    except:
        page_num = None
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

        try:
            yard = ad.find('span', class_='ForSaleAttributes_secondaryAttributes__ko6y2').text.strip()
            yard = yard.replace('tomt', '').strip()
            yard = yard.replace('\xa0', '').strip()
            if 'kr' in yard:
                yard = None
        except:
            yard = None

        titles.append(title)
        prices.append(price)
        locations.append(location)
        sizes.append(size)
        rooms.append(room)
        yards.append(yard)

def get_last_number_from_list(lst):
    global lock
    if not lock:
        try:
            last_element = lst[-1]
            dot_index = last_element.rfind('...')
            if dot_index != -1:
                print("dot_index", dot_index)
                number_str = last_element[dot_index + 3 :]
                lock = True
                return int(number_str)
            else:
                return int(last_element[-1])
        except Exception as e:
            print(f"Error in get_last_number_from_list: {e}")
            return 0  # Return a default value in case of error
    else:
        return last_number

last_number = get_last_number_from_list(page_nums)
current_page = 1
while current_page <= last_number:
    get_page_data(luleå + '&page=' + str(current_page), current_page)
    last_number = get_last_number_from_list(page_nums)
    current_page += 1
    print(page_nums)
    print("Current page  ",current_page)
    print(last_number)



print(titles)
# print("")
# print(prices)
# print("")
# print(locations)
# print("")
# print(sizes)
# print("")
# print(rooms)
# print("")
# print(yards)
# print("")
# print(page_nums)