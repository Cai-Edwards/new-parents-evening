import numpy
import math
import statistics

def analysis(timetable):
    o = overall(timetable)
    b = bounds(timetable)

    o.update(b)

    return o

def individual(time):

    earliest = time.index(next(slot for slot in time if slot != 0)) + 1
    latest = len(time)
    difference = latest - earliest
    median = math.floor((difference + 1)/2)

    current_gap = 0
    gaps = []

    for slot in range(len(time)):
        if time[slot] != 0:
            gaps.append(current_gap)
            current_gap = 0
        else:
            current_gap += 1
    
    gaps.pop(0)


    smallest_gap = min(gaps)
    longest_gap = max(gaps)
    average_gap = statistics.mean(gaps)
    sd_gap = statistics.stdev(gaps)

    return {
        "earliest":earliest,
        "latest":latest,
        "difference":difference,
        "median":median,
        "smallest_gap":smallest_gap, 
        "longest_gap": longest_gap,
        "average_gap": average_gap,
        "sd_gap": sd_gap
    }

def bounds(timetable):
    data = {}
    data['minimum_length'] = 0

    for p in timetable:

        person = [x for x in timetable[p] if x != 0]

        if len(person) > data['minimum_length']: data['minimum_length'] = len(person)

    return data


def overall(timetable):
    
    all_earliest = []
    all_latest = []
    all_median = []
    all_difference = []
    smallest_gaps = []
    longest_gaps = []
    average_gaps = []
    sd_gaps = []

    names = ['all_earliest', 'all_latest', 'all_median', 'all_difference', 
            'smallest_gaps', 'longest_gaps', 'average_gaps', 'sd_gaps']

    stats = [all_earliest, all_latest, all_median, all_difference,
            smallest_gaps, longest_gaps, average_gaps, sd_gaps]

    for person in timetable:
        data = individual(timetable[person])

        num = 0
        for d in data:
            stats[num].append(data[d])
            num += 1

    values = {}
    values['slot_distribution'] = [len([timetable[x][i] for x in timetable if i < len(timetable[x])
    and timetable[x][i] != 0]) for i, e in enumerate(timetable[max(timetable, key=lambda x: len(timetable[x]))])]

    for data, name in zip(stats, names):
        values[name] = [min(data), max(data), 
                        statistics.mean(data), statistics.stdev(data)]

    return values