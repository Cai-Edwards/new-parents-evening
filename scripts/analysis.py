import numpy
import math
import statistics

def analysis(timetable):

    o = overall(timetable)
    s = score(o)
    b = bounds(timetable)

    o.update(b)
    o.update(s)

    return o


def score(overall):

    score = (overall['data_longest_gaps'][0]*-1 + overall['data_longest_gaps'][1]*-2 + overall['data_longest_gaps'][2]*-5 + 
    overall['data_difference'][0]*1 + overall['data_difference'][2]*5 +
    overall['data_earliest'][1]*-3 + overall['data_sd_gaps'][1]*-10)*-1

    return {"score":score}


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

    if all(v == 0 for v in timetable) == True:
        return {}

    data = {}
    data['minimum_length'] = 0

    for p in timetable:

        person = [x for x in timetable[p] if x != 0]

        if len(person) > data['minimum_length']: data['minimum_length'] = len(person)

    return data


def overall(timetable):

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

    names = ['data_earliest', 'data_latest', 'data_median', 'data_difference', 
            'data_smallest_gaps', 'data_longest_gaps', 'data_average_gaps',
            'data_sd_gaps']
    
    all_names = ["all_earliest", "all_latest", "all_median", "all_difference",
                "smallest_gaps", "longest_gaps", "average_gaps", "sd_gaps"]

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

    for name, data in zip(all_names, stats):
        values[name] = data

    for data, name in zip(stats, names):
        values[name] = [min(data), max(data), 
                        statistics.mean(data), statistics.stdev(data)]

    return values