from dotenv import load_dotenv
load_dotenv()

import os
import sys
import time

from selenium import webdriver
driver = webdriver.Firefox()

# Sign in to LinkedIn and navigate to the desired company's personnel
driver.get('https://www.linkedin.com')
assert "LinkedIn" in driver.title
sign_in = driver.find_element_by_partial_link_text('Sign in')
sign_in.click()
username = driver.find_element_by_id('username')
username.send_keys(os.getenv("LINKEDIN_USERNAME"))
password = driver.find_element_by_id('password')
password.send_keys(os.getenv("LINKEDIN_PASSWORD"))
password.submit()
url = sys.argv[1]
time.sleep(3)
driver.get(url + '/people')

# Scroll down the whole page
SCROLL_PAUSE_TIME = 2
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Scrape names
name_cards = driver.find_elements_by_class_name('org-people-profile-card__profile-title')
names = []
for card in name_cards:
    first_name = card.text.split()[0]
    names.append(first_name)

linkedin_employee_count = driver.find_element_by_class_name('t-20').text
driver.close()

print('Number of names found: ' + str(len(names)))
print('Number of names according to LinkedIn: "' + linkedin_employee_count + '"')