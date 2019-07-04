import sys

from example_response import example_response
from get_gender_percent import get_gender_percent
from report import report
from scrape_web import scrape_web
from show_bar_chart import show_bar_chart
from tally_genders import tally_genders

try:
    sys.argv[1]
except:
    url = None
    linkedin_employee_count = None
    names_response = example_response
    company_name = 'Example Company'
else:
    url = sys.argv[1]
    company_name, names_response, linkedin_employee_count = scrape_web(url)

gender_tally_dict, null_count, total = tally_genders(names_response)
gender_percent_dict = get_gender_percent(gender_tally_dict, total)

report(
        company_name,
        names_response,
        null_count,
        gender_tally_dict,
        gender_percent_dict,
        linkedin_employee_count,
    )

show_bar_chart(gender_tally_dict, gender_percent_dict)