import sys

from example_response import example_response
from subroutines import get_gender_percent, report, scrape_web, show_bar_chart, tally_genders

PRIOR_PROBABILITY_OF_NULL_BEING_MALE = 0.5

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

gender_tally_dict, null_count, total = tally_genders.tally_genders(names_response, PRIOR_PROBABILITY_OF_NULL_BEING_MALE)
gender_percent_dict = get_gender_percent.get_gender_percent(gender_tally_dict, total)

report.report(
        company_name,
        names_response,
        null_count,
        gender_tally_dict,
        gender_percent_dict,
        linkedin_employee_count,
    )

show_bar_chart.show_bar_chart(gender_tally_dict, gender_percent_dict)

from random import random
male = 0
female = 0

for person in names_response:
    if person['gender'] == 'male':
        person['probability_of_being_male'] = person['probability']
    elif person['gender'] == 'null':
        person['gender'] = 'male'
        person['probability_of_being_male'] = PRIOR_PROBABILITY_OF_NULL_BEING_MALE
    else:
        person['probability_of_being_male'] = 1 - float(person['probability'])

NUMBER_OF_SIMULATIONS = 1000
populations_collection = []
for i in range(NUMBER_OF_SIMULATIONS):
    population = {
    'male': 0,
    'female': 0,
    }
    for person in names_response:
        randomized_probability = random() * float(person['probability_of_being_male'])
        if round(randomized_probability) == 1:
            population['male'] += 1
        else:
            population['female'] += 1
    population = tuple(population.values())
    populations_collection.append(population)

from matplotlib import pyplot as plt

male_outcomes_tally = {}
female_outcomes_tally = {}
for population in populations_collection:
    number_of_males = population[0]
    if number_of_males in male_outcomes_tally.keys():
        male_outcomes_tally[number_of_males] += 1
        # If not male, then female.
        female_outcomes_tally[population[1]] += 1
    else:
        male_outcomes_tally[number_of_males] = 1
        # If not male, then female.
        female_outcomes_tally[population[1]] = 1   

def define_axes():
    all_values = []
    for population in populations_collection:
        all_values.append(population[0])
        all_values.append(population[1])
    all_values.sort()
    sorted_values = all_values
    outcomes_tally = list(male_outcomes_tally.keys()) + list(female_outcomes_tally.keys())
    outcomes_tally.sort()
    plt.axis([0, sorted_values[-1], 0, 1.2*outcomes_tally[-1]])
define_axes()

plt.plot(list(male_outcomes_tally.keys()), list(male_outcomes_tally.values()), 'bo')
plt.plot(list(female_outcomes_tally.keys()), list(female_outcomes_tally.values()), 'mo')

plt.ylabel('Occurrences in %s simulated populations' % NUMBER_OF_SIMULATIONS)
plt.xlabel('Number of employees by gender')
plt.show()