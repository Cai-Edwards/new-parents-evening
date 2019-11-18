'''Perform analysis on the parents evening timetable generated'''

from list_manipulation import convert_to_slots
import numpy

def find_bounds(timetable):
    minimum_slots = 0
    num_persons = 0
    minimum_latest = 1000
    minimum_duration = 0

    for p in timetable:

        person = [x for x in timetable[p] if x != 0]

        if len(person) < minimum_latest: minimum_latest = len(person)
        if len(person) > minimum_duration: minimum_duration = len(person)
        num_persons += 1

        minimum_slots += len(person)

    maximum_slots = minimum_slots * num_persons
    
    earliest_slot = 1
    latest_earliest = maximum_slots - minimum_latest

    return minimum_slots, minimum_duration, maximum_slots, minimum_latest, earliest_slot, latest_earliest

def slot_analysis(db):
    cursor = db.cursor()
    
    cursor.execute("select slot, count(slot) from relationships group by slot;")
    slot_distribution = [x[1] for x in cursor.fetchall()]
    
    return slot_distribution

def analyse(db, timetable):

    '''Analysis function. slotted timetable input
    
    {3:[0, 1, ... , 3], ... }'''

    slots_timetable = convert_to_slots(timetable)

    order = []
    all_earliest = []
    all_latest = []
    all_difference = []
    all_average_gap = []
    all_min_gap = []
    all_max_gap = []
    all_all_gaps = []
    change_average_difference = []

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

        change_average_difference.append(sum(all_difference)/len(order))
    
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

    total_time = sum(all_difference)

    minimum_slots, minimum_duration, maximum_slots, minimum_latest, earliest_slot, latest_earliest = find_bounds(timetable)

    slot_distribution = slot_analysis(db)

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
        "largest_average_gap":largest_average_gap,
        "change_average_difference":change_average_difference,
        "minimum_slots":minimum_slots,
        "minimum_duration":minimum_duration,
        "maximum_slots":maximum_slots,
        "minimum_latest":minimum_latest,
        "earliest_slot":earliest_slot,
        "latest_earliest":latest_earliest,
        "slot_distribution":slot_distribution,
        "total_time":total_time
    }

def individual_analysis(individual):
    '''Perform analysis for an individual person
    
    [0, 12, 0, 345, 0, 34, 0, 0 , 3]'''

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
