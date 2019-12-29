import random

def dict_shuffle(dictionary):
    '''Randomly shuffles the dictionary order'''
    new = list(dictionary.items())
    random.shuffle(new)
    return dict(new)

def dict_to_str(dictionary):
    for x in dictionary:
        dictionary[x] = str(dictionary[x])
    return dictionary


def order_by_longest(dictionary, *args):
    '''Add arg = True for reverse sort'''

    d = {}
    for k in dictionary:
        d[k] = len(dictionary[k])

    new = {}
    for i in sorted(d, key=d.get, reverse=(lambda a: True if len(a) > 0 and a[0] == True else False)(args)):        
        new[i] = dictionary[i]

    return new

