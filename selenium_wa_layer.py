import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time

drive = None

def start_selenium():
    global driver
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=selenium")

    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    group_name = "Nóis"

    driver.get("https://web.whatsapp.com")

    # Find Search box and search group name
    timeout = 10
    search_box_locator = (By.XPATH, "//div[@title = 'Search input textbox']")
    input_box_search = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(search_box_locator))
    input_box_search.click()
    time.sleep(2)
    input_box_search.send_keys(group_name)
    time.sleep(2)

    # Click the group that shows up
    contact_el_locator = (By.XPATH, "//span[@title='"+group_name+"']")
    selected_contact = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(contact_el_locator))
    selected_contact.click()
    time.sleep(3)

# Figure out who are the group participants
def find_group_participants():
    pass

def send_message(message):
    # Find Message text box
    inp_xpath = '//div[@title="Type a message"][@role="textbox"]'
    input_box = driver.find_element('xpath', inp_xpath)
    time.sleep(2)

    # Message Group
    input_box.send_keys(message + Keys.ENTER)
    time.sleep(1)

def stop():
    global driver
    driver.quit()
