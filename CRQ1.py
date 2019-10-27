import json
import pandas as pd
from operator import itemgetter
import matplotlib.pyplot as plt

events_England = pandas.read_json(r"C:\Users\39335\Downloads\Data\events_England.json")
events_England = events_England.reset_index()
events_England.drop(columns=["index"], inplace=True)
TeamGoals = dict()  # Teams ID as value, a list of the goals for each time interval
PlayerGoals = dict()  # Players ID as value, a list of the goals for each time interval
TotalGoals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # A list of the sum of all goals for each time interval
for i in range(len(events_England["tags"])):
    for j in range(len(events_England["tags"][i])):
        # For each event if the tag is 101 (a goal) I increase the count of a list depending of the minute it was scored.
        # There is a different list for each team, each player and the total sum of the goals.
        if (101 == events_England["tags"][i][j]["id"]):
            if (0 <= events_England["eventSec"][i] <= 540 and events_England["matchPeriod"][i] == "1H"):
                PlayerGoals.setdefault(events_England["playerId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[0] += 1
                TeamGoals.setdefault(events_England["teamId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[0] += 1
                TotalGoals[0] += 1
            if (541 <= events_England["eventSec"][i] <= 1080 and events_England["matchPeriod"][i] == "1H"):
                PlayerGoals.setdefault(events_England["playerId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[1] += 1
                TeamGoals.setdefault(events_England["teamId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[1] += 1
                TotalGoals[1] += 1
            if (1081 <= events_England["eventSec"][i] <= 1620 and events_England["matchPeriod"][i] == "1H"):
                PlayerGoals.setdefault(events_England["playerId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[2] += 1
                TeamGoals.setdefault(events_England["teamId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[2] += 1
                TotalGoals[2] += 1
            if (1621 <= events_England["eventSec"][i] <= 2160 and events_England["matchPeriod"][i] == "1H"):
                PlayerGoals.setdefault(events_England["playerId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[3] += 1
                TeamGoals.setdefault(events_England["teamId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[3] += 1
                TotalGoals[3] += 1
            if (2161 <= events_England["eventSec"][i] <= 2700 and events_England["matchPeriod"][i] == "1H"):
                PlayerGoals.setdefault(events_England["playerId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[4] += 1
                TeamGoals.setdefault(events_England["teamId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[4] += 1
                TotalGoals[4] += 1
            if (2701 <= events_England["eventSec"][i] and events_England["matchPeriod"][i] == "1H"):
                PlayerGoals.setdefault(events_England["playerId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[5] += 1
                TeamGoals.setdefault(events_England["teamId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[5] += 1
                TotalGoals[5] += 1

            if (0 <= events_England["eventSec"][i] <= 540 and events_England["matchPeriod"][i] == "2H"):
                PlayerGoals.setdefault(events_England["playerId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[6] += 1
                TeamGoals.setdefault(events_England["teamId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[6] += 1
                TotalGoals[6] += 1
            if (541 <= events_England["eventSec"][i] <= 1080 and events_England["matchPeriod"][i] == "2H"):
                PlayerGoals.setdefault(events_England["playerId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[7] += 1
                TeamGoals.setdefault(events_England["teamId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[7] += 1
                TotalGoals[7] += 1
            if (1081 <= events_England["eventSec"][i] <= 1620 and events_England["matchPeriod"][i] == "2H"):
                PlayerGoals.setdefault(events_England["playerId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[8] += 1
                TeamGoals.setdefault(events_England["teamId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[8] += 1
                TotalGoals[8] += 1
            if (1621 <= events_England["eventSec"][i] <= 2160 and events_England["matchPeriod"][i] == "2H"):
                PlayerGoals.setdefault(events_England["playerId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[9] += 1
                TeamGoals.setdefault(events_England["teamId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[9] += 1
                TotalGoals[9] += 1
            if (2161 <= events_England["eventSec"][i] <= 2700 and events_England["matchPeriod"][i] == "2H"):
                PlayerGoals.setdefault(events_England["playerId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[10] += 1
                TeamGoals.setdefault(events_England["teamId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[10] += 1
                TotalGoals[10] += 1
            if (2701 <= events_England["eventSec"][i] and events_England["matchPeriod"][i] == "2H"):
                PlayerGoals.setdefault(events_England["playerId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[11] += 1
                TeamGoals.setdefault(events_England["teamId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[11] += 1
                TotalGoals[11] += 1
intervals = ["0-9", "9-18", "18-27", "27-36", "36-45", "45+", "45-54", "54-63", "63-72", "72-81", "81-90", "90+"]

######## I ########
plt.bar(intervals, TotalGoals)

######## II ########
TopScore = []   # List of team ID and goal scored in the interval 81-90
for key in TeamGoals:
    TopScore.append([key, TeamGoals[key][10]])
TopScore = pd.DataFrame(TopScore)
# Data cleaning and merge with the tams.json file to match the teams' ID and their Official Name
TopScore.columns = ["teamId","Score 81-90"]
TopScore = TopScore.sort_values(by = "Score 81-90", ascending=False)
TeamsName = pandas.read_json(r"C:\Users\39335\Downloads\Data\teams.json")
TeamsName.drop(columns = ["area", "city", "name", "type"], inplace = True)
TeamsName.columns = ["Official name", "teamId"]
Top10 = pd.merge(TopScore, TeamsName)
Top10.drop("teamId", axis = 1, inplace = True)
print(Top10.head(10))

######## III ########
BestPlayers = []   # List of player with at least a goal in at least 8 different intervals.
count = 0
for key in PlayerGoals:
    for i in PlayerGoals[key]:
        if i > 0:
            count += 1
    if count >= 8:
        BestPlayers.append(key)
    count = 0
BestPlayers = pd.DataFrame(BestPlayers)
BestPlayers.columns = ["playerId"]
players = pd.read_json(r"C:\Users\39335\Downloads\Data\players.json")
# update/change column to improve readability
players.drop(columns = ["passportArea", "weight", "firstName" , "middleName",
            "lastName", "currentTeamId", "birthDate", "role", "birthArea", "foot",
                         "currentNationalTeamId", "height"], inplace = True )
players.rename(columns = ({"wyId":"playerId"}), inplace = True)
PlayerList = pd.merge(BestPlayers, players)
PlayerList.drop(columns = ["playerId"], inplace = True)
print(PlayerList)