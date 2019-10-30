 ##THE GOAL OF THIS ANALYSIS IS TO DISCOVER AND UNDERSTAND WHICH IS THE CORRELATION BETHWEEN NATIONS AND NUMBER OF GOAL OF THIS NATION

    
##WHO WILL BE THE STRONGEST TEAM?

###IMPORTANT! THIS FUNCTION CHANGES THE ORIGINAL DATASET. IF IT IS CALLED TWICE ON ITS OWN RESULT IT WON'T WORK!



    #We have dictionaries in tags column, we just want a string that is the event number, we are interested just in 101 event that is the goal
def calculate_nations_goals(events,players):
    
    import pandas
    import numpy as np
    import matplotlib.pyplot as plt
    
    
    a=[] 

    for tag in events.tags:

        b=[] #list_to_replace_dictonaries

        for dictonary in tag:

            for var in dictonary.values():

                var=int(var)

            b.append(var)

        a.append(b)



    #I remove the number which are different to 101



    for lis in a:

        while(len(lis)>1):

            for elem in lis:

                if elem!=101:

                    lis.remove(elem)



    for lis in a:

        for elem in lis:

            if elem>101 or elem<101:

                lis.remove(elem)




    #this function converts a list into an integer

    def convert(list): 

    # Converting integer list to string list 

        s = [str(i) for i in list] 



        # Join list items using join() 

        res = int("".join(s)) 
        return(res)





   #I put a 0 in all empty list, it's necessary for the conversion

    for tag in a:

        if tag==[]:

            tag.append(0)




    #now i put a list of integer which are the tags' column

    result=[]

    for tag in a:

        result.append(convert(tag))




    events.tags=result



    #These queries calculate the number of goal for each player

    final=events[(events.tags==101)][['teamId','tags','eventSec']]

    final=events[(events.tags==101)][['tags','playerId']]

    final=final.groupby(['playerId',]).size().to_frame('goalNumber').reset_index().sort_values(['playerId', 'goalNumber'], ascending=[True, False])

    Nations=players.merge(final, left_on='wyId', right_on='playerId')

    nations=[] #listofvalues(tags_values)

    for i in range(len(Nations.birthArea)):

        #list_to_replace_dictonaries
        nations.append(Nations.birthArea[i]['name'])

    Nations.birthArea=nations

    #This query modify the dataframe: a column with nations and a corresponding column with goals number

    nations_GN=Nations.groupby(['birthArea',]).size().to_frame('goalNumber').reset_index().sort_values(['birthArea', 'goalNumber'], ascending=[True, False])

    #This is the bar_plot x_ax=Nations y_ax=goals
    
    nations_GN.plot.bar()



  



