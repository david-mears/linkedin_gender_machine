from random import random
from matplotlib import pyplot as plt


def convert_gender_odds_to_male_odds(names_response, prior):
    for person in names_response:
        if person['gender'] == 'male':
            person['probability_of_being_male'] = person['probability']
        elif person['gender'] == 'null':
            person['gender'] = 'male'
            person['probability_of_being_male'] = prior
        else:
            person['probability_of_being_male'] = 1 - \
                float(person['probability'])
    return names_response


def define_axes(
        populations_collection,
        male_outcomes_tally,
        female_outcomes_tally):
    all_values = []
    for population in populations_collection:
        all_values.append(population[0])
        all_values.append(population[1])
    all_values.sort()
    sorted_values = all_values
    outcomes_tally = sorted(
        list(
            male_outcomes_tally.keys()) +
        list(
            female_outcomes_tally.keys()))
    plt.axis([0, sorted_values[-1], 0, 1.2 * outcomes_tally[-1]])


def run_simulations(number_of_simulations, names_response):
    populations_collection = []
    for i in range(number_of_simulations):
        population = {
            'male': 0,
            'female': 0,
        }
        for person in names_response:
            randomized_probability = random(
            ) * float(person['probability_of_being_male'])
            if round(randomized_probability) == 1:
                population['male'] += 1
            else:
                population['female'] += 1
        population = tuple(population.values())
        populations_collection.append(population)
    return populations_collection


def get_outcomes_tallies_by_gender(populations_collection):
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
    return male_outcomes_tally, female_outcomes_tally

def show_histogram(names_response, prior):
    NUMBER_OF_SIMULATIONS = 1000
    names_response = convert_gender_odds_to_male_odds(names_response, prior)
    populations_collection = run_simulations(
        NUMBER_OF_SIMULATIONS, names_response)
    male_outcomes_tally, female_outcomes_tally = get_outcomes_tallies_by_gender(
        populations_collection)
    define_axes(
        populations_collection,
        male_outcomes_tally,
        female_outcomes_tally)

    plt.plot(
        list(
            male_outcomes_tally.keys()), list(
            male_outcomes_tally.values()), 'bo')
    plt.plot(
        list(
            female_outcomes_tally.keys()), list(
            female_outcomes_tally.values()), 'mo')
    plt.ylabel(
        'Occurrences in %s simulated populations' %
        NUMBER_OF_SIMULATIONS)
    plt.xlabel('Number of employees by gender')
    plt.show()
