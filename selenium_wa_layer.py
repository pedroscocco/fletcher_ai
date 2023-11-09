import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time

GROUP_NAME = "Nóis"
TIMEOUT = 30

chrome_options = Options()
chrome_options.add_argument("user-data-dir=selenium")

service = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)
chat_window = None

def start_selenium():
    driver.get("https://web.whatsapp.com")

    # Find Search box and search group name
    search_box_locator = (By.XPATH, "//div[@title = 'Search input textbox']")
    input_box_search = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located(search_box_locator))
    input_box_search.click()
    time.sleep(1)
    input_box_search.send_keys(GROUP_NAME)
    # time.sleep(2)

    # Click the group that shows up
    contact_el_locator = (By.XPATH, "//span[@title='"+GROUP_NAME+"']")
    selected_contact = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located(contact_el_locator))
    selected_contact.click()

    # Wait for chat to load before returning
    global chat_window
    app_chat_locator = (By.XPATH, "//div[@role='application']")
    chat_window = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located(app_chat_locator))

    time.sleep(2)


# Wait for a new message in group
def wait_new_message_element():
    rows_locator = (By.XPATH, './/span[contains(@class, "selectable-text")]//ancestor::div[@role="row"]')
    get_row_count_func = lambda: len(chat_window.find_elements(*rows_locator))

    initial_row_count = get_row_count_func()

    # Wait until count increases
    WebDriverWait(driver, timeout=14400, poll_frequency=10).until(lambda x: get_row_count_func() > initial_row_count)

    # Return the new (last) message
    rows = chat_window.find_elements(*rows_locator)
    return rows[-1]

def get_message_details(message_row_element):
    # Get message text
    message_text = message_row_element.find_element(By.XPATH, './/span[contains(@class, "selectable-text")]').text

    # Get sender name
    date_and_sender = message_row_element.find_element(By.XPATH, './/div[@data-pre-plain-text]').get_attribute('data-pre-plain-text')
    
    date_time_regex = r"\[(\d{2}:\d{2}), (\d{1,2}/\d{1,2}/\d{4})\] (.*):"

    # Search the string for date and time
    match = re.search(date_time_regex, date_and_sender)

    # Extract the time and date from the match groups
    time_str, date_str, author = match.groups()

    # Combine the date and time strings
    date_time_str = f"{date_str} {time_str}"

    # Parse the date and time string into a datetime object
    date_time_obj = datetime.strptime(date_time_str, "%m/%d/%Y %H:%M")

    print(date_time_obj)

    return (date_time_obj, author, message_text)


# Figure out who are the group participants
# def find_group_participants():
#     pass

def send_message(message):
    # Find Message text box
    inp_xpath = '//div[@title="Type a message"][@role="textbox"]'
    input_box = driver.find_element('xpath', inp_xpath)
    time.sleep(2)

    # Message Group
    input_box.send_keys(message + Keys.ENTER)
    time.sleep(1)

def stop():
    driver.quit()
