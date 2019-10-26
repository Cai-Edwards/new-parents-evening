'''Perform analysis on the parents evening timetable generated'''

from list_manipulation import convert_to_slots
import numpy

def analyse(timetable):

    slots_timetable = convert_to_slots(timetable)

    order = []
    all_earliest = []
    all_latest = []
    all_difference = []
    all_average_gap = []
    all_min_gap = []
    all_max_gap = []
    all_all_gaps = []

    for person in slots_timetable:
        order.append(person)
        data = individual_analysis(slots_timetable[person])
        
        all_earliest.append(data[0])
        all_latest.append(data[1])
        all_difference.append(data[2])
        all_average_gap.append(data[3])
        all_min_gap.append(data[4])
        all_max_gap.append(data[5])
        all_all_gaps.append(data[6])
    
    average_earliest = float(numpy.average(all_earliest))
    average_latest = float(numpy.average(all_latest))
    average_difference = float(numpy.average(all_difference))
    average_gap = float(numpy.average(all_average_gap))
    average_min_gap = float(numpy.average(all_min_gap))
    average_max_gap = float(numpy.average(all_max_gap))

    earliest_start = min(all_earliest)
    latest_start = max(all_earliest)

    earliest_end = min(all_latest)
    latest_end = max(all_latest)

    smallest_difference = min(all_difference)
    largest_difference = max(all_difference)

    smallest_average_gap = min(all_average_gap)
    largest_average_gap = max(all_average_gap)

    return {
        "order":order,
        "all_earliest":all_earliest,
        "all_latest":all_latest,
        "all_difference":all_difference,
        "all_average_gap":all_average_gap,
        "all_min_gap":all_min_gap,
        "all_max_gap":all_max_gap,
        "all_all_gaps":all_all_gaps,
        "average_earliest":average_earliest,
        "average_latest":average_latest,
        "average_difference":average_difference,
        "average_gap":average_gap,
        "average_min_gap":average_min_gap,
        "average_max_gap":average_max_gap,
        "earliest_start":earliest_start,
        "latest_start":latest_start,
        "earliest_end":earliest_end,
        "latest_end":latest_end,
        "smallest_difference":smallest_difference,
        "largest_difference":largest_difference,
        "smallest_average_gap":smallest_average_gap,
        "largest_average_gap":largest_average_gap
    }

def individual_analysis(individual):

    earliest = min(individual)
    latest = max(individual)
    difference = latest - earliest

    all_gaps = []

    for slot in range(len(individual)-1):
        gap = individual[slot+1] - individual[slot] - 1
        all_gaps.append(gap)

    average_gap = float(numpy.average(all_gaps))
    min_gap = min(all_gaps)
    max_gap = max(all_gaps)

    return [earliest, latest, difference, average_gap, min_gap, max_gap, all_gaps]
