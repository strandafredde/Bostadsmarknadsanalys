import time
import pandas as pd
import logging
import smtplib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from database import get_engine
from schema import Listings, UpdateLog, Base
from sqlalchemy.orm import sessionmaker
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Suppress SQLAlchemy logging
logging.getLogger('sqlalchemy').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy.engine').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy.pool').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy.dialects').setLevel(logging.CRITICAL)

# Define the URLs
urls = {
    'piteå': 'https://www.hemnet.se/bostader?item_types%5B%5D=villa&item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=18015&page={page}',
    'älsvbyn': 'https://www.hemnet.se/bostader?item_types%5B%5D=radhus&item_types%5B%5D=villa&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=17834&page={page}',
    'boden': 'https://www.hemnet.se/bostader?item_types%5B%5D=villa&item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=17879&page={page}',
    'luleå': 'https://www.hemnet.se/bostader?item_types%5B%5D=villa&item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt&item_types%5B%5D=fritidshus&location_ids%5B%5D=18045&page={page}',
}

# Initialize the Chrome driver
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")  # Disable sandbox for headless environments
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Disable logging
    chrome_options.add_argument("--log-level=3")  # Set logging level to OFF
    service = Service(executable_path='chromedriver.exe')
    return webdriver.Chrome(service=service, options=chrome_options)

driver = create_driver()

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
    time.sleep(2)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    
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

    # If the page number is greater than the last page number, return
    if page_number > total_pages:
        print("Page number is greater than the last page number, skipping...")
        return 
    
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
                ListingPrice_listingPrice__jg_CG
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
            yard = yard.replace('tomt', '').strip()
            yard = yard.replace('\xa0', '').strip()
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


        if title is not None:
            if titles not in titles:
                titles.append(title)
                prices.append(price)
                locations.append(location)
                sizes.append(size)
                rooms.append(room)
                yards.append(yard)

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


def send_email_alert(title, location, price, room, recipient_email):
    sender_email = "NyBostadsAnnons@outlook.com"
    sender_password = "hemnet-fyrkanten"
    smtp_server = "smtp.office365.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "New Listing Alert"

    body = f"Title: {title}\nLocation: {location}\nPrice: {price}\nRooms: {room}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Email sent successfully")
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Start scraping
current_page = 1

start_time = time.time()
while current_page <= 10:
    engine = get_engine('postgres', '1234', 'localhost', '5432', 'bostadsdata')

    Base.metadata.create_all(engine)

    
    print(f"Current page: {current_page}")
    get_page_data(urls['luleå'], current_page)
    get_page_data(urls['piteå'], current_page)
    get_page_data(urls['älsvbyn'], current_page)
    get_page_data(urls['boden'], current_page)
    current_page += 1
    

# print(titles)


Session = sessionmaker(bind=engine)
session = Session()

for title, price, location, size, room, yard in zip(titles, prices, locations, sizes, rooms, yards):
    listing = Listings(title=title, price=price, location=location, size=size, rooms=room, yard=yard)
    existing_listing = session.query(Listings).filter_by(title=listing.title).first()
    if existing_listing is None:
        session.add(listing)
        send_email_alert(title, location, price, room, 'strandafredde@gmail.com')
    else:
        print("======================================================================")
        print(f"Listing with the title {listing.title} already exists in the database")
        print("======================================================================")

UpdateTime = UpdateLog(execute_time=time.time() - start_time)
session.add(UpdateTime)
session.commit()
session.close()

driver.quit()

data = pd.DataFrame({
    'Title': titles,
    'Price': prices,
    'Location': locations,
    'Size': sizes,
    'Rooms': rooms,
    'Yard': yards
})

data.dropna(how='all', inplace=True)
data.to_csv('hemnet_data.csv', index=False)
print("time it took to run the script: ", time.time() - start_time)
