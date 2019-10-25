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


# --------------------------------------------------------------------------------------
import pandas as pd
import datetime
from dateutil.parser import parse
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import seaborn as sns

# -----------------------------------------------------------------------
# read the datasets that i need
spagna = pd.read_json("events_Spain.json")
players = pd.read_json("players.json")
players.rename(columns={"wyId": "playerId"}, inplace=True)
spagna = pd.merge(spagna, players)
# ---------------------------------------------------------
# keep the rows that have "pass", "shot", "free kick" and "duel", the events that interest me
boo = []
for ele in spagna.eventName:
    if (ele == "Pass" or ele == "Shot" or ele == "Duel" or ele == "Free Kick"):
        boo.append(True)
    else:
        boo.append(False)
spagna = spagna[boo]
# -------------------------------------------------------0-------------------------------
# keep only the messi and ronaldo events
boo = []
for ele in spagna.lastName:
    if (ele == "Messi Cuccittini" or ele == "dos Santos Aveiro"):
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
    if (ele == "Messi Cuccittini"):
        boo.append(True)
    else:
        boo.append(False)
messi = spagna[boo]
boo = []
for ele in spagna.lastName:
    if (ele == "dos Santos Aveiro"):
        boo.append(True)
    else:
        boo.append(False)
ronaldo = spagna[boo]
# --------------------------------------------------------------------------------
# and now I plot
fig = plt.figure()  # set up the figures
fig.set_size_inches(7, 5)
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
fig.set_size_inches(7, 5)
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