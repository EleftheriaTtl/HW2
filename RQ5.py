import pandas as pd
import datetime
from dateutil.parser import parse
import collections
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
#--------------------------------------------------------------------------------
#-------------------------------------------------------------
#E_V_E_N_T_S
#read the database that im interested in
events = pd.read_json("events_England.json")
#check where there is an airduel event and keep only that
is_air_duel = events.subEventName == "Air duel"
events = events[is_air_duel]
#reser the indexes so you make you're analysis more easy
events = events.reset_index()
events.drop(columns = ["index"], inplace = True)
#remove all the null elements
events = events[pd.notnull(events['tags'])]
#update/change your current column tags with the actual result of the duel(won, lost, neutral)
tag = []
to_remove = []
for i in range(len(events)):
    o = events.tags[i][1]["id"]
    if o == 1802 or o == 703:
        tag.append("Lost")
    elif o == 1801 or o == 701:
        tag.append("Won")
    elif o == 702:
        tag.append("Neutral")
    else:
        to_remove.append(i)
events.drop(index= to_remove, inplace = True)
events = events.reset_index()
events.tags = tag
#--------------------------------------------------------------------------------------
#im gonna make two dictionaries(dataframes to be) one for the duels won and one for the total
airduelswon = collections.Counter()
airduelstotal = collections.Counter()
for i in range(len(events)):
    if events.tags[i] == "Won":
        airduelswon[events.playerId[i]] +=1
        airduelstotal[events.playerId[i]] +=1
    else:
        airduelstotal[events.playerId[i]] +=1
air = pd.DataFrame([airduelswon, airduelstotal]).T
air.dropna(inplace = True)
air = air[air[1] > air[1].quantile(0.10)]
#now i have a dataframe where i have my air duels won and the total , where i deleted the row where the total
#airduels where less than the 10%
air.reset_index(inplace = True)
air["ratio"] = round(air[0]/air[1],2)
air.drop(columns = [0, 1], inplace = True)
air.rename(columns = {"index" : "playerId"}, inplace = True)
players = pd.read_json("players.json")
#update/change column to improve readability
players.drop(columns = ["passportArea", "weight", "firstName" , "middleName",
            "lastName", "currentTeamId", "birthDate", "role", "birthArea", "foot",
                        "currentNationalTeamId"], inplace = True )
players.rename(columns = ({"wyId":"playerId"}), inplace = True)
#----------------------------------------------------------------------
#now i have a dataframe with the players height and the ratio of won air duels
kefalies = pd.merge(air,players)
kefalies.drop(columns = ["playerId"], inplace = True)
cat = []
#i fix the category where each players lies, according to their height
for i in range(len(kefalies)):
    if kefalies.height[i]< 160:
        cat.append(" <1,60 ")
    elif 160 <= kefalies.height[i]< 165 :
        cat.append("[1,60 - 1,65)")
    elif 165 <= kefalies.height[i]< 170:
        cat.append("[1,65 - 1,70)")
    elif 170 <= kefalies.height[i]< 175 :
        cat.append("[1,70 - 1,75)")
    elif 175 <= kefalies.height[i]< 180 :
        cat.append("[1,75 - 1,80)")
    elif 180 <= kefalies.height[i]< 185 :
        cat.append("[1,80 - 1,85)")
    elif 185 <= kefalies.height[i]< 190 :
        cat.append("[1,85 - 1,90)")
    elif 190 <= kefalies.height[i]<195 :
        cat.append("[1,90 - 1,95)")
    elif 195 <= kefalies.height[i]<200 :
        cat.append("[1,95 - 2,00)")
    elif kefalies.height[i]>=200:
        cat.append(" >=2,00")
kefalies["Category"] = pd.Categorical(cat)
kefalies.sort_values(by = ["ratio"])
#------------------------------------------------------------------------------
#Plot
sns.set_style("white", {'font.family': ['sans-serif'], 'axes.axisbelow': True})
sns.catplot(x = "height", y = "ratio", hue = "Category", data = kefalies, jitter=False)
