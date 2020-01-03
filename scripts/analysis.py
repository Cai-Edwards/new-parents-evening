'''Perform analysis on a timetable'''

import numpy
import math
import statistics

def analysis(timetable):
    '''Collate all the data calculated'''

    o = overall(timetable)
    b = bounds(timetable)

    o.update(b)

    s = score(o)
    o.update(s)

    return o


def score(overall):
    '''Generate a fitness value. lower is better'''

    score = 1
    score += sum(overall['all_difference']) - overall['minimum_slots']
    score += overall['data_difference'][0] - overall['minimum_difference']
    score += overall['data_difference'][1] - overall['minimum_difference']
    score += overall['data_longest_gaps'][0]*5 + overall['data_longest_gaps'][0]*5

    return {"score":score}


def individual(time):
    '''Calculate statistics based an a singular person'''

    data = {}

    data['earliest'] = [0, time.index(next(slot for slot in time if slot != 0)) + 1]

    data['latest'] = [1, len(time)]
    data['difference'] = [2, data['latest'][1] - data['earliest'][1] + 1]
    data['median'] = [3, math.floor((data['difference'][1] + 1)/2) + data['earliest'][1]]

    current_gap = 0
    gaps = []

    for slot in range(len(time)):
        if time[slot] != 0:
            gaps.append(current_gap)
            current_gap = 0
        else:
            current_gap += 1
    
    gaps.pop(0)

    data['smallest_gap'] = [4, min(gaps)]
    data['longest_gap'] = [5, max(gaps)]
    data['average_gap'] = [6, statistics.mean(gaps)]
    data['sd_gap'] = [7, statistics.stdev(gaps)]

    return data
def bounds(timetable):
    '''In an ideal scenario, what should values be'''

    if all(v == 0 for v in timetable) == True:
        return {}

    data = {}
    data['maximum_difference'] = 0
    data['minimum_difference'] = 10000
    data['minimum_slots'] = 0

    for p in timetable:

        person = [x for x in timetable[p] if x != 0]

        if len(person) > data['maximum_difference']: data['maximum_difference'] = len(person) 
        if len(person) < data['minimum_difference']: data['minimum_difference'] = len(person)  

        data['minimum_slots'] += len(person) 

    return data

def overall(timetable):
    '''Calculate general statistics for a whole timetable'''

    if all(v == 0 for v in timetable) == True:
        return {}
    
    all_earliest = []
    all_latest = []
    all_median = []
    all_difference = []
    smallest_gaps = []
    longest_gaps = []
    average_gaps = []
    sd_gaps = []

    names = ['data_earliest', 'data_latest', 'data_difference', 'data_median', 
            'data_smallest_gaps', 'data_longest_gaps', 'data_average_gaps',
            'data_sd_gaps']
    
    all_names = ["all_earliest", "all_latest", "all_difference", "all_median", 
                "smallest_gaps", "longest_gaps", "average_gaps", "sd_gaps"]

    stats = [all_earliest, all_latest, all_difference, all_median,
            smallest_gaps, longest_gaps, average_gaps, sd_gaps]

    for person in timetable:
        data = individual(timetable[person])

        for d in data:
            stats[data[d][0]].append(data[d][1])

    values = {}
    values['slot_distribution'] = [len([timetable[x][i] for x in timetable if i < len(timetable[x])
    and timetable[x][i] != 0]) for i, e in enumerate(timetable[max(timetable, key=lambda x: len(timetable[x]))])]

    for name, data in zip(all_names, stats):
        values[name] = data

    for data, name in zip(stats, names):
        values[name] = [min(data), max(data), 
                        statistics.mean(data), statistics.stdev(data)]

    return values