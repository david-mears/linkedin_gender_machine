import sys

from example_response import example_response
from subroutines import get_gender_percent, report, scrape_web
from subroutines import show_bar_chart, show_histogram, tally_genders

PRIOR_PROBABILITY_OF_NULL_BEING_MALE = 0.5

try:
    sys.argv[1]
except IndexError:
    URL = None
    linkedin_employee_count = None
    names_response = example_response
    company_name = 'Example Company'
else:
    URL = sys.argv[1]
    company_name,
    names_response,
    linkedin_employee_count = scrape_web.scrape_web(URL)

gender_tally_dict, null_count, total = tally_genders.tally_genders(
    names_response,
    PRIOR_PROBABILITY_OF_NULL_BEING_MALE
)
gender_percent_dict = get_gender_percent.get_gender_percent(
    gender_tally_dict,
    total
)

report.report(
    company_name,
    names_response,
    null_count,
    gender_tally_dict,
    gender_percent_dict,
    linkedin_employee_count,
)

show_bar_chart.show_bar_chart(gender_tally_dict, gender_percent_dict)

show_histogram.show_histogram(
    names_response,
    PRIOR_PROBABILITY_OF_NULL_BEING_MALE
)
