#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas
events = pandas.read_json(r"C:\Users\lucy_\Downloads\events\events_England.json")


# In[2]:


a=[] #listofvalues(tags_values)
for tag in events.tags:
    b=[] #list_to_replace_dictonaries
    for dictonary in tag:
        for var in dictonary.values():
            var=int(var)
        b.append(var)
    a.append(b)


# In[4]:


for lis in a:
    while(len(lis)>1):
        for elem in lis:
            if elem!=101:
                lis.remove(elem)


# In[10]:


for lis in a:
    
    for elem in lis:
        if elem>101 or elem<101:
            lis.remove(elem)


# In[6]:


def convert(list): 
      
    # Converting integer list to string list 
    s = [str(i) for i in list] 
      
    # Join list items using join() 
    res = int("".join(s)) 
      
    return(res)


# In[13]:


for tag in a:
    if tag==[]:
        tag.append(0)


# In[15]:


result=[]
for tag in a:
    result.append(convert(tag))


# In[22]:


result=[]
for tag in a:
    result.append(convert(tag))


# In[24]:


events.tags=result


# In[26]:


final=events[(events.tags==101)][['teamId','tags','eventSec']]


# In[28]:


final=events[(events.tags==101)][['tags','playerId']]


# In[29]:


final=final.groupby(['playerId',]).size().to_frame('goalNumber').reset_index().sort_values(['playerId', 'goalNumber'], ascending=[True, False])


# In[30]:


players = pandas.read_json(r"C:\Users\lucy_\Downloads\players.json")


# In[31]:


Nations=players.merge(final, left_on='wyId', right_on='playerId')


# In[32]:


nations=[] #listofvalues(tags_values)
for i in range(len(Nations.birthArea)):
    
     #list_to_replace_dictonaries
    
    nations.append(Nations.birthArea[i]['name'])


# In[33]:


Nations.birthArea=nations


# In[34]:


nations_GN=Nations.groupby(['birthArea',]).size().to_frame('goalNumber').reset_index().sort_values(['birthArea', 'goalNumber'], ascending=[True, False])


# In[49]:


import numpy as np
import matplotlib.pyplot as plt

ax = nations_GN.plot.bar()

