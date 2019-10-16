#Homework 2 Excersice 1
import json
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt

eng = pd.read_json(r"C:\Users\emanu\Desktop\HW2\Datasets\matches\matches_England.json")
week = 0
teams = []
score = []
ranking = defaultdict(int)
for i in eng["label"]:
    teams.append(i.split(",")[0])
    score.append(i.split(",")[1])
for i in range(len(teams) - 1, -1, -1):
    if int(score[i].split("-")[0]) > int(score[i].split("-")[1]):
        ranking[teams[i].split("-")[0]] += 3
    elif int(score[i].split("-")[0]) < int(score[i].split("-")[1]):
        ranking[teams[i].split("-")[1]] += 3
    elif int(score[i].split("-")[0]) == int(score[i].split("-")[1]):
        ranking[teams[i].split("-")[0]] += 1
        ranking[teams[i].split("-")[1]] += 1

    week += 1
    plt.plot(week, int(ranking[teams[i].split("-")[0]]))
    plt.plot(week, int(ranking[teams[i].split("-")[1]]))