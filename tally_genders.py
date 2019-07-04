from decimal import Decimal, getcontext

def tally_genders(names_response):
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

    # Convert tally dictionary to two sig figs
    getcontext().prec = 3
    for key in gender_tally_dict:
        gender_tally_dict[key] = float(
            Decimal(gender_tally_dict[key]) / Decimal(1)
        )

    return gender_tally_dict, null_count, total