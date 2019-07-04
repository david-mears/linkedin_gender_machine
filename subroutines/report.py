def report(
        company_name,
        names_response,
        null_count,
        gender_tally_dict,
        gender_percent_dict,
        linkedin_employee_count,
    ):
    print()
    title = company_name + ' Report'
    underline = ''
    for char in title: underline += '-'
    print(title)
    print(underline)
    print('  Number of names found: ' + str(len(names_response)))
    if linkedin_employee_count != None:
        print('  Number of names according to LinkedIn: ' + str(linkedin_employee_count))
    print('  Number of names of unknown gender: ' + str(null_count))
    print('\nEstimated gender tally:')
    for key in gender_tally_dict:
        print('  %s:  %.2f (%d%%)' % (key.capitalize(), gender_tally_dict[key], gender_percent_dict[key]))
    print()