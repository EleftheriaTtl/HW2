#!/usr/bin/env python
# coding: utf-8

# # Homework 2 - Soccer analytics
# 
# ### Libraries

# In[10]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from collections import defaultdict
import collections
import matplotlib.patches as mp
import datetime
from dateutil.parser import parse
import numpy as np
import scipy.stats as scs


# # Clean the matches dataframe
# 
# ### We made a function that cleans a bit the matches dataset, so the analysis and access to information is easier

# In[7]:


def matches_clean(matches):
    matches.drop(columns=["status", "roundId", "seasonId",
                          "referees", "duration", "competitionId",
                          "date"], inplace=True)
    team_home = []
    team_away = []
    score_home = []
    score_away = []
    coach_home = []
    coach_away = []
    line_up_home = []
    line_up_away = []
    bench_home = []
    bench_away = []
    sub_home = []
    sub_away = []
    for i in range(len(matches)):
        teams = list(matches.teamsData[i].keys())
        score = list(matches.teamsData[i].values())
        team_home.append(teams[0])
        team_away.append(teams[1])
        score_home.append(score[0]["score"])
        score_away.append(score[1]["score"])
        coach_home.append(score[0]["coachId"])
        coach_away.append(score[1]["coachId"])
        line_up_home.append(score[0]["formation"]["lineup"])
        line_up_away.append(score[1]["formation"]["lineup"])
        bench_home.append(score[0]["formation"]["bench"])
        bench_away.append(score[1]["formation"]["bench"])
        sub_home.append(score[0]["formation"]["substitutions"])
        sub_away.append(score[1]["formation"]["substitutions"])
    matches["team_home"] = team_home
    matches["team_away"] = team_away
    matches["score_home"] = score_home
    matches["score_away"] = score_away
    matches["coach_home"] = coach_home
    matches["coach_away"] = coach_away
    matches["line_up_home"] = line_up_home
    matches["line_up_away"] = line_up_away
    matches["bench_home"] = bench_home
    matches["bench_away"] = bench_away
    matches["sub_home"] = sub_home
    matches["sub_away"] = sub_away
    matches.rename(columns={"gameweek": "GameWeek", "wyId": "MatchId"}, inplace=True)
    matches.drop(columns=["teamsData", "label"], inplace=True)
    return matches


# ### We will need a function that provides us with a football pitch

# In[35]:


def draw_pitch(axes):
    # focus on only half of the pitch
    # pitch Outline & Centre Line
    pitch = mp.Rectangle([0, 0], width=120, height=80, fill=False)
    # Left, Right Penalty Area and midline
    left_penalty = mp.Rectangle([0, 22.3], width=14.6, height=35.3, fill=False)
    right_penalty = mp.Rectangle([105.4, 22.3], width=14.6, height=35.3, fill=False)
    midline = mp.ConnectionPatch([60, 0], [60, 80], "data", "data")

    # Left, Right 6-yard Box
    left_six_yard = mp.Rectangle([0, 32], width=4.9, height=16, fill=False)
    right_six_yard = mp.Rectangle([115.1, 32], width=4.9, height=16, fill=False)

    # Prepare Circles
    centre_circle = plt.Circle((60, 40), 8.1, color="black", fill=False)
    centre_spot = plt.Circle((60, 40), 0.71, color="black")
    # Penalty spots and Arcs around penalty boxes
    left_pen_spot = plt.Circle((9.7, 40), 0.71, color="black")
    right_pen_spot = plt.Circle((110.3, 40), 0.71, color="black")
    left_arc = mp.Arc((9.7, 40), height=16.2, width=16.2, angle=0, theta1=310, theta2=50, color="black")
    right_arc = mp.Arc((110.3, 40), height=16.2, width=16.2, angle=0, theta1=130, theta2=230, color="black")

    element = [pitch, left_penalty, right_penalty, midline, left_six_yard, right_six_yard, centre_circle,
               centre_spot, right_pen_spot, left_pen_spot, left_arc, right_arc]
    for j in element:
        axes.add_patch(j)


# # [RQ1] Who wants to be a Champion? 

# In[8]:


def RQ1(m):
    m = m.sort_values(by="gameweek")
    teams = []
    score = []
    ranking = dict()
    for result in m["label"]:
        teams.append(result.split(",")[0].strip())
        score.append(result.split(",")[1].strip())
    # Creo due liste (Team1 - Team2, Score1 - Score2) ordinate per settimana
    for i in range(len(teams)):
        ranking[teams[i].split("-")[0].strip()] = [0]
        ranking[teams[i].split("-")[1].strip()] = [0]

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
    for keys, values in ranking.items():
        del values[0]
    df = pd.DataFrame(ranking)
    plt.style.use("seaborn-darkgrid")
    num = 0
    week = []
    for i in range(len(set(m.gameweek)) + 1):
        week.append("Week " + str(i + 1))
    fig = plt.figure(figsize=(30, 20))
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    for column in df:
        num += 1
        axes.plot(df[column], marker="", linewidth=1, alpha=0.9, label=column.encode("utf-8").decode("unicode-escape"))
    plt.xticks(range(38), week)
    plt.legend(loc="upper left", ncol=1, bbox_to_anchor=(1, 1), fancybox=True, shadow=True)
    plt.title("Score of the teams for each week", loc='left', fontsize=12, fontweight=0, color='orange')
    plt.ylabel("Score")
    plt.show()

    namew = [0, 0]
    scorew = [0, 0]
    namel = [0, 0]
    scorel = [0, 0]
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
            if ranking[key][i] == ranking[key][i - 1] + 3:
                countw += 1
            else:
                if countw > w:
                    w = countw
                countw = 0

            if ranking[key][i] == ranking[key][i - 1]:
                countl += 1
            else:
                if countl > l:
                    l = countl
                countl = 0

        if w > scorew[0]:
            scorew[1] = scorew[0]
            scorew[0] = w
            namew[1] = namew[0]
            namew[0] = key
        elif scorew[0] >= w > scorew[1]:
            scorew[1] = w
            namew[1] = key

        if l > scorel[0]:
            scorel[1] = scorel[0]
            scorel[0] = l
            namel[1] = namel[0]
            namel[0] = key
        elif scorel[0] >= l > scorel[1]:
            scorel[1] = l
            namel[1] = key
    namew[0] = namew[0].encode("utf-8").decode("unicode-escape")
    namew[1] = namew[1].encode("utf-8").decode("unicode-escape")
    namel[0] = namel[0].encode("utf-8").decode("unicode-escape")
    namel[1] = namel[1].encode("utf-8").decode("unicode-escape")
    fig = go.Figure(data=[go.Table(header=dict(values=['Team', 'Winning Record']),
                                   cells=dict(values=[namew, scorew]))
                          ])
    fig.show()
    fig = go.Figure(data=[go.Table(header=dict(values=['Team', 'Losing Record']),
                                   cells=dict(values=[namel, scorel]))
                          ])
    fig.show()


# ###### The plot that follows is the results of RQ1 for the Premier League

# In[11]:


eng = pd.read_json("matches_England.json")
RQ1(eng)


# ###### The code that follows is the results  of RQ1 for the other leagues as well as the European Championship and the World Cup

# In[ ]:


# The RQ1 exercise for the European Championship
# ec = pd.read_json("matches_European_Championship.json")
# RQ1(ec)

# The RQ1 exercise for Ligue 1
# f = pd.read_json("matches_France.json")
# RQ1(f)

# The RQ1 exercise for Bundesliga
# g = pd.read_json("matches_Germany.json")
# RQ1(g)

# The RQ1 exercise for Serie A
# it = pd.read_json("matches_Italy.json")
# RQ1(it)

# The RQ1 exercise for LaLiga
# sp = pd.read_json("matches_Spain.json")
# RQ1(sp)

# The RQ1 exercise for the World Cup
# wc = pd.read_json("matches_World_Cup.json")
# RQ1(wc)


# # [RQ2] Is there a home-field advantage?

# In[27]:


def compute_contingency_table(dataset):
    eng = dataset

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
    #cont is a function that calculate the contingency table for the input team
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

        Contigency_Table = pandas.DataFrame(lst)

        Contigency_Table.columns = ["Home", "Away"]

        Contigency_Table.rename(index = {0:'''Win''', 1:'''Lose''', 2:'''Draw'''}, inplace = True)

        return Contigency_Table
    print("Burnley Cont\n")
    print(cont('Burnley'))
    print('\n')

    print("Burnley Cont\n")
    print(cont('Burnley'))
    print('\n')

    print("Arsenal\n")
    print(cont('Arsenal'))
    print('\n')

    print("West Bromwich Albion\n")
    print(cont('West Bromwich Albion'))
    print('\n')
    print("Manchester City\n")
    print(cont('Manchester City'))
    print('\n')

    print("Liverpool")
    print(cont('Liverpool'))
    print('\n')
    #Calc_of_CHISQUARED 
    #choosen_team:BURNLEY
    print("BURNLEY CHI_SQUARED_TEST\n")
    print(scs.chi2_contingency(cont('Burnley')))


# ###### The table that follows id the result of RQ2 for the chosen teams of Premier League

# In[28]:


compute_contingency_table(eng)


# # [RQ3] Which teams have the youngest coaches?

# In[17]:


def RQ3(c, t, m):
    # C_0_A_C_H_E_S__D_A_T_A_F_R_A_M_E
    # save the whole name in one column
    c["Name"] = c["firstName"] + " " + c["lastName"]
    # delete the null cells in birthDate
    c = c[pd.notnull(c['birthDate'])]
    # now i am ready to calculate the age
    # i compute now so i can find the exact age
    now = pd.Timestamp("now")
    # i tranfsorm my column into a datetime element that ecognise years months and days
    c["birthDate"] = pd.to_datetime(c["birthDate"], format="%Y-%m-%d")
    # i create a new column "age", where i calculate the age. I use astype(<m8[y]) cause if i don't this format gives me
    # the total says this guy lived on earth.. So this makes it into years
    c["Age"] = (now - c["birthDate"]).astype('<m8[Y]')
    c.Age = c.Age.astype(int)
    # at som programs there is a unicode problem..
    # working with pyCharm thiw works for my strings
    name = []
    for ele in c.Name:
        name.append(ele.encode("utf-8").decode("unicode-escape"))
    c["Name"] = name
    # clean up the team id column(there is no team with team id equal to 0
    c.reset_index(inplace=True)
    c.drop(columns=["index", "birthArea","currentTeamId", "passportArea", "middleName", "firstName", "lastName", "shortName", "birthDate"],
           inplace=True)
    c.rename(columns={"wyId": "CoachId"}, inplace=True)
    # --------------------------------------------------------------------------------------------
    # T_E_A_M_S__D_A_T_A_F_R_A_M_E
    city = []
    name = []
    on = []
    for i in range(len(t.city)):
        name.append(t.name[i].encode("utf-8").decode("unicode-escape"))
        city.append(t.city[i].encode("utf-8").decode("unicode-escape"))
        on.append(t.officialName[i].encode("utf-8").decode("unicode-escape"))
    t["City"] = city
    t["Name"] = name
    t["OfficialName"] = on
    t.drop(columns=["area", "type", "officialName", "name", "city"], inplace=True)
    t.rename(columns={"wyId": "TeamId"}, inplace=True)
    # ---------------------------------------------------------------------------------------------------
    # M_A_T_C_H_E_S__D_A_T_A_F_R_A_M_E
    matches = matches_clean(m)
    # ----------------------------------------------------------------------------------------------------
    # Check the column of matches (team_home, team_away) and their coaches and make a dictionary,
    # with no duplicates and no coaches with id 0
    #premier_league1, is a dictionary with keys the coaches and values the teams, so we can have all the coaches
    premier_league1 = defaultdict(list)
    for i in range(len(matches)):
        if matches["coach_home"][i] != 0 and int(matches.team_home[i]) not in premier_league1[matches["coach_home"][i]] :
                premier_league1[matches["coach_home"][i]].append(int(matches.team_home[i]))
        if matches["coach_away"][i] != 0 and int(matches.team_away[i]) not in premier_league1[matches["coach_away"][i]] :
                premier_league1[matches["coach_away"][i]].append(int(matches.team_away[i]))
    premier_league1 = pd.Series(premier_league1).to_frame()
    premier_league1.reset_index(inplace = True)
    premier_league1.rename(columns = {"index": "CoachId", 0:"TeamId"}, inplace = True)
    # I merge the dataframes premier_league1 and c so i can have all the coaches, their teams and their ages
    all_the_coaches = pd.merge(premier_league1, c, on = "CoachId")
    # premier_league2 is a dictionary with keys the teams and values the list(if there are more than one ) of coaches
    premier_league2 = defaultdict(list)
    for i in range(len(matches)):
        if int(matches.coach_home[i]) != 0 and int(matches.coach_home[i]) not in premier_league2[matches.team_home[i]] :
                premier_league2[matches.team_home[i]].append(int(matches.coach_home[i]))
        if int(matches.coach_away[i]) != 0 and int(matches.coach_away[i]) not in premier_league2[matches.team_away[i]] :
                premier_league2[matches.team_away[i]].append(int(matches.coach_away[i]))
    premier_league2 = pd.Series(premier_league2).to_frame()
    premier_league2.reset_index(inplace = True)
    premier_league2.rename(columns = {"index": "TeamId", 0:"CoachId"}, inplace = True)
    # from every team in premier_league2 i keep the youngest coach
    co = []
    for ele in premier_league2.CoachId:
        m = 99
        for a in ele:
            try:
                if c.loc[a].Age < m:
                    m = c.loc[a].Age
            except KeyError:
                pass
        co.append(a)
    premier_league2["CoachId"] = co
    # I merge the dataframes premier_league2 and c so i can have the ages of teh coaches and their teams
    top_10 = pd.merge(premier_league2, c, on = "CoachId")
    top_10.TeamId = top_10.TeamId.astype(int)
    # I merge again the dataframe i obtain with t (teams dataframe) so i can have the official name of the team
    top_10 = pd.merge(top_10, t, on = "TeamId")
    top_10.sort_values(by = "Age", inplace = True)
    # Q_U_E_S_T_I_O_N_#_1__Rank the teams beased on the age of the coach and show the top 10
    fig = go.Figure(data=[go.Table(header=dict(values=['Team', 'Younger Coach', 'Age']),
                     cells=dict(values=[top_10.OfficialName.head(10), top_10.Name_x.head(10), top_10.Age.head(10)]))
                     ])
    fig.show()
    # Q_U_E_S_T_I_O_N_#_2__ Show the distirbutions of the ages of all coaches, using a boxplot
    ax = sns.boxplot( y=all_the_coaches["Age"] ).set_title("Distribution of the coaches' age")
    return(ax)


# ###### What follows is the results of RQ3 for the Premier League

# In[18]:


eng = pd.read_json("matches_England.json")
c = pd.read_json("coaches.json")
t = pd.read_json("teams.json")
RQ3(c,t,eng)


# ###### The code that follows is the results  of RQ3 for the other leagues as well as the European Championship and the World Cup

# In[ ]:


# The RQ3 exercise for the European Championship
# ec = pd.read_json("matches_European_Championship.json")
# c = pd.read_json("coaches.json")
# t = pd.read_json("teams.json")
# RQ3(c,t,ec)

# The RQ3 exercise for Ligue 1
# f = pd.read_json("matches_France.json")
# c = pd.read_json("coaches.json")
# t = pd.read_json("teams.json")
# RQ3(c,t,f)

# The RQ3 exercise for Bundesliga
# g = pd.read_json("matches_Germany.json")
# c = pd.read_json("coaches.json")
# t = pd.read_json("teams.json")
# RQ3(c,t,g)

# The RQ3 exercise for Serie A
# it = pd.read_json("matches_Italy.json")
# c = pd.read_json("coaches.json")
# t = pd.read_json("teams.json")
# RQ3(c,t,it)

# The RQ3 exercise for LaLiga
# sp = pd.read_json("matches_Spain.json")
# c = pd.read_json("coaches.json")
# t = pd.read_json("teams.json")
# RQ3(c,t,sp)

# The RQ3 exercise for the World Cup
# wc = pd.read_json("matches_World_Cup.json")
# c = pd.read_json("coaches.json")
# t = pd.read_json("teams.json")
# RQ3(c,t,wc)


# # [RQ4] Find the top 10 players with the highest ratio between completed passes and attempted passes.

# In[19]:


def RQ4(e, p):
    is_passes = e.eventName == "Pass"
    e = e[is_passes]
    e = e.reset_index()
    e.drop(columns=["index"], inplace=True)
    TopPlyPass = dict()  # This dictionary will have the player ID as key and a list as values. The first item of the
    # list is the count of successful passes, the second is the one of the failed passes.
    for i in range(len(e["tags"])):
        for j in range(len(e["tags"][i])):
            if 1801 == e["tags"][i][j]["id"]:  # Check to see if at least 1 of the tags of a specific event
                # is a successful pass.
                TopPlyPass.setdefault(e["playerId"][i], [0, 0])[0] += 1
            if 1802 == e["tags"][i][j]["id"]:  # Same for a failed pass.
                TopPlyPass.setdefault(e["playerId"][i], [0, 0])[1] += 1

    Top10 = []
    for key in list(TopPlyPass.keys()):
        if TopPlyPass[key][0] + TopPlyPass[key][1] < 100:  # Set treshold on the number of total passes
            del TopPlyPass[key]
        else:
            Top10.append([key, TopPlyPass[key][0] / (TopPlyPass[key][0] + TopPlyPass[key][1])])

    # Use the player name in place of player ID. We merge the data found this way with the dataset from "players.json".
    Top10 = pd.DataFrame(Top10)
    Top10.rename(columns=({0: "PlayerId", 1: "Ratio"}), inplace=True)
    # update/change column to improve readability
    p["Name"] = p["firstName"] + " " + p["lastName"]
    p = p[p.currentTeamId != 0]
    name = []
    for i in range(len(p.Name)):
        name.append(p.Name[i].encode("utf-8").decode("unicode-escape"))
    p["Name"] = name
    p.reset_index(inplace=True)
    p.drop(columns=["index", "foot", "birthArea", "role", "weight", "passportArea", "middleName", "firstName", "lastName",
                    "shortName", "birthDate", "currentNationalTeamId"],
           inplace=True)
    p.rename(columns={"currentTeamId": "TeamId", "wyId": "PlayerId", "height": "Height"}, inplace=True)

    passes = pd.merge(Top10, p)
    passes.drop(columns=["PlayerId"], inplace=True)
    passes = passes.sort_values(by="Ratio", ascending=False)
    fig = go.Figure(data=[go.Table(header=dict(values=['Player', "Ratio of Completed to Attempted Passes"]),
                                   cells=dict(values=[passes["Name"].head(10), round(passes["Ratio"],3).head(10)]))
                          ])
    fig.show()


# ###### What follows is the results of RQ4 for the Premier League

# In[20]:


eng = pd.read_json("events_England.json")
p = pd.read_json("players.json")
RQ4(eng, p)


# ###### The code that follows is the results  of RQ4 for the other leagues as well as the European Championship and the World Cup

# In[21]:


# The RQ4 exercise for the European Championship
# ec = pd.read_json("events_European_Championship.json")
# p = pd.read_json("players.json")
# RQ4(ec, p)

# The RQ4 exercise for Ligue 1
# f = pd.read_json("events_France.json")
# p = pd.read_json("players.json")
# RQ4(f, p)

# The RQ4 exercise for Bundesliga
# g = pd.read_json("events_Germany.json")
# p = pd.read_json("players.json")
# RQ4(g, p)

# The RQ4 exercise for Serie A
# it = pd.read_json("events_Italy.json")
# p = pd.read_json("players.json")
# RQ4(it, p)

# The RQ4 exercise for LaLiga
# sp = pd.read_json("events_Spain.json")
# p = pd.read_json("players.json")
# RQ4(sp, p)

# The RQ4 exercise for the World Cup
# wc = pd.read_json("events_World_Cup.json")
# p = pd.read_json("players.json")
# RQ4(wc, p)


# # [RQ5] Does being a tall player mean winning more air duels?

# In[22]:


def RQ5(e,p):
    # check where there is an airduel event and keep only that
    e = e[e.subEventName == "Air duel"]
    # reser the indexes so you make you're analysis more easy
    e = e.reset_index()
    e.drop(columns=["index"], inplace=True)
    # remove all the null elements
    e = e[pd.notnull(e['tags'])]
    # update/change your current column tags with the actual result of the duel(won, lost, neutral)
    tag = []
    to_remove = []
    for i in range(len(e)):
        o = e.tags[i][1]['id']
        if o == 1802 or o == 703:
            tag.append("Lost")
        elif o == 1801 or o == 701:
            tag.append("Won")
        elif o == 702:
            tag.append("Neutral")
        else:
            to_remove.append(i)
    e.drop(index=to_remove, inplace=True)
    e = e.reset_index()
    e.tags = tag
    # --------------------------------------------------------------------------------------
    # im gonna make two dictionaries(dataframes to be) one for the duels won and one for the total
    airduelswon = collections.Counter()
    airduelstotal = collections.Counter()
    for i in range(len(e)):
        if e.tags[i] == "Won":
            airduelswon[e.playerId[i]] += 1
            airduelstotal[e.playerId[i]] += 1
        else:
            airduelstotal[e.playerId[i]] += 1
    air = pd.DataFrame([airduelswon, airduelstotal]).T
    air.dropna(inplace=True)
    air = air[air[1] > air[1].quantile(0.10)]
    # now i have a dataframe where i have my air duels won and the total , where i deleted the row where the total
    # airduels where less than the 10%
    air.reset_index(inplace=True)
    air["Ratio"] = round(air[0] / air[1], 2)
    air.drop(columns=[0, 1], inplace=True)
    air.rename(columns={"index": "PlayerId"}, inplace=True)
    #-----------------------------------------------------------------------------------------------
    #P_L_A_Y_E_R_S__D_A_T_A_S_E_T
    p["Name"] = p["firstName"] + " " + p["lastName"]
    p = p[p.currentTeamId != 0]
    name = []
    for i in range(len(p.Name)):
        name.append(p.Name[i].encode("utf-8").decode("unicode-escape"))
    p["Name"] = name
    p.reset_index(inplace=True)
    p.drop(columns=["index", "foot", "birthArea", "role", "weight", "passportArea", "middleName", "firstName", "lastName",
                    "shortName", "birthDate", "currentNationalTeamId"],
           inplace=True)
    p.rename(columns={"currentTeamId": "TeamId", "wyId": "PlayerId", "height" : "Height"}, inplace=True)
    #----------------------------------------------------------------------------------------------
    # now i have a dataframe with the players height and the ratio of won air duels
    kefalies = pd.merge(air, p)
    kefalies.drop(columns=["PlayerId"], inplace=True)
    cat = []
    # i fix the category where each players lies, according to their height
    for i in range(len(kefalies)):
        if kefalies.Height[i] < 160:
            cat.append(" <1,60 ")
        elif 160 <= kefalies.Height[i] < 165:
            cat.append("[1,60 - 1,65)")
        elif 165 <= kefalies.Height[i] < 170:
            cat.append("[1,65 - 1,70)")
        elif 170 <= kefalies.Height[i] < 175:
            cat.append("[1,70 - 1,75)")
        elif 175 <= kefalies.Height[i] < 180:
            cat.append("[1,75 - 1,80)")
        elif 180 <= kefalies.Height[i] < 185:
            cat.append("[1,80 - 1,85)")
        elif 185 <= kefalies.Height[i] < 190:
            cat.append("[1,85 - 1,90)")
        elif 190 <= kefalies.Height[i] < 195:
            cat.append("[1,90 - 1,95)")
        elif 195 <= kefalies.Height[i] < 200:
            cat.append("[1,95 - 2,00)")
        elif kefalies.Height[i] >= 200:
            cat.append(" >=2,00")
    kefalies["Category"] = pd.Categorical(cat)
    kefalies.sort_values(by=["Ratio"])
    #-------------------------------------------------------------------------------------
    #scatterplot, where each point (x,y) represent a player whose height is equal to x,
    #and that has a ratio of winning air duels equal to y.
    sns.set_style("white", {'font.family': ['sans-serif'], 'axes.axisbelow': True})
    ax = sns.catplot(x="Height", y="Ratio", hue="Category", data=kefalies, jitter=False)
    ax.set_xticklabels([])
    return(ax)


# ###### What follows is the results of RQ5 for the Premier League

# In[23]:


eng = pd.read_json("events_England.json")
p = pd.read_json("players.json")
RQ5(eng, p)


# ###### The code that follows is the results  of RQ5 for the other leagues as well as the European Championship and the World Cup

# In[ ]:


# The RQ5 exercise for the European Championship
# ec = pd.read_json("events_European_Championship.json")
# p = pd.read_json("players.json")
# RQ5(ec, p)

# The RQ5 exercise for Ligue 1
# f = pd.read_json("events_France.json")
# p = pd.read_json("players.json")
# RQ5(f, p)

# The RQ5 exercise for Bundesliga
# g = pd.read_json("events_Germany.json")
# p = pd.read_json("players.json")
# RQ5(g, p)

# The RQ5 exercise for Serie A
# it = pd.read_json("events_Italy.json")
# p = pd.read_json("players.json")
# RQ5(it, p)

# The RQ5 exercise for LaLiga
# sp = pd.read_json("events_Spain.json")
# p = pd.read_json("players.json")
# RQ5(sp, p)

# The RQ5 exercise for the World Cup
# wc = pd.read_json("events_World_Cup.json")
# p = pd.read_json("players.json")
# RQ5(wc, p)


# # [RQ6] Free your mind!
# 
# ## THE GOAL OF THIS ANALYSIS IS TO DISCOVER AND UNDERSTAND WHICH IS THE CORRELATION BETHWEEN NATIONS AND NUMBER OF GOAL OF THIS NATION
# 
# ## WHO WILL BE THE STRONGEST TEAM?
# 
# ### IMPORTANT! THIS FUNCTION CHANGES THE ORIGINAL DATASET. IF IT IS CALLED TWICE ON ITS OWN RESULT IT WON'T WORK!

# In[25]:


def calculate_nations_goals(events,players):
    
    import pandas
    import numpy as np
    import matplotlib.pyplot as plt
    
    
    a=[] 

    for tag in events.tags:

        b=[] #list_to_replace_dictonaries

        for dictonary in tag:

            for var in dictonary.values():

                var=int(var)

            b.append(var)

        a.append(b)



    #I remove the number which are different to 101



    for lis in a:

        while(len(lis)>1):

            for elem in lis:

                if elem!=101:

                    lis.remove(elem)



    for lis in a:

        for elem in lis:

            if elem>101 or elem<101:

                lis.remove(elem)




    #this function converts a list into an integer

    def convert(list): 

    # Converting integer list to string list 

        s = [str(i) for i in list] 



        # Join list items using join() 

        res = int("".join(s)) 
        return(res)





   #I put a 0 in all empty list, it's necessary for the conversion

    for tag in a:

        if tag==[]:

            tag.append(0)




    #now i put a list of integer which are the tags' column

    result=[]

    for tag in a:

        result.append(convert(tag))




    events.tags=result



    #These queries calculate the number of goal for each player

    final=events[(events.tags==101)][['teamId','tags','eventSec']]

    final=events[(events.tags==101)][['tags','playerId']]

    final=final.groupby(['playerId',]).size().to_frame('goalNumber').reset_index().sort_values(['playerId', 'goalNumber'], ascending=[True, False])

    Nations=players.merge(final, left_on='wyId', right_on='playerId')

    nations=[] #listofvalues(tags_values)

    for i in range(len(Nations.birthArea)):

        #list_to_replace_dictonaries
        nations.append(Nations.birthArea[i]['name'])

    Nations.birthArea=nations

    #This query modify the dataframe: a column with nations and a corresponding column with goals number

    nations_GN=Nations.groupby(['birthArea',]).size().to_frame('goalNumber').reset_index().sort_values(['birthArea', 'goalNumber'], ascending=[True, False])

    #This is the bar_plot x_ax=Nations y_ax=goals
    
    nations_GN.plot.bar()


# In[26]:


calculate_nations_goals(eng, p)


# # [CRQ1] What are the time slots of the match with more goals?

# ### Make a barplot with the absolute frequency of goals in all the time slots.

# In[29]:


events_England = pd.read_json(r"events_England.json")
events_England = events_England.reset_index()
events_England.drop(columns = ["index"], inplace = True)
TeamGoals = dict()   # Teams ID as value, a list of the goals for each time interval
PlayerGoals = dict() # Players ID as value, a list of the goals for each time interval
TotalGoals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # A list of the sum of all goals for each time interval
for i in range(len(events_England["tags"])):
    for j in range(len(events_England["tags"][i])):
    # For each event if the tag is 101 (a goal) I increase the count of a list depending of the minute it was scored
    # There is a different list for each team, each player and the total sum of the goals
        if (101 == events_England["tags"][i][j]["id"]):
            for m in range(6):
                if (m*540 <= events_England["eventSec"][i] <= (m+1)*540 and events_England["matchPeriod"][i] == "1H"):
                    PlayerGoals.setdefault(events_England["playerId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[m] += 1
                    TeamGoals.setdefault(events_England["teamId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[m] += 1
                    TotalGoals[m] += 1
            for m in range(6):
                if (m*540 <= events_England["eventSec"][i] <= (m+1)*540 and events_England["matchPeriod"][i] == "2H"):
                    PlayerGoals.setdefault(events_England["playerId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[6+m] += 1
                    TeamGoals.setdefault(events_England["teamId"][i], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])[6+m] += 1
                    TotalGoals[6+m] += 1
intervals = ["0-9", "9-18", "18-27", "27-36", "36-45", "45+", "45-54", "54-63", "63-72", "72-81", "81-90", "90+"]

######## I ########
plt.barh(intervals, TotalGoals, color = "green")
plt.title('Goals scored for each time interval')


# ### Find the top 10 teams that score the most in the interval "81-90"

# In[32]:


######## II ########
TopScore = []   # List of team ID and goal scored in the interval 81-90
for key in TeamGoals:
    TopScore.append([key, TeamGoals[key][10]])
TopScore = pd.DataFrame(TopScore)
# Data cleaning and merge with the tams.json file to match the teams' ID and their Official Name
TopScore.columns = ["teamId","Score 81-90"]
TopScore = TopScore.sort_values(by = "Score 81-90", ascending=False)
TeamsName = pd.read_json(r"teams.json")
TeamsName.drop(columns = ["area", "city", "name", "type"], inplace = True)
TeamsName.columns = ["teamId", "Official name"]
Top10 = pd.merge(TopScore, TeamsName)
Top10.drop("teamId", axis = 1, inplace = True)
print("Top 10 teams that score the most in the interval 81-90 are:\n")
Top10
print(Top10.head(10))


# ### Show if there are players that were able to score at least one goal in 8 different intervals.

# In[34]:


######## III ########
BestPlayers = []   # List of players with at least a goal in at least 8 different intervals.
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
# Merge with players.json to pair ID with players' names
players = pd.read_json(r"players.json")
players.drop(columns = ["passportArea", "weight", "firstName" , "middleName",
            "lastName", "currentTeamId", "birthDate", "role", "birthArea", "foot",
                         "currentNationalTeamId", "height"], inplace = True )
players.rename(columns = ({"wyId":"playerId"}), inplace = True)
PlayerList = pd.merge(BestPlayers, players)
PlayerList.drop(columns = ["playerId"], inplace = True)
print("The players that were able to score at least one goal in 8 different intervals are:\n", PlayerList)


# # [CRQ2] Visualize movements and passes on the pitch! 

# ### Considering only the match Barcelona - Real Madrid played on the 6 May 2018:
# ##### visualize with a heatmap the zones where Cristiano Ronaldo was more active. The events to be considered are: passes, shoots, duels, free kicks.
# ##### compare his map with the one of Lionel Messi. Comment the results and point out the main differences (we are not looking for deep and technique analysis, just show us if there are some clear differences between the 2 plots).

# In[36]:



def draw_pitch(axes):
    # focus on only half of the pitch
    # pitch Outline & Centre Line
    pitch = mp.Rectangle([0, 0], width=120, height=80, fill=False)
    # Left, Right Penalty Area and midline
    left_penalty = mp.Rectangle([0, 22.3], width=14.6, height=35.3, fill=False)
    right_penalty = mp.Rectangle([105.4, 22.3], width=14.6, height=35.3, fill=False)
    midline = mp.ConnectionPatch([60, 0], [60, 80], "data", "data")

    # Left, Right 6-yard Box
    left_six_yard = mp.Rectangle([0, 32], width=4.9, height=16, fill=False)
    right_six_yard = mp.Rectangle([115.1, 32], width=4.9, height=16, fill=False)

    # Prepare Circles
    centre_circle = plt.Circle((60, 40), 8.1, color="black", fill=False)
    centre_spot = plt.Circle((60, 40), 0.71, color="black")
    # Penalty spots and Arcs around penalty boxes
    left_pen_spot = plt.Circle((9.7, 40), 0.71, color="black")
    right_pen_spot = plt.Circle((110.3, 40), 0.71, color="black")
    left_arc = mp.Arc((9.7, 40), height=16.2, width=16.2, angle=0, theta1=310, theta2=50, color="black")
    right_arc = mp.Arc((110.3, 40), height=16.2, width=16.2, angle=0, theta1=130, theta2=230, color="black")

    element = [pitch, left_penalty, right_penalty, midline, left_six_yard, right_six_yard, centre_circle,
               centre_spot, right_pen_spot, left_pen_spot, left_arc, right_arc]
    for j in element:
        axes.add_patch(j)


# -----------------------------------------------------------------------
# read the datasets that i need
spagna = pd.read_json("events_Spain.json")
players = pd.read_json("players.json")
players.rename(columns={"wyId": "playerId"}, inplace=True)
spagna = spagna[spagna.matchId == 2565907]
spagna = pd.merge(spagna, players)
# ---------------------------------------------------------
# keep the rows that have "pass", "shot", "free kick" and "duel", the events that interest me
boo = []
for ele in spagna.eventName:
    if ele == "Pass" or ele == "Shot" or ele == "Duel" or ele == "Free Kick":
        boo.append(True)
    else:
        boo.append(False)
spagna = spagna[boo]
# -------------------------------------------------------0-------------------------------
# keep only the messi and ronaldo events
boo = []
for ele in spagna.lastName:
    if ele == "Messi Cuccittini" or ele == "dos Santos Aveiro":
        boo.append(True)
    else:
        boo.append(False)
spagna = spagna[boo]
spagna.reset_index(inplace=True)
spagna.drop(columns=["index"], inplace=True)
# ------------------------------------------------------------------------------------------
# unfold the dictionary with the coordinates into two seperate collumns
location = []
end_location = []
for i in range(len(spagna["positions"])):
    location.append(list(spagna.positions[i][0].values()))
    end_location.append(list(spagna.positions[i][1].values()))
spagna["location"] = location
spagna["end_location"] = end_location
boo = []
# ---------------------------------------------------------------------------------
# now since we're going to check about Messi, i make two different dataframes, one for messi , one for ronaldo
for ele in spagna.lastName:
    if ele == "Messi Cuccittini":
        boo.append(True)
    else:
        boo.append(False)
messi = spagna[boo]
boo = []
for ele in spagna.lastName:
    if ele == "dos Santos Aveiro":
        boo.append(True)
    else:
        boo.append(False)
ronaldo = spagna[boo]
# --------------------------------------------------------------------------------
# and now I plot
fig = plt.figure()  # set up the figures
fig.set_size_inches(14, 10)
ax = fig.add_subplot(1, 1, 1)
draw_pitch(ax)  # overlay our different objects on the pitch
plt.ylim(-1, 81)
plt.xlim(-1, 121)
plt.axis('off')
x_coord = [i[0] for i in ronaldo["location"]]
y_coord = [i[1] for i in ronaldo["location"]]

# shades: give us the heat map we desire
# n_levels: draw more lines, the larger n, the more blurry it looks
sns.kdeplot(x_coord, y_coord, shade="True", color="green", n_levels=30)
plt.show()
fig = plt.figure()  # set up the figures
fig.set_size_inches(14, 10)
ax = fig.add_subplot(1, 1, 1)
draw_pitch(ax)  # overlay our different objects on the pitch
plt.ylim(-1, 81)
plt.xlim(-1, 121)
plt.axis('off')
x_coord = [i[0] for i in messi["location"]]
y_coord = [i[1] for i in messi["location"]]

# shades: give us the heat map we desire
# n_levels: draw more lines, the larger n, the more blurry it looks
sns.kdeplot(x_coord, y_coord, shade="True", color="blue", n_levels=30)
plt.show()


# ### Considering only the match Juventus - Napoli played on the 22 April 2018:
# ##### visualize with arrows the starting point and ending point of each pass done during the match by Jorginho and Miralem Pjanic. Is there a huge difference between the map with all the passes done and the one with only accurate passes? Comment the results and point out the main differences.

# In[ ]:


it = pd.read_json("events_Italy.json")
it = it[it.matchId == 2576295]
players = pd.read_json("players.json")
players.rename(columns={"wyId": "playerId"}, inplace=True)
it = pd.merge(it, players)
# -------------------------------------------------------------------------------------------------------------------
# keep only the passes
is_pass = it.eventName == "Pass"
it = it[is_pass]
# -------------------------------------------------------------------------------------------------
it.reset_index(inplace=True)
it.drop(columns=["index"], inplace=True)
# --------------------------------------------------------------------------------------------------------
# i keep only the passes from jorginho and piatnic
boo = []
for ele in it.firstName:
    if ele == "Miralem" or ele == "Jorge Luiz":
        boo.append(True)
    else:
        boo.append(False)
it = it[boo]
it.reset_index(inplace=True)
it.drop(columns=["index"], inplace=True)
# ---------------------------------------------------------------------------------------------
# make a new column in the dataset for the location adn end location coordinates
location = []
end_location = []
for i in range(len(it["positions"])):
    location.append(list(it.positions[i][0].values()))
    end_location.append(list(it.positions[i][1].values()))
it["location"] = location
it["end_location"] = end_location

# --------------------------------------------------------------------------------------

# check if the passes are successful or not

tag = []
to_remove = []
for i in range(len(it)):
    for j in range(len(it.tags[i])):
        o = it.tags[i][j]["id"]
        if o == 1802 or o == 703:
            tag.append("Lost")
            break
        elif o == 1801 or o == 701:
            tag.append("Won")
            break
        else:
            to_remove.append(i)
            break
# drop element in the tag column like interception
it.drop(index=to_remove, inplace=True)
it = it.reset_index()
it.tags = tag
# -------------------------------------------------------------
# make a different dataframe for the successful passes
boo = []
for ele in it.tags:
    if ele == "Won":
        boo.append(True)
    else:
        boo.append(False)
won = it[boo]
# ---------------------------------------------------------------------------
# plot of the total passes
fig = plt.figure()  # set up the figures
fig.set_size_inches(7, 5)
ax = fig.add_subplot(1, 1, 1)
draw_pitch(ax)  # overlay our different objects on the pitch
for i in range(len(it)):
    # annotate draw an arrow from a current position to pass_end_location
    ax.annotate("", xy=(it.iloc[i]['end_location'][0], it.iloc[i]['end_location'][1]), xycoords='data',
                xytext=(it.iloc[i]['location'][0], it.iloc[i]['location'][1]), textcoords='data',
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="blue"), )
plt.ylim(-2, 82)
plt.xlim(-2, 122)
plt.axis('off')
plt.show()
# -------------------------------------------------------------------
# plot of the successful ones
fig = plt.figure()  # set up the figures
fig.set_size_inches(7, 5)
ax = fig.add_subplot(1, 1, 1)
draw_pitch(ax)  # overlay our different objects on the pitch
for i in range(len(won)):
    # annotate draw an arrow from a current position to pass_end_location
    ax.annotate("", xy=(won.iloc[i]['end_location'][0], won.iloc[i]['end_location'][1]), xycoords='data',
                xytext=(won.iloc[i]['location'][0], won.iloc[i]['location'][1]), textcoords='data',
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="red"), )
plt.ylim(-2, 82)
plt.xlim(-2, 122)
plt.axis('off')
plt.show()


# In[ ]:




