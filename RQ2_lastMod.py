#!/usr/bin/env python
# coding: utf-8


def compute_contingency_table(dataset):

    import pandas 

    import datetime

    from dateutil.parser import parse

    from collections import defaultdict

    import matplotlib.pyplot as plt

    import scipy.stats as scs

    #--------------------------------------------------------------------------------

    #read my file


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

    #Calculate contingency table of 5 teams: Burnley, Arsenal,West Bromwich Albion,Manchester City, Liverpool
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

##CHI_SQUARED_RESULTS: The null hypothesis isn't rejected because the p-value is high.  

