import json
import pandas
from collections import defaultdict
import matplotlib.pyplot as plt

events_England = pandas.read_json(r"C:\Users\emanu\Downloads\Data\events\events_England.json")
is_passes = events_England.eventName == "Pass"
events_England = events_England[is_passes]
events_England = events_England.reset_index()
events_England.drop(columns = ["index"], inplace = True)
TopPlyPass = dict()
for j in range(len(events_England["tags"])):
    for i in range(len(events_England["tags"][i])):
        if (1801 == events_England["tags"][j][i]["id"]):
            TopPlyPass.setdefault(events_England["playerId"][i], [0, 0])[0] += 1