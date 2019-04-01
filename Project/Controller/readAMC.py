#!/usr/bin/env python
# coding: utf-8

# In[1]:
from pathlib import Path
import sqlite3
import pandas as pd
import json
import numpy as np

dataPath = str(Path(__file__).resolve().parent.parent).replace("\\", "/") + "/Real Data/"
weightPath = dataPath + "weights.json"
coherenceFormulaPath = dataPath + "coherenceFormula.json"
print("dataPath : " + str(dataPath))
print("weightPath : " + str(weightPath))
print("coherenceFormulaPath : " + str(coherenceFormulaPath))

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
    weights = getWeights()
    for question in listQuestions:
        resultatsPoints.loc[question,:] = resultat.loc[question,:]*NbPointsQuestions.loc[question,'Points']\
                                          *weights.loc[weights['question'] == question, 'weight'].item()

    # Then computes the points per student
    resultatsPoints.loc['Note',:] = resultatsPoints.sum()
    # resultatsPoints.loc['Note/20',:] = 20/maxPoints*resultatsPoints.loc['Note',:] # old formula
    max_mark = resultatsPoints.loc['Note'].max()
    min_mark = resultatsPoints.loc['Note'].min()
    resultatsPoints.loc['Note/' + str(maxPoints), :] = (resultatsPoints.loc['Note',:] / maxPoints) * (max_mark - min_mark) + min_mark
    resultatsPoints.loc['Note/20', :] = (resultatsPoints.loc['Note/' + str(maxPoints)]*20) / maxPoints
    return resultat, resultatsPoints

# In[5]:

def computeData():
    # dataPath = "D:/Travail/AMC/Project/Real Data/"

    # In[6]:


    zone, answer, association, var = readAMCTables(dataPath)
    boxes = makeBoxes(zone, answer, var )

    boxes["weight"] = 1.0 # default weight
    # weights = boxes[['question', 'student', 'weight']]
    weights = boxes[['question', 'weight']]
    weights = weights.drop_duplicates('question')
    writeWeights(weights)

    schemeMarkingInQuestion1(boxes, 1, 0., -0.2, -0.2)


    # In[8]:


    # Example of marking scheme per question
    listQuestions = boxes['question'].unique()
    NbPointsQuestions = pd.DataFrame(index=range(1,listQuestions.shape[0]+1), columns=['Points']  )
    NbPointsQuestions['Points'] = 1


    # In[9]:
    #get by user or default
    resultat, resultatsPoints = MarkingQuestions1(NbPointsQuestions, boxes,penalty="def",avoidNeg=False)

    # In[13]:


    studentIdToNameMapper = {association.loc[k,'student']: association.loc[k,'manual'] for k in association.index}


    # In[16]:


    resultatsPoints = resultatsPoints.rename(studentIdToNameMapper, axis=1)

    return boxes, resultatsPoints

def updateData():
    zone, answer, association, var = readAMCTables(dataPath)
    boxes = makeBoxes(zone, answer, var)

    rawWeights = parseWeights()
    weights = pd.read_json(rawWeights)
    boxes["weight"] = weights['weight']  # default weight

    schemeMarkingInQuestion1(boxes, 1, 0., -0.2, -0.2)

    # In[8]:

    # Example of marking scheme per question
    listQuestions = boxes['question'].unique()
    NbPointsQuestions = pd.DataFrame(index=range(1, listQuestions.shape[0] + 1), columns=['Points'])
    NbPointsQuestions['Points'] = 1

    # In[9]:
    # get by user or default
    resultat, resultatsPoints = MarkingQuestions1(NbPointsQuestions, boxes, penalty="def", avoidNeg=False)

    # In[13]:

    studentIdToNameMapper = {association.loc[k, 'student']: association.loc[k, 'manual'] for k in association.index}

    # In[16]:

    resultatsPoints = resultatsPoints.rename(studentIdToNameMapper, axis=1)

    return boxes, resultatsPoints

def updateCoherence():
    boxes, resultatsPoints = updateData()
    listOfModifiers = parseCoherenceFormula()


def getWeights():
    rawWeights = parseWeights()
    weights = pd.read_json(rawWeights)

    # weights = boxes.loc[boxes['student'] == 26]
    # weights = weights[['question', 'weight']]
    # weights = weights.drop_duplicates('question')
    # weights = weights.sort_values(by=['question'])

    return weights

def getNumberOfQuestions():
    boxes, point = updateData()

    questions = boxes.loc[boxes['student'] == 26]
    questions = questions[['question']]
    questions = questions.drop_duplicates('question')
    numberOfQuestions = len(questions)
    #add by SAHAR TO RETURN PEERCENTAGE
    correctAns=[]
    for i in range(len(questions)):
        correctAns.append(round((np.sum(point.iloc[i]) * 100) / 26,0))

    return numberOfQuestions, correctAns

def changeWeight(indexOfQuestion, value):
    weights = getWeights()
    weights.loc[weights['question'] == indexOfQuestion, 'weight'] = value
    writeWeights(weights)

def parseWeights():
    with open(weightPath) as f:
        data = json.load(f)
        f.close()
    return data

def writeWeights(data):
    with open(weightPath, 'w') as out:
        json.dump(data.to_json(), out, indent=2)

def getAllStudentQuestions():
    boxes, point = updateData()
    allStudentQuestions = []

    listStudents = boxes['student'].unique()
    listQuestions = boxes['question'].unique()

    for student in listStudents:
        for question in listQuestions:
            value = True
            boxes_onestudent_onequestion = boxes.loc[(boxes['student'] == student) & (boxes['question'] == question)]

            for i in range(len(boxes_onestudent_onequestion)):
                value = value and ((boxes_onestudent_onequestion['correct'].iloc[i] and boxes_onestudent_onequestion['ticked'].iloc[i])
                                   or (not(boxes_onestudent_onequestion['correct'].iloc[i]) and not(boxes_onestudent_onequestion['ticked'].iloc[i])))
            for index in list(boxes_onestudent_onequestion.index):
                allStudentQuestions.append(tuple((index, int(value))))
    return allStudentQuestions

def getAllStudentAnswers():
    boxes, point = updateData()
    allStudentAnswers = []
    for i in range(len(boxes)):
        allStudentAnswers.append(tuple((list(boxes.index)[i], int(boxes['correct'].iloc[i] and boxes['ticked'].iloc[i]))))
    return allStudentAnswers

def writeCoherence(data):
    with open(coherenceFormulaPath, 'w') as out:
        json.dump(data.to_json(), out, indent=2)

def parseCoherenceFormula():
    with open(coherenceFormulaPath) as f:
        data = json.load(f)
        f.close()
    return data

boxes , resultatsPoints = computeData()
# print(boxes.columns)
print(boxes)
# print(boxes['total'])
# print(boxes['ticked'])

# boxes_by_student = boxes.groupby('student')
# boxes_by_student_by_question = boxes_by_student.groupby('question')
# print(boxes_by_student_by_question)
# print(int(boxes['correct'].iloc[3] and boxes['ticked'].iloc[3]))
# print(list(boxes['question']))
# print(boxes.loc[(boxes['student'] == 26) & (boxes['question'] == 4) ])
# print(boxes.loc[boxes['student'] == 26, boxes['question'] == 4])
# getAllStudentQuestions()
print(getAllStudentQuestions())
# print(getAllStudentAnswers())