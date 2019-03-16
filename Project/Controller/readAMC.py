#!/usr/bin/env python
# coding: utf-8

# In[1]:

import sqlite3
import pandas as pd
import json

def readAMCTables(dataPath):
    # Create your connection.
    cnx = sqlite3.connect(dataPath + 'capture.sqlite')
    zone = pd.read_sql_query("SELECT * FROM capture_zone", cnx)
    cnx.close()
    
    cnx = sqlite3.connect(dataPath +'scoring.sqlite')
    answer = pd.read_sql_query("SELECT * FROM scoring_answer", cnx)
    variables = pd.read_sql_query("SELECT * FROM scoring_variables", cnx)
    cnx.close()
    
    cnx = sqlite3.connect(dataPath +'association.sqlite')
    association = pd.read_sql_query("SELECT * FROM association_association", cnx)
    cnx.close()
    
    
    return zone, answer, association, variables


# In[ ]:





# In[2]:


def makeBoxes(zone, answer, var ):
    # Creates a table of all boxes in all copies
    # including detection of ticked boxes

    var.index = var['name']
    darkness_threshold = var.loc['darkness_threshold', 'value']
    darkness_threshold_up = var.loc['darkness_threshold_up', 'value']

    boxes = zone[(zone['type']==4)].copy()

    boxes.drop(['type', 'zoneid', 'image', 'imagedata' ], axis=1, inplace=True)
    boxes.columns = ['student', 'page', 'copy', 'question', 'answer', 'total', 'black', 'manual']


    # Box is ticked if black > total*darkness_threshold
    boxes['ticked'] = boxes['black'] > boxes['total']*float(darkness_threshold)
    boxes['ticked'] = boxes['ticked'].astype('bool')

    # This is to take into accound manual correction of detected ticked boxes
    I = boxes['manual'] != -1 
    boxes.loc[I,'manual'] = boxes.loc[I, 'manual'].map({0:False, 1:True}) 
    boxes.loc[I, 'ticked'] = boxes.loc[I,'manual']
    #boxes.loc[:,'ticked']

    # Add a column 'correct' to indicate what is the correct answer
    # Boucler sur les étudiants, les questions, les réponses
    listStudents = boxes['student'].unique()
    listQuestions = boxes['question'].unique()
    for student in [1]: #listStudents:  #Actually all correct answers are the same for all students
        for question in listQuestions:
            K = (answer['student']==student) & (answer['question'] == question)
            listAnswers = answer.loc[K, 'answer'].values
            for answ in listAnswers:
                J = (answer['student']==student) & (answer['question'] == question) & (answer['answer'] == answ)
                out = answer.loc[J,'correct']
                J =  (boxes['question'] == question) &  (boxes['answer'] == answ)
                boxes.loc[J, 'correct'] = bool(out.values)

    return boxes            


# In[3]:


def schemeMarkingInQuestion1(boxes, TP, TN, FP, FN ):
    
# Une Stratégie de notation : 
#
#       |Ticked | Non ticked |
# True  |  1    |   -0.2     |
# False | -0.2  |   +0.3     |
#
#       |Ticked | Non ticked |
# True  |  TP   |   FN     |
# False |  FP   |   TN     |
#
# Adds colums 'points' and 'maxPoints' to the dataframe boxes
# points is the number of points earned for each student and each box

    boxes.loc[ boxes['ticked'] & boxes['correct'], 'points' ] = TP
    boxes.loc[ ~boxes['ticked'] & boxes['correct'], 'points'  ] = FN
    boxes.loc[ ~boxes['ticked'] & ~boxes['correct'], 'points'  ] = TN
    boxes.loc[ boxes['ticked'] & ~boxes['correct'], 'points'  ] = FP
    
    boxes.loc[ boxes['correct'], 'maxPoints' ] = TP
    boxes.loc[ ~boxes['correct'], 'maxPoints'  ] = TN


# In[4]:


def MarkingQuestions1(NbPointsQuestions, boxes,penalty="def", avoidNeg=True):
    from collections import Counter
    # computes the sum of points per student and question
    # result is a a dataframe of the number of points per question (row) 
    # and per student (column)

    listStudents = boxes['student'].unique()
    listQuestions = boxes['question'].unique()
    resultat = pd.DataFrame(index=listQuestions, columns=listStudents)
    resultatsPoints = pd.DataFrame(index=listQuestions, columns=listStudents)


    for student in listStudents:
        for question in listQuestions:
            K = (boxes['student']==student) & (boxes['question'] == question)
            # resultat as a proportion of the possible max
            resultat.loc[question, student] = boxes.loc[K,'points'].sum()/boxes.loc[K,'maxPoints'].sum()
            resultatsPoints.loc[question, student] = boxes.loc[K,'points'].sum()/boxes.loc[K,'maxPoints'].sum()

    # compute number of choice for each question use in penalty
    c = boxes.groupby(['student'])['question'].value_counts().to_frame('count')  # .apply(list).to_dict()
    c2 = pd.DataFrame(c).reset_index()
    c3 = c2.loc[c2['student'] == listStudents[0]]
    # print(resultat)
    # then avoid negative points for questions
    if avoidNeg: resultat[resultat < 0] = 0
    else:#penalty 1/(n-1) default or get by teacher as entry
        if(penalty=="def"):
            for q in c3['question']:
                for std in listStudents:
                    if resultat.loc[q,std]<0:
                        count=c3.loc[c3['question'] == q, 'count'].iloc[0]
                        resultat.loc[q,std]=round(1/(count -1), 1)
        else:
             resultat[resultat < 0] = penalty

    # Taking into account points per question
    maxPoints = NbPointsQuestions['Points'].sum()
    for question in listQuestions:
        resultatsPoints.loc[question,:] = resultat.loc[question,:]*NbPointsQuestions.loc[question,'Points']

    # Then computes the points per student

    resultatsPoints.loc['Note',:] = resultatsPoints.sum()
    resultatsPoints.loc['Note/20',:] = 20/maxPoints*resultatsPoints.loc['Note',:]
    return resultat, resultatsPoints


# In[ ]:





# In[ ]:





# ## Example
# 
# Data are given as an example in data.zip

# In[5]:

def computeData():
    dataPath = "C:/Users/Arthur/PycharmProjects/AMC/Project/Real Data/"


    # In[6]:


    zone, answer, association, var = readAMCTables(dataPath)
    boxes = makeBoxes(zone, answer, var )
    boxes["weight"] = 0.5
    schemeMarkingInQuestion1(boxes, 1, 0., -0.2, -0.2)


    # In[8]:


    # Example of marking scheme per question
    # import pandas as pd
    listQuestions = boxes['question'].unique()
    NbPointsQuestions = pd.DataFrame(index=range(1,listQuestions.shape[0]+1), columns=['Points']  )
    NbPointsQuestions['Points'] = 1


    # In[9]:
    #get by user or default
    resultat, resultatsPoints = MarkingQuestions1(NbPointsQuestions, boxes,penalty="def",avoidNeg=False)


    # In[10]:


    # resultatsPoints


    # In[13]:


    studentIdToNameMapper = {association.loc[k,'student']: association.loc[k,'manual'] for k in association.index}


    # In[16]:


    resultatsPoints = resultatsPoints.rename(studentIdToNameMapper, axis=1)

    # print(boxes)
    # print(resultatsPoints.head())
    # print(boxes.loc[(boxes['question'] == 1) & (boxes['student'] == 26)].iloc[0])

    weights = boxes[['question', 'student', 'weight']]
    writeWeights(weights)

    return boxes.loc[(boxes['question'] == 1) & (boxes['student'] == 26)].iloc[0]['weight']

def changeWeight(value):
    rawWeights = parseWeights('../View/weights.json')
    weights = pd.read_json(rawWeights)
    weights['weight'] = value
    print(weights)
    writeWeights(weights)

def parseWeights(fileName):
    with open(fileName) as f:
        data = json.load(f)
        f.close()
    return data

def writeWeights(data):
    with open('weights.json', 'w') as out:
        json.dump(data.to_json(), out, indent=2)