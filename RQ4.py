import json
import pandas
from operator import itemgetter

events_England = pandas.read_json(r"C:\Users\39335\Downloads\Data\events_England.json")
is_passes = events_England.eventName == "Pass"
events_England = events_England[is_passes]
events_England = events_England.reset_index()
events_England.drop(columns = ["index"], inplace = True)
TopPlyPass = dict()
for i in range(len(events_England["tags"])):
    for j in range(len(events_England["tags"][i])):
        if (1801 == events_England["tags"][i][j]["id"]):
            TopPlyPass.setdefault(events_England["playerId"][i], [0, 0])[0] += 1
        if (1802 == events_England["tags"][i][j]["id"]):
            TopPlyPass.setdefault(events_England["playerId"][i], [0, 0])[1] += 1

Top10 = []
for key in list(TopPlyPass.keys()):
    if (TopPlyPass[key][0] + TopPlyPass[key][1] < 100):     # Set treshold
        del TopPlyPass[key]
    else:
        Top10.append([key, TopPlyPass[key][0]/(TopPlyPass[key][0]+TopPlyPass[key][1])])
print(sorted(Top10, key = itemgetter(1), reverse = True)[:10])