import json
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt

eng = pd.read_json(r"C:\Users\emanu\Downloads\Data\matches\matches_England.json")
eng = eng.sort_values(by="gameweek")    # I sort the dataframe by game week to make it simple to visualize the score throughout the season
teams = []
score = []
ranking = dict()
# I create two lists with elements "Team1 - Team2" and "Score1 - Score2" ordered by week
for result in eng["label"]:
    teams.append(result.split(",")[0].strip())
    score.append(result.split(",")[1].strip())

# I initialize a dictionary with keys the names of the teams and as value a list (in the end the list will contain the points that a team has for each week of the season)
for i in range(len(teams)):
    ranking[teams[i].split("-")[0].strip()] = [0]
    ranking[teams[i].split("-")[1].strip()] = [0]

# For each game I append the points that a team has +3 if it won, +1 draw, or +0 if lost, to the dictionary
for i in range(len(teams)):
    if int(score[i].split("-")[0].strip()) > int(score[i].split("-")[1].strip()):
        ranking[teams[i].split("-")[0].strip()].append(ranking[teams[i].split("-")[0].strip()][-1] + 3)
        ranking[teams[i].split("-")[1].strip()].append(ranking[teams[i].split("-")[1].strip()][-1])
    elif int(score[i].split("-")[0].strip()) < int(score[i].split("-")[1].strip()):
        ranking[teams[i].split("-")[1].strip()].append(ranking[teams[i].split("-")[1].strip()][-1] + 3)
        ranking[teams[i].split("-")[0].strip()].append(ranking[teams[i].split("-")[0].strip()][-1])
    elif int(score[i].split("-")[0].strip()) == int(score[i].split("-")[1].strip()):
        ranking[teams[i].split("-")[1].strip()].append(ranking[teams[i].split("-")[1].strip()][-1] + 1)
        ranking[teams[i].split("-")[0].strip()].append(ranking[teams[i].split("-")[0].strip()][-1] + 1)

# Delete the first element of the lists (because it's 0 for everybody and we want to count from week 1)
for keys, values in ranking.items():
    del values[0]

# Plot of teams' score throughout the season
df = pd.DataFrame(ranking)
plt.style.use("seaborn-darkgrid")
num = 0
week = []
for i in range(len(set(eng.gameweek))+1):
    week.append("Week " + str(i+1))
fig= plt.figure(figsize=(30,20))
axes= fig.add_axes([0.1,0.1,0.8,0.8])
for column in df:
    num += 1
    axes.plot(df[column], marker = "",  linewidth = 1, alpha = 0.9, label = column)
plt.xticks(range(38), week)
plt.legend(loc="upper left", ncol=1, bbox_to_anchor=(1, 1), fancybox=True, shadow=True)
plt.title("Score of the teams for each week", loc='left', fontsize=12, fontweight=0, color='orange')
plt.ylabel("Score")
fig.savefig("Score_Graph")
###############################################################################################################################
# Winning and losing streaks
# I'll use 4 lists of 2 elements. The names of the 2 teams with the highest winning strak, the ones with the highest losing streak and their respective value.
namew = [0, 0]
scorew = [0, 0]
namel = [0, 0]
scorel = [0, 0]

# For each team I set a counter that increases each win/loss and I reset to 0 if the streak is broken. When the streak is broken if the counter is bigger than the stored value (w/l) I update it
for key in ranking:
    countw = 0
    countl = 0
    w = 0
    l = 0
    if ranking[key][0] == 0:
        countl += 1
    if ranking[key][0] == 3:
        countw += 1
    for i in range(1, len(ranking[key])):
        if (ranking[key][i] == ranking[key][i - 1] + 3):
            countw += 1
        else:
            if (countw > w):
                w = countw
            countw = 0

        if (ranking[key][i] == ranking[key][i - 1]):
            countl += 1
        else:
            if (countl > l):
                l = countl
            countl = 0

    if (w > scorew[0]):
        scorew[1] = scorew[0]
        scorew[0] = w
        namew[1] = namew[0]
        namew[0] = key
    elif (w <= scorew[0] and w > scorew[1]):
        scorew[1] = w
        namew[1] = key

    if (l > scorel[0]):
        scorel[1] = scorel[0]
        scorel[0] = l
        namel[1] = namel[0]
        namel[0] = key
    elif (l <= scorel[0] and l > scorel[1]):
        scorel[1] = l
        namel[1] = key

print("The team with the highest winning streak is {} with {} consecutive wins, the second is {} with {} consecutive wins". format(namew[0], scorew[0], namew[1], scorew[1]))
print("The team with the highest losing streak is {} with {} consecutive losses, the second is {} with {} consecutive losses". format(namel[0], scorel[0], namel[1], scorel[1]))