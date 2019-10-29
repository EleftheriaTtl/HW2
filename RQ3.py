import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
# -----------------------------------------------------------------------------------------
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
#----------------------------------------------------------------------------------------
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
    plt.figure(figsize=(14, 14))
    sns.boxplot( y=all_the_coaches["Age"] ).set_title("Distribution of the coaches' age")

eng = pd.read_json("matches_England.json")
c = pd.read_json("coaches.json")
t = pd.read_json("teams.json")
RQ3(c,t,eng)

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

