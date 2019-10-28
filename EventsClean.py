import pandas as pd


def events_clean(e):
    location = []
    end_location = []
    to_remove = []
    e = e[pd.notnull(e['tags'])]
    e = e[pd.notnull(e["positions"])]
    e.reset_index(inplace=True)
    for i in range(len(e["positions"])):
        if len(e["positions"][i]) > 1:
            location.append(list(e.positions[i][0].values()))
            end_location.append(list(e.positions[i][1].values()))
        else:
            to_remove.append(i)
    e.drop(index=to_remove, inplace=True)
    e["Location"] = location
    e["EndLocation"] = end_location
    e.drop(columns=["positions", "index"], inplace=True)
    e.reset_index(inplace=True)
    to_remove = []
    tag = []
    for i in range(len(e.tags)):
        nest = []
        if len(e.tags[i]) > 0:
            for j in range(len(e.tags[i])):
                nest.append(e.tags[i][j]["id"])
            tag.append(nest)
        else:
            to_remove.append(i)
    e.reset_index(inplace=True)
    e.drop(index=to_remove, columns=["level_0", "index", "id", "tags"], inplace=True)
    e.rename(columns={"eventName": "EventName", "eventId": "EventId", "eventSec": "EventSeconds", "matchId": "MatchId",
                      "matchPeriod": "MatchPeriod",
                      "playerId": "PlayerId", "subEventId": "SubEventId", "subEventName": "SubEventName",
                      "tags": "Tags",
                      "teamId": "TeamId"}, inplace=True)
    e['Tags'] = tag
    return e

