import pandas as pd
import datetime
from dateutil.parser import parse
from collections import defaultdict
import matplotlib.pyplot as plt
#--------------------------------------------------------------------------------
#read my file
coaches = pd.read_json("coaches.json")
teams = pd.read_json("teams.json")
eng = pd.read_json("matches_England.json")
teams = []
score = []
ranking = dict()
for result in eng["label"]:
    teams.append(result.split(",")[0].strip())
    score.append(result.split(",")[1].strip())
matchteam = []
matchscore = []
for i in range(len(teams)):
    o = teams[i].split("-")
    p = score[i].split("-")
    matchteam.append([o[0].strip(), o[1].strip()])
    matchscore.append([p[0].strip(), p[1].strip()])
def cont(myteam):
    winhome = 0
    winaway = 0
    drawhome = 0
    drawaway = 0
    losehome = 0
    loseaway = 0
    for i in range(len(eng)):
        if myteam==matchteam[i][0]:
            if matchscore[i][0]>matchscore[i][1]:
                winhome +=1
            elif matchscore[i][0]<matchscore[i][1]:
                losehome +=1
            else:
                drawhome +=1
        elif myteam==matchteam[i][1]:
            if matchscore[i][0]>matchscore[i][1]:
                loseaway +=1
            elif matchscore[i][0]<matchscore[i][1]:
                winaway +=1
            else:
                drawaway +=1
    lst = [[winhome,winaway], [losehome, loseaway], [drawhome, drawaway]]
    Contigency_Table = pd.DataFrame(lst)
    Contigency_Table.columns = ["Home", "Away"]
    Contigency_Table.rename(index = {0:'''Win''', 1:'''Lose''', 2:'''Draw'''}, inplace = True)
    return Contigency_Table