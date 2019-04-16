import csv
from pathlib import Path
import sqlite3
import pandas as pd
import json
import numpy as np
import os


dataPath = ""
weightPath = ""
coherenceFormulaPath = ""
csvParamsPath = ""
paramsValues = None


def initDirectories(path):
    global dataPath
    global weightPath
    global coherenceFormulaPath
    global csvParamsPath
    dataPath = path
    weightPath = dataPath + "weights.json"
    coherenceFormulaPath = dataPath + "coherenceFormula.json"
    csvParamsPath = dataPath + "basic_parameters.csv"


def setParameters(params):
    global paramsValues
    paramsValues = params




def readAMCTables(dataPath):
    # Create your connection.
    cnx = sqlite3.connect(dataPath + 'capture.sqlite')
    zone = pd.read_sql_query("SELECT * FROM capture_zone", cnx)
    cnx.close()

    cnx = sqlite3.connect(dataPath +'scoring.sqlite')
    answer = pd.read_sql_query("SELECT * FROM scoring_answer", cnx)
    variables = pd.read_sql_query("SELECT * FROM scoring_variables", cnx)
    questiontitle = pd.read_sql_query("SELECT * FROM scoring_title", cnx)
    cnx.close()

    cnx = sqlite3.connect(dataPath +'association.sqlite')
    association = pd.read_sql_query("SELECT * FROM association_association", cnx)
    cnx.close()


    return zone, answer, association, variables,questiontitle



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


def schemeMarkingInQuestion1(boxes, arrParams ):
    #paramsValues order data
    #TP, FN, TN, FP

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
    boxes.loc[ boxes['ticked'] & boxes['correct'], 'points' ] = arrParams['TP']
    boxes.loc[ ~boxes['ticked'] & boxes['correct'], 'points'  ] = arrParams['FN']
    boxes.loc[ ~boxes['ticked'] & ~boxes['correct'], 'points'  ] = arrParams['TN']
    boxes.loc[ boxes['ticked'] & ~boxes['correct'], 'points'  ] = arrParams['FP']

    boxes.loc[ boxes['correct'], 'maxPoints' ] = arrParams['TP']
    boxes.loc[ ~boxes['correct'], 'maxPoints'  ] = arrParams['TN']


def MarkingQuestions(NbPointsQuestions, boxes, avoidNeg=True):
    resultat, resultatsPoints, maxPoints = initResults(NbPointsQuestions, boxes, avoidNeg)
    resultatsPoints = setHeaders(resultatsPoints, maxPoints)

    return resultat, resultatsPoints

def MarkingQuestionsWithCoherence(NbPointsQuestions, boxes, avoidNeg=True):
    listStudents = boxes['student'].unique()
    listQuestions = boxes['question'].unique()
    resultat, resultatsPoints, maxPoints = initResults(NbPointsQuestions, boxes, avoidNeg)

    formulas = parseCoherenceFormula()
    for i, student in enumerate(listStudents):
        # print("Student : " + str(student))
        for question in listQuestions:
            for indexFormula in range(0, len(formulas[0]), len(listStudents)):
                if formulas[0][indexFormula][0] == question:
                    break
            if formulas[0][indexFormula][0] != question:
                continue
            # print("Question : " + str(question))
            # print("indexFormula : " + str(indexFormula))
            # print("Modifier : " + str(formulas[0][indexFormula][1]))
            # print("Note avant : " + str(resultatsPoints.loc[question, student]))
            resultatsPoints.loc[question, student] = resultatsPoints.loc[question, student] + \
                                                     formulas[0][indexFormula + i][1]
            # print("Note après : " + str(resultatsPoints.loc[question, student]))


    resultatsPoints = setHeaders(resultatsPoints, maxPoints)

    for i, student in enumerate(listStudents):
        print("Student : " + str(student))
        if formulas[0][0][0] == -1: # [Modifiers][Tuple][Index]
            resultatsPoints.loc['Note/20 (avec cohérence)', student] = \
                resultatsPoints.loc['Note/20', student] + formulas[0][i][1]
            print("Modifier : " + str(formulas[0][i][1]))
            print("Note avant : " + str(resultatsPoints.loc['Note/20', student]))
            print("Note après : " + str(resultatsPoints.loc['Note/20 (avec cohérence)', student]))

    return resultat, resultatsPoints


def initResults(NbPointsQuestions, boxes, avoidNeg = True):
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

    if avoidNeg: resultat[resultat < 0] = 0

    # Taking into account points per question
    weights = getWeights()
    for question in listQuestions:
        resultatsPoints.loc[question,:] = resultat.loc[question,:]*NbPointsQuestions.loc[question,'Points']\
                                          *weights.loc[weights['question'] == question, 'weight'].item()
    maxPoints = NbPointsQuestions['Points'].sum()


    return resultat, resultatsPoints, maxPoints


def setHeaders(resultatsPoints, maxPoints):
    # Then computes the points per student
    resultatsPoints.loc['Note',:] = resultatsPoints.sum()
    # resultatsPoints.loc['Note/20',:] = 20/maxPoints*resultatsPoints.loc['Note',:] # old formula
    max_mark = resultatsPoints.loc['Note'].max()
    min_mark = resultatsPoints.loc['Note'].min()
    resultatsPoints.loc['Note/' + str(maxPoints), :] = (resultatsPoints.loc['Note',:] / maxPoints) * (max_mark - min_mark) + min_mark
    resultatsPoints.loc['Note/20', :] = (resultatsPoints.loc['Note/' + str(maxPoints)]*20) / maxPoints

    return resultatsPoints


def manageData(option1, option2):
    zone, answer, association, var,_ = readAMCTables(dataPath)
    boxes = makeBoxes(zone, answer, var )

    option1(boxes)

    schemeMarkingInQuestion1(boxes, paramsValues)

    # Example of marking scheme per question
    listQuestions = boxes['question'].unique()
    NbPointsQuestions = pd.DataFrame(index=range(1,listQuestions.shape[0] + 1), columns=['Points'])
    NbPointsQuestions['Points'] = 1

    #get by user or default
    resultat, resultatsPoints = option2(NbPointsQuestions, boxes,avoidNeg=True)
    studentIdToNameMapper = {association.loc[k,'student']: association.loc[k,'manual'] for k in association.index}
    resultatsPoints = resultatsPoints.rename(studentIdToNameMapper, axis=1)
    return boxes, resultatsPoints



def computeDataPart(boxes):
    boxes["weight"] = paramsValues['Weight'] # default weight
    # weights = boxes[['question', 'student', 'weight']]
    weights = boxes[['question', 'weight']]
    weights = weights.drop_duplicates('question')
    writeWeights(weights)


def updateDataPart(boxes):
    rawWeights = parseWeights()
    weights = pd.read_json(rawWeights)
    boxes["weight"] = weights['weight']


def computeData():
    if os.path.isfile(coherenceFormulaPath) and parseCoherenceFormula():
        return computeDataCoherence()
    else:
        return computeDataWeights()

def computeDataWeights():
    return manageData(computeDataPart, MarkingQuestions)

def computeDataCoherence():
    return manageData(computeDataPart, MarkingQuestionsWithCoherence)

def updateData():
    if os.path.isfile(coherenceFormulaPath) and parseCoherenceFormula():
        return updateDataCoherence()
    else:
        return updateDataWeights()


def updateDataWeights():
    return manageData(updateDataPart, MarkingQuestions)


def updateDataCoherence():
    return manageData(updateDataPart, MarkingQuestionsWithCoherence)



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

def getAllStudents():
    boxes, point = updateData()
    listStudents = boxes['student'].unique().tolist()
    return listStudents

def getStudentQuestionsCorrect(student):
    boxes, point = updateData()
    studentQuestionsCorrect = []
    listQuestions = boxes['question'].unique()

    for question in listQuestions:
        value = True
        boxes_onequestion = boxes.loc[(boxes['student'] == student) & (boxes['question'] == question)]
        for i in range(len(boxes_onequestion)):
            value = value and ((boxes_onequestion['correct'].iloc[i] and boxes_onequestion['ticked'].iloc[i])
                           or (not(boxes_onequestion['correct'].iloc[i]) and not(boxes_onequestion['ticked'].iloc[i])))
        studentQuestionsCorrect.append(tuple((question, int(value))))
    return studentQuestionsCorrect

def getStudentAnswersCorrect(student, question):
    boxes, point = updateData()
    studentAnswersCorrect = []
    boxes_onequestion = boxes.loc[(boxes['student'] == student) & (boxes['question'] == question)]
    # listQuestions = boxes_onequestion.unique()
    for i in range(len(boxes_onequestion)):
        value = ((boxes_onequestion['correct'].iloc[i] and boxes_onequestion['ticked'].iloc[i])
                    or (not (boxes_onequestion['correct'].iloc[i]) and not (boxes_onequestion['ticked'].iloc[i])))
        studentAnswersCorrect.append(tuple((boxes_onequestion['answer'].iloc[i], int(value))))
    return studentAnswersCorrect

def writeCoherence(data):
    with open(coherenceFormulaPath, 'w') as out:
        json.dump(data, out, indent=2)

def parseCoherenceFormula():
    if not os.path.isfile(coherenceFormulaPath):
        return False

    with open(coherenceFormulaPath) as f:
        data = json.load(f)
        f.close()

    if data == [[], []]:
        return False

    return data

def getDataPath():
    return dataPath

def getDefaultDataPath():
    return str(Path(__file__).resolve().parent.parent).replace("\\", "/") + "/Real Data/"


#-------------------------------------sahar code---------------------------
def MarkingQuestions2(NbPointsQuestions, boxes, avoidNeg=True):
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

    # compute number of choice for each question
    c = boxes.groupby(['student'])['question'].value_counts().to_frame('count')  # .apply(list).to_dict()
    c2 = pd.DataFrame(c).reset_index()
    c3 = c2.loc[c2['student'] == listStudents[0]]

    return c, c2, c3

def computeData2():
    # dataPath = "D:/Travail/AMC/Project/Real Data/"

    # In[6]:


    zone, answer, association, var,_ = readAMCTables(dataPath)
    boxes = makeBoxes(zone, answer, var )

    boxes["weight"] = 1.0 # default weight
    # weights = boxes[['question', 'student', 'weight']]
    weights = boxes[['question', 'weight']]
    weights = weights.drop_duplicates('question')
    writeWeights(weights)

    schemeMarkingInQuestion1(boxes, paramsValues)


    # In[8]:


    # Example of marking scheme per question
    listQuestions = boxes['question'].unique()
    NbPointsQuestions = pd.DataFrame(index=range(1,listQuestions.shape[0]+1), columns=['Points']  )
    NbPointsQuestions['Points'] = 1


    # In[9]:
    #get by user or default
    c, c2, c3 = MarkingQuestions2(NbPointsQuestions, boxes,avoidNeg=False)
    return c, c2, c3
