import pandas as pd
import requests
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import time
import pyautogui

def random_click():
    screen_width, screen_height = pyautogui.size()
    random_x = 1867
    random_y = 485
def click_jai(driver,xpath):
    if len(driver.find_elements(By.XPATH, xpath)) != 0:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    else:
        pass

def click_jai_class(driver,classn):
    if len(driver.find_elements(By.CLASS_NAME, classn)) != 0:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, classn))).click()
    else:
        pass

def get_flat_ids():
    all_data_ids = []
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    driver.get('https://krisha.kz/arenda/kvartiry/astana/?das[_sys.hasphoto]=1&das[who]=1')
    time.sleep(1)

    random_click()
    section_xpath = '/html/body/main/section[3]/div/section[1]'
    total_pages_xpath = '/html/body/main/section[3]/div/nav/a[9]'
    next_button_xpath = '/html/body/main/section[3]/div/nav/a[10]' 
    total_pages_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, total_pages_xpath)))
    total_pages = 10#int(total_pages_element.text.strip())  # Extract and convert the page number
    print(f"Total pages: {total_pages}")
    for page in tqdm(range(total_pages)):
        section_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, section_xpath)))
        div_elements = section_element.find_elements(By.TAG_NAME, 'div')
        data_ids = [div.get_attribute('data-id') for div in div_elements if div.get_attribute('data-id')]
        all_data_ids.extend(data_ids)
        print(f"Extracted {len(data_ids)} data-ids from page {page + 1}.")
        if page < total_pages - 1:
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
            next_button.click()
    return all_data_ids




def click_with_wait(driver, xpath, timeout=20):
    try:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
    except Exception as e:
        print(f"Error clicking element {xpath}: {e}")




def get_text(driver, xpath, timeout=20):
    try:
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return element.text
    except Exception as e:
        print(f"Error retrieving text from {xpath}: {e}")
        return None


def get_live_area(driver, xpath):
    al_text = get_text(driver, xpath)
    digits = ''.join([char for char in al_text if char.isdigit()]).replace(" ", '').split('²')

    if len(digits) < 2:
        print(f"Unable to determine live area from the given data: {al_text}")
        return None  
    try:
        gen_area = int(max(digits))
        live_area = gen_area - int(min(digits))
        return live_area
    except ValueError as e:
        print(f"Error calculating live area: {e}")
        return None  



def if_there_lift(driver, xpath):
    lift_text = get_text(driver, xpath)
    
    if lift_text is None:
        print(f"No text found at xpath: {xpath}")
        return False  
    if 'лифт' in lift_text.lower():
        return True
    else:
        return False

def get_number(driver, xpath_button, xpath_number):
    click_with_wait(driver, xpath_button)
    return get_text(driver,xpath_number)

def scrap_data(all_ids, center_coordinate=None):
    data = {
        "link": [],
        "address": [],
        "km_to_center": [],
        "gen_area": [],
        "room_amount": [],
        "live_area": [],
        "stage": [],
        "lift_exists": [],
        "WC": [],
        "kitchen_studio": [],
        "price": [],
        "date_arenda": [],
        "name_hoz": [],
        "tel_number": []
    }
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)

    for i in tqdm(all_ids):
        link = f'https://krisha.kz/a/show/{i}'
        driver.get(link)
        time.sleep(1)
        random_click()
        
        address_text = get_text(driver, '/html/body/main/div[2]/div/div[1]/h1')
        address = address_text.strip().split(',')[-1].split('—')[0].strip() if address_text else "N/A"
        data["address"].append(address)

        gen_area_text = get_text(driver, '/html/body/main/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[3]/div[3]')
        gen_area = ''.join([char for char in gen_area_text if char.isdigit()]) if gen_area_text else "N/A"
        data["gen_area"].append(gen_area)

        room_amount_text = get_text(driver, "/html/body/main/div[2]/div/div[1]/h1")
        room_amount = room_amount_text[0] if room_amount_text else "N/A"
        data["room_amount"].append(room_amount)
        
        live_area = get_text(driver, '/html/body/main/div[2]/div/div[1]/h1') or "N/A"
        data["live_area"].append(live_area)
        
        stage = get_text(driver, '/html/body/main/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div[3]') or "N/A"
        data["stage"].append(stage)
        
        lift_text = get_text(driver, '/html/body/main/div[2]/div/div[2]/div[2]/div[5]/div[2]/dl[2]/dd')
        lift_exists = "лифт" in lift_text.lower() if lift_text else False
        data["lift_exists"].append(lift_exists)
        
        wc_text = get_text(driver, '/html/body/main/div[2]/div/div[2]/div[2]/div[5]/div[2]/dl[3]/dd')
        data["WC"].append(wc_text or "N/A")
        
        data["kitchen_studio"].append("no")
        
        price_text = get_text(driver, '/html/body/main/div[2]/div/div[2]/div[1]/div[1]/div[1]/div')
        price = int(''.join([char for char in price_text if char.isdigit()])) if price_text else None
        data["price"].append(price)
        
        data["link"].append(link)
        data["date_arenda"].append("N/A")
        data["name_hoz"].append("N/A")
        data["tel_number"].append(None)

    driver.quit()
    
    max_length = len(data["link"])
    for key, value in data.items():
        while len(value) < max_length:
            value.append(None)  

    return data

all_data_ids = get_flat_ids()

scraped_data = scrap_data(all_data_ids)

df = pd.DataFrame(scraped_data)

df.to_csv(r'C:\Users\arlan\Desktop\Programming BIG DATA\assignment 2\data\data_new.csv', index=False, encoding='utf-8-sig')

