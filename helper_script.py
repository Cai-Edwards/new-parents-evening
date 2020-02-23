import json

"""
with open('init_analysis.json') as f:
    d = json.load(f)

    point = 0
    value = "data_median"

    for point in range(0, 4):
        total = []
        total2 = []

        for algo in d:
            for o in d[algo]:

                
                if ("Forpupil" in o) and ("Teacher" in o):
                
                    v = ([x.strip() for x in d[algo][o][value][1:-1].split(",")])
                    total.append(float(v[point]))
                    #print(v)
                    

                if ("Forpupil" in o) and ("Pupil" in o):
                
                    v = ([x.strip() for x in d[algo][o][value][1:-1].split(",")])
                    total2.append(float(v[point]))
                    #print(v)

        print(sum(total)/len(total))
        print(sum(total2)/len(total2))

        print("")
"""

with open('init_analysis.json') as f:
    d = json.load(f)

    value = "data_median"
    
    for algo in d:
        for o in d[algo]:
            if o == "BaseSortedTeachersForteacherFalse":
                v = ([x.strip() for x in d[algo][o][value][1:-1].split(",")])

                print(algo)
                for i in v:
                    print(i)
                print()
            
