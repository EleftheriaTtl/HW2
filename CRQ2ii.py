def draw_pitch(ax):
    # focus on only half of the pitch
    # Pitch Outline & Centre Line
    Pitch = mp.Rectangle([0, 0], width=120, height=80, fill=False)
    # Left, Right Penalty Area and midline
    LeftPenalty = mp.Rectangle([0, 22.3], width=14.6, height=35.3, fill=False)
    RightPenalty = mp.Rectangle([105.4, 22.3], width=14.6, height=35.3, fill=False)
    midline = mp.ConnectionPatch([60, 0], [60, 80], "data", "data")

    # Left, Right 6-yard Box
    LeftSixYard = mp.Rectangle([0, 32], width=4.9, height=16, fill=False)
    RightSixYard = mp.Rectangle([115.1, 32], width=4.9, height=16, fill=False)

    # Prepare Circles
    centreCircle = plt.Circle((60, 40), 8.1, color="black", fill=False)
    centreSpot = plt.Circle((60, 40), 0.71, color="black")
    # Penalty spots and Arcs around penalty boxes
    leftPenSpot = plt.Circle((9.7, 40), 0.71, color="black")
    rightPenSpot = plt.Circle((110.3, 40), 0.71, color="black")
    leftArc = mp.Arc((9.7, 40), height=16.2, width=16.2, angle=0, theta1=310, theta2=50, color="black")
    rightArc = mp.Arc((110.3, 40), height=16.2, width=16.2, angle=0, theta1=130, theta2=230, color="black")

    element = [Pitch, LeftPenalty, RightPenalty, midline, LeftSixYard, RightSixYard, centreCircle,
               centreSpot, rightPenSpot, leftPenSpot, leftArc, rightArc]
    for i in element:
        ax.add_patch(i)


# -----------------------------------------------------------------------------------------------------------------
import pandas as pd
import datetime
from dateutil.parser import parse
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import seaborn as sns

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
    if (ele == "Miralem" or ele == "Jorge Luiz"):
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
    if (ele == "Won"):
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