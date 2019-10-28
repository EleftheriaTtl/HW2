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
