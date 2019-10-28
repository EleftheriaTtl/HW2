import pandas as pd
t = pd.read_json("teams.json")
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
