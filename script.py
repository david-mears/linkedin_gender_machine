from decimal import Decimal, getcontext
import os
import sys
import time

from dotenv import load_dotenv
from genderize import Genderize
from selenium import webdriver

try:
    sys.argv[1]
except:
    from example_response import example_response
    names_response = example_response
    company_name = 'Example Company'
else:
    url = sys.argv[1]

try:
    example_response
except:
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

# Tally genders
PRIOR_PROBABILITY_OF_NULL_BEING_MALE = 0.5
gender_tally_dict = {
    'male': 0,
    'female': 0,
}

total = 0
null_count = 0
for person in names_response:
    total += 1

    if person['gender'] == 'null':
        null_count += 1
        gender_tally_dict['male'] += PRIOR_PROBABILITY_OF_NULL_BEING_MALE
        gender_tally_dict['female'] += (1-PRIOR_PROBABILITY_OF_NULL_BEING_MALE)
    else:
        gender_tally_dict[person['gender']] += float(person['probability'])

gender_percent_dict = {}
for gender in gender_tally_dict:
    gender_percent_dict[gender] = 100 * (gender_tally_dict[gender]/total)

# Convert tally dictionary to two sig figs
getcontext().prec = 3
for key in gender_tally_dict:
    gender_tally_dict[key] = float(
        Decimal(gender_tally_dict[key]) / Decimal(1)
    )

# Report

print()
title = company_name + ' Report'
underline = ''
for char in title: underline += '-'
print(title)
print(underline)

print('  Number of names found: ' + str(len(names_response)))
try:
    url
except:
    pass
else:
    print('  Number of names according to LinkedIn: ' + str(linkedin_employee_count))
print('  Number of names of unknown gender: ' + str(null_count))

print('\nEstimated gender tally:')
for key in gender_tally_dict:
    print('  ' + key.capitalize() + ': '
    + str(gender_tally_dict[key])
    + ' ('
    + str(int(gender_percent_dict[key]))
    + '%)')
print()
       
