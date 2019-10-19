import json
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt

eng = pd.read_json(r"C:\Users\39335\Downloads\Data\matches_England.json")
eng = eng.sort_values(by="gameweek")
teams = []
score = []
ranking = dict()
for result in eng["label"]:
    teams.append(result.split(",")[0].strip())
    score.append(result.split(",")[1].strip())
# Creo due liste (Team1 - Team2, Score1 - Score2) ordinate per settimana
for i in range(len(teams)):
    if teams[i].split("-")[0].strip() in ranking:
        if teams[i].split("-")[1].strip() in ranking:
            if int(score[i].split("-")[0].strip()) > int(score[i].split("-")[1].strip()):
                ranking[teams[i].split("-")[0].strip()].append(ranking[teams[i].split("-")[0].strip()][-1] + 3)
                ranking[teams[i].split("-")[1].strip()].append(ranking[teams[i].split("-")[1].strip()][-1])
            elif int(score[i].split("-")[0].strip()) < int(score[i].split("-")[1].strip()):
                ranking[teams[i].split("-")[1].strip()].append(ranking[teams[i].split("-")[1].strip()][-1] + 3)
                ranking[teams[i].split("-")[0].strip()].append(ranking[teams[i].split("-")[0].strip()][-1])
            elif int(score[i].split("-")[0].strip()) == int(score[i].split("-")[1].strip()):
                ranking[teams[i].split("-")[1].strip()].append(ranking[teams[i].split("-")[1].strip()][-1] + 3)
                ranking[teams[i].split("-")[0].strip()].append(ranking[teams[i].split("-")[0].strip()][-1] + 3)
        else:
            ranking[teams[i].split("-")[1].strip()] = [0]
    else:
        ranking[teams[i].split("-")[0].strip()] = [0]
for keys in ranking:
    plt.plot(ranking[keys])


###############################################################################################################################


namew = [0, 0]
scorew = [0, 0]
namel = [0, 0]
scorel = [0, 0]
for key in ranking:
    countw = 0
    countl = 0
    w = 0
    l = 0
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
print(namew, scorew)
print(namel, scorel)