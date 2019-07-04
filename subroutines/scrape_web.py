import os
import time

from dotenv import load_dotenv
from genderize import Genderize
from selenium import webdriver

def scrape_web(url):
    load_dotenv()
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
    company_name_list = url.split('/')[4].split('-')
    company_name = []
    for word in company_name_list: company_name.append(word.capitalize())
    company_name = ' '.join(company_name)

    time.sleep(3)
    if url[-1] != '/': url += '/'
    driver.get(url + 'people/')

    print('Successfully hacked into the main-frame.')

    # Get LinkedIn's own count of employees
    number_string = driver.find_element_by_class_name('t-20').text.split(' ')[0]
    linkedin_employee_count = int(''.join(number_string.split(',')))

    SCROLL_PAUSE_TIME = 2

    MAX_EMPLOYEE_COUNT = 200
    if linkedin_employee_count > MAX_EMPLOYEE_COUNT:
        print('Sorry: there are ' + str(linkedin_employee_count) + ' employees at this company.')
        print('To load all of them would take me ' + str((SCROLL_PAUSE_TIME * linkedin_employee_count)/60).split('.')[0] + ' minutes.')
        print('I will sample the first ' + str(MAX_EMPLOYEE_COUNT) + '-ish employees only.')
    # Scroll down the whole page
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

        # Break if enough employees found
        employees_found = len(driver.find_elements_by_class_name('org-people-profile-card__profile-title'))
        print('Employees found: ' + str(employees_found))
        if employees_found > MAX_EMPLOYEE_COUNT:
            break

    # Scrape names
    name_cards = driver.find_elements_by_class_name('org-people-profile-card__profile-title')
    names = []
    for card in name_cards:
        first_name = card.text.split()[0]
        names.append(first_name)

    # Close webdriver
    driver.close()

    # Make API request to Genderize 
    names_response = Genderize().get(names)

    return company_name, names_response, linkedin_employee_count