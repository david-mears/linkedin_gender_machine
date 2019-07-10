from decimal import Decimal, getcontext


def tally_genders(names_response, prior):
    gender_tally_dict = {
        'male': 0,
        'female': 0,
    }

    total = 0
    null_count = 0
    for person in names_response:
        total += 1
        gender = person['gender']
        if gender == 'male':
            gender_tally_dict['male'] += float(person['probability'])
            gender_tally_dict['female'] += 1 - float(person['probability'])
        elif gender == 'female':
            gender_tally_dict['female'] += float(person['probability'])
            gender_tally_dict['male'] += 1 - float(person['probability'])
        else:
            null_count += 1
            gender_tally_dict['male'] += prior
            gender_tally_dict['female'] += (1 - prior)

    return gender_tally_dict, null_count, total
