from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import concurrent.futures
import pandas as pd

<<<<<<< Updated upstream
# Importing the urls
piteå = 'https://www.hemnet.se/bostader?item_types%5B%5D=villa&item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=18015&page={page}'
älsvbyn = 'https://www.hemnet.se/bostader?item_types%5B%5D=radhus&item_types%5B%5D=villa&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=17834&page={page}'
boden = 'https://www.hemnet.se/bostader?item_types%5B%5D=villa&item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=17879&page={page}'
luleå = 'https://www.hemnet.se/bostader?item_types%5B%5D=villa&item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=18045&page={page}'
=======
from database import get_engine
from schema import Listings, Base
from sqlalchemy.orm import sessionmaker
>>>>>>> Stashed changes

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

                # Remove "kr" from price and convert to integer
                if 'kr' in price:
                    try:
                        price = int(price.replace('kr', '').replace(' ', ''))
                    except ValueError as e:
                        print(f"Price conversion failed: {e}")
                        price = None

                # Remove "m²" from size and handle addition
                if 'm²' in size:
                    size = size.replace('m²', '').replace(' ', '')
                    if '+' in size:
                        try:
                            parts = size.split('+')
                            size = sum(float(part.replace(',', '.')) for part in parts)
                        except ValueError as e:
                            print(f"Size conversion failed: {e}")
                            size = None
                    else:
                        try:
                            size = float(size.replace(',', '.'))
                        except ValueError as e:
                            print(f"Size conversion failed: {e}")
                            size = None

                # Remove "rum" from room and convert to integer
                if 'rum' in room:
                    room = room.replace('rum', '').replace(' ', '')
                    if '+' in room:
                        try:
                            parts = room.split('+')
                            room = sum(float(part) for part in parts)
                        except ValueError as e:
                            room = None
                    else:
                        try:
                            room = float(room)
                        except ValueError as e:
                            print(f"Room conversion failed: {e}")
                            room = None
            else:
                price = size = room = None
        except Exception as e:
            print(f"Room conversion failed: {e}")
            price = size = room = None


        try:
            yard = ad.find('span', class_='ForSaleAttributes_secondaryAttributes__ko6y2').text.strip()
            yard = yard.replace('tomt', '').strip()
            yard = yard.replace('\xa0', '').strip()
            if 'kr' in yard:
                yard = None
            elif 'm²' in yard:
                try:
                    yard = float(yard.replace('m²', '').replace(' ', ''))
                except ValueError as e:
                    print(f"Yard m² conversion failed: {e}")
                    yard = None
            elif 'ha' in yard:
                try:
                    yard = int(float(yard.replace('ha', '').replace(' ', '').replace(',', '.')) * 10000)
                except ValueError as e:
                    print(f"Yard ha conversion failed: {e}")
                    yard = None
            # If yard doesn't contain 'kr', 'm²', or 'ha', leave it unchanged
            else:
                yard = yard
        except Exception as e:
            print(f"Yard extraction failed: {e}")
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
                number_str = last_element[dot_index + 3 : ]
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

<<<<<<< Updated upstream

print("Titles: " , titles)
print("")
print("prices: " , prices)
print("")
print("locations: " , locations)
print("")
print("sizes: ", sizes)
print("")
print("rooms: ", rooms)
print("")
print("yards: ", yards)
=======
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {
            executor.submit(get_page_data, url, page): url
            for url in urls.values()
            for page in range(1, 6)  # Adjust page range as needed
        }

        results_list = []
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                results = future.result()
                results_list.append(results)
            except Exception as exc:
                print(f'Error occurred: {exc}')
    
    # Aggregate all results
    aggregated_results = aggregate_results(results_list)
    
    # Save to CSV
    data = pd.DataFrame(aggregated_results)
    data.to_csv('bostandsdata.csv', index=False)

    # Save to database
    Session = sessionmaker(bind=engine)
    session = Session()
    
    for i in range(len(aggregated_results['titles'])):
        listing = Listings(
            title=aggregated_results['titles'][i],
            price=aggregated_results['prices'][i],
            location=aggregated_results['locations'][i],
            size=aggregated_results['sizes'][i],
            rooms=aggregated_results['rooms'][i],
            yard=aggregated_results['yards'][i],
        )
        existing_listing = session.query(Listings).filter_by(title=listing.title).first()

        if not existing_listing and listing.title is not None:
            session.add(listing)

        else:
            print(f'Listing with title {listing.title} already exists in the database. Skipping...')



    session.commit()
    session.close()


if __name__ == "__main__":
    main()
>>>>>>> Stashed changes


# ======================== Save the data to a csv file ========================

data = pd.DataFrame({
    'Title': titles,
    'Price': prices,
    'Location': locations,
    'Size': sizes,
    'Rooms': rooms,
    'Yard': yards
})

data.to_csv('bostandsdata.csv', index=False)