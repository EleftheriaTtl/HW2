import pandas as pd

c = pd.read_json("E:\ADM HW2\coaches.json")
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
    name.append(ele.encode("utf-8"))
c["Name"] = name
#clean up the team id column(there is no team with team id equal to 0
c = c[c.currentTeamId!=0]
c.reset_index(inplace = True)
c.drop(columns=["index", "birthArea", "passportArea", "middleName", "firstName", "lastName", "shortName", "birthDate"], inplace=True)
c.rename(columns = {"currentTeamId": "TeamId", "wyId":"CoachId"}, inplace = True)
