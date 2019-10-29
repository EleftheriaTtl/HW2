import json
import pandas as pd
from operator import itemgetter

events_England = pd.read_json(r"C:\Users\39335\Downloads\Data\events_England.json")
is_passes = events_England.eventName == "Pass"
events_England = events_England[is_passes]
events_England = events_England.reset_index()
events_England.drop(columns = ["index"], inplace = True)
TopPlyPass = dict()    # This dictionary will have the player ID as key and a list as values. The first item of the list is the count of successful passes, the second is the one of the failed passes.

# I check all the tags for each event and see if it's a succesful pass (1801) or a failed one (1802)
for i in range(len(events_England["tags"])):
    for j in range(len(events_England["tags"][i])):
        if (1801 == events_England["tags"][i][j]["id"]):
            TopPlyPass.setdefault(events_England["playerId"][i], [0, 0])[0] += 1
        if (1802 == events_England["tags"][i][j]["id"]):
            TopPlyPass.setdefault(events_England["playerId"][i], [0, 0])[1] += 1

Top10 = []
for key in list(TopPlyPass.keys()):
    if (TopPlyPass[key][0] + TopPlyPass[key][1] < 100):     # Set treshold on the number of total passes
        del TopPlyPass[key]
    else:
        Top10.append([key, TopPlyPass[key][0]/(TopPlyPass[key][0]+TopPlyPass[key][1])])

# Use the player name in place of player ID. We merge the data found this way with the dataset from "players.json".
Top10 = pd.DataFrame(Top10)
Top10.rename(columns = ({0:"playerId", 1:"Ratio"}), inplace = True)
players = pd.read_json(r"C:\Users\39335\Downloads\Data\players.json")
players.drop(columns = ["passportArea", "weight", "firstName" , "middleName",
            "lastName", "currentTeamId", "birthDate", "role", "birthArea", "foot",
                        "currentNationalTeamId", "height"], inplace = True )
players.rename(columns = ({"wyId":"playerId"}), inplace = True)
passes = pd.merge(Top10,players)
passes.drop(columns = ["playerId"], inplace = True)
passes = passes.sort_values(by = "Ratio", ascending = False)
print(passes.head(10))
