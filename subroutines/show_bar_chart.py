from matplotlib import pyplot as plt

def show_bar_chart(gender_tally_dict, gender_percent_dict):
    heights = []
    for gender in gender_tally_dict:
        heights.append(gender_tally_dict[gender])
    x_labels = []
    for gender in gender_percent_dict:
        percent = gender_percent_dict[gender]
        x_labels.append(
            '%s (%d%%)' % (gender.capitalize(), percent)
        )
    plt.bar(x=x_labels,height=heights,color=['b','m'])
    plt.show()