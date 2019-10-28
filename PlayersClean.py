import pandas as pd
p = pd.read_json("E:\ADM HW2\players.json")
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
