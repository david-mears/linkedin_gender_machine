def get_gender_percent(gender_tally_dict, total):
    gender_percent_dict = {}
    for gender in gender_tally_dict:
        gender_percent_dict[gender] = 100 * (gender_tally_dict[gender] / total)
    # Convert percent dictionary to integers
    for key in gender_percent_dict:
        gender_percent_dict[key] = int(gender_percent_dict[key])
    return gender_percent_dict
