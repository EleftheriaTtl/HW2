import json
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt

eng = pd.read_json(r"C:\Users\39335\Downloads\Data\matches_England.json")
eng = eng.sort_values(by = "gameweek")
teams = []
score = []
ranking = dict()
for result in eng["label"]:
    teams.append(result.split(",")[0])
    score.append(result.split(",")[1])
# Creo due liste (Team1 - Team2, Score1 - Score2) ordinate per settimana
for i in range(len(teams)):
    if teams[i].split("-")[0] in ranking:
        if teams[i].split("-")[1] in ranking:
            if int(score[i].split("-")[0]) > int(score[i].split("-")[1]):
                ranking[teams[i].split("-")[0]].append(ranking[teams[i].split("-")[0]][-1] + 3)
                ranking[teams[i].split("-")[1]].append(ranking[teams[i].split("-")[1]][-1])
            elif int(score[i].split("-")[0]) < int(score[i].split("-")[1]):
                ranking[teams[i].split("-")[1]].append(ranking[teams[i].split("-")[1]][-1] + 3)
                ranking[teams[i].split("-")[0]].append(ranking[teams[i].split("-")[0]][-1])
            elif int(score[i].split("-")[0]) == int(score[i].split("-")[1]):
                ranking[teams[i].split("-")[1]].append(ranking[teams[i].split("-")[1]][-1] + 3)
                ranking[teams[i].split("-")[0]].append(ranking[teams[i].split("-")[0]][-1] + 3)
        else:
            ranking[teams[i].split("-")[1]] = [0]
    else:
        ranking[teams[i].split("-")[0]] = [0]
for keys in ranking:
    plt.plot(ranking[keys])