from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import concurrent.futures
import pandas as pd

from database import get_engine
from schema import Listings, UpdateLog, Base
from sqlalchemy.orm import sessionmaker


# =============================================== Get Data ===============================================


# Define the URLs
urls = {
    'piteå': 'https://www.hemnet.se/bostader?item_types%5B%5D=villa&item_types%5B%5D=radhus&item _types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=18015&page={page}',
    'älsvbyn': 'https://www.hemnet.se/bostader?item_types%5B%5D=radhus&item_types%5B%5D=villa&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=17834&page={page}',
    'boden': 'https://www.hemnet.se/bostader?item_types%5B%5D=villa&item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=17879&page={page}',
    'luleå': 'https://www.hemnet.se/bostader?item_types%5B%5D=villa&item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=18045&page={page}',
}

# Initialize the Chrome driver (to be shared by all threads)
def create_driver():
    service = Service(executable_path='chromedriver.exe')
    return webdriver.Chrome(service=service)

# Scraping function
def get_page_data(url, page_number):
    results = {
        'titles': [],
        'prices': [],
        'locations': [],
        'sizes': [],
        'rooms': [],
        'yards': [],
    }

    driver = create_driver()
    try:
        url = url.format(page=page_number)
        driver.get(url)
        time.sleep(5)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract total number of pages
        try:
            page_num = soup.find('div', class_='hcl-pagination-items').text.strip()
            print(f'Page number!!!!!: {page_num}')
            page_nums = [int(num) for num in page_num.split() if num.isdigit()]
            print(f'Page numbers: {page_nums}')
            total_pages = get_last_number_from_list(page_nums)
            print(f'Total pages: {total_pages}')
        except:
            print('Failed to extract total number of pages for the current URL', url)
            total_pages = 1

        if page_number > total_pages:
            print(f'Page number {page_number} exceeds total pages {total_pages} Aborting to prevent unnecessary requests')
            return results  # Exit if the page number exceeds the total number of pages

        ads = soup.find_all('a', class_='hcl-card')

        for ad in ads:
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

                    if 'kr' in price:
                        try:
                            price = int(price.replace('kr', '').replace(' ', ''))
                        except ValueError:
                            price = None

                    if 'm²' in size:
                        size = size.replace('m²', '').replace(' ', '')
                        if '+' in size:
                            try:
                                parts = size.split('+')
                                size = sum(float(part.replace(',', '.')) for part in parts)
                            except ValueError:
                                size = None
                        else:
                            try:
                                size = float(size.replace(',', '.'))
                            except ValueError:
                                size = None

                    if 'rum' in room:
                        room = room.replace('rum', '').replace(' ', '')
                        if '+' in room:
                            try:
                                parts = room.split('+')
                                room = sum(float(part) for part in parts)
                            except ValueError:
                                room = None
                        else:
                            try:
                                room = float(room)
                            except ValueError:
                                room = None
                else:
                    price = size = room = None
            except:
                price = size = room = None

            try:
                yard = ad.find('span', class_='ForSaleAttributes_secondaryAttributes__ko6y2').text.strip()
                yard = yard.replace('tomt', '').strip().replace('\xa0', '')
                if 'kr' in yard:
                    yard = None
                elif 'm²' in yard:
                    try:
                        yard = float(yard.replace('m²', '').replace(' ', ''))
                    except ValueError:
                        yard = None
                elif 'ha' in yard:
                    try:
                        yard = int(float(yard.replace('ha', '').replace(' ', '').replace(',', '.')) * 10000)
                    except ValueError:
                        yard = None
                else:
                    yard = yard
            except:
                yard = None

            results['titles'].append(title)
            results['prices'].append(price)
            results['locations'].append(location)
            results['sizes'].append(size)
            results['rooms'].append(room)
            results['yards'].append(yard)

    finally:
        driver.quit()

    return results

# Existing logic for getting the last page number
def get_last_number_from_list(lst):
    lock = False #locking because you get the last page number on the first page
    global last_number
    if not lock:
        try:
            last_element = str(lst[-1])
            dot_index = last_element.rfind('...')
            if dot_index != -1:
                print("dot_index", dot_index)
                number_str = last_element[dot_index + 3 : ]
                lock = True
                last_number = int(number_str)
                return last_number
            else:
                last_number = int(last_element[-1])
                print("last_number¤!¤!¤¤!¤!", last_number)
                return last_number
        except Exception as e:
            print(f"Error in get_last_number_from_list: {e}")
            return 0  # Return a default value in case of error
    else:
        return last_number

# Aggregate results function
def aggregate_results(results_list):
    all_results = {
        'titles': [],
        'prices': [],
        'locations': [],
        'sizes': [],
        'rooms': [],
        'yards': [],
    }
    for results in results_list:
        for key in all_results:
            all_results[key].extend(results[key])
    return all_results

def main():


    engine = get_engine('postgres', '1234', 'localhost', '5432', 'bostadsdata')

    Base.metadata.create_all(engine)

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
            print(f'Adding new listing to the database')
            session.add(listing)

        # else:
        #     print(f'Listing with title {listing.title} already exists in the database. Skipping...')

    try:
        UpdateTime = UpdateLog() 
        session.add(UpdateTime)
    except Exception as e:
        print(f"Error in adding UpdateTime to the database: {e}")

    session.commit()
    session.close()


if __name__ == "__main__":
    main()


#TODO
# 1. Create database and store data in it - DONE
# 2. Create linux server to continuously run the script
# 3. Analyze data
