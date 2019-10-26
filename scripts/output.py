import csv
import matplotlib.pyplot as plt

def write(timetable, file):

    timetable = dictToList(timetable)

    with open(file, "w", newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(timetable)
    
    return "Done"

def visualise(analysis):

    print("""
    VALUES

    The earliest start is at slot: {}
    The latest start is at slot: {}

    The earliest end is at slot: {}
    The latest end is at slot: {}

    The smallest difference is a difference of: {}
    The largest difference is a difference of: {}

    The smallest average gap of a person is: {}
    The largest average gap of a person is: {}

    AVERAGES
    The average start slot was: {}
    The average end slot was: {}

    The average difference was: {}

    The average gap was: {}
    The average smallest gap was: {}
    The average largest gap was: {}
    """.format(str(analysis['earliest_start']), str(analysis['latest_start']),
    str(analysis['earliest_end']), str(analysis['latest_end']),
    str(analysis['smallest_difference']), str(analysis['largest_difference']),
    str(analysis['smallest_average_gap']), str(analysis['largest_average_gap']),
    str(analysis['average_earliest']), str(analysis['average_latest']),
    str(analysis['average_difference']), str(analysis['average_gap']),
    str(analysis['average_min_gap']), str(analysis['average_max_gap'])))

    fig, axs = plt.subplots(2, 2)

    axs[0,0].plot(analysis['all_earliest'])
    axs[0,0].set_ylabel("Earliest slot")
    axs[0,0].set_xlabel("People")

    axs[0,1].plot(analysis['all_latest'])
    axs[0,1].set_ylabel("Latest slot")
    axs[0,1].set_xlabel("People")

    axs[1,0].plot(analysis['all_difference'])
    axs[1,0].set_ylabel("Time spent at parents evening")
    axs[1,0].set_xlabel("People")

    axs[1,1].plot(analysis['all_average_gap'])
    axs[1,1].set_ylabel("The average gap length")
    axs[1,1].set_xlabel("People")

    fig2, axs2 = plt.subplots(1, 2)

    axs2[0].plot(analysis['all_min_gap'])
    axs2[0].set_ylabel("Minimum gap length")
    axs2[0].set_xlabel("People")

    axs2[1].plot(analysis['all_max_gap'])
    axs2[1].set_ylabel("Maximum gap length")
    axs2[1].set_xlabel("People")

    plt.show()

    return "Done"