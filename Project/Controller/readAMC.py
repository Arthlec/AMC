import json
import os
import numpy as np
import sqlite3
from pathlib import Path

import pandas as pd

WEIGHTS_FILENAME = "weights.json"
COHERENCE_FILENAME = "coherenceFormula.json"
CAPTURE_FILE = 'capture.sqlite'
SCORING_FILE = 'scoring.sqlite'
ASSOCIATION_FILE = 'association.sqlite'

dataPath = ""
weightPath = ""
coherenceFormulaPath = ""
paramsValues = None
examDate = ""


class _Question():
    def __init__(self, id=None, title=''):
        self.id = id
        self.title = title
        self.answers = {}

    def addAnswer(self, answerId, correct):
        self.answers[answerId] = correct

    def defined(self, answerId):
        return answerId in self.answers


class _Student():
    def __init__(self, id=None, name='', globalResult=None):
        self.id = id
        self.name = name
        self.questions = {}
        self.globalResult = globalResult

    def addAnswer(self, questionId, answerId, ticked):
        if questionId not in self.questions:
            self.questions[questionId] = {}

        self.questions[questionId][answerId] = ticked






def initDirectories(path):
    global dataPath
    global weightPath
    global coherenceFormulaPath
    dataPath = path
    weightPath = dataPath + WEIGHTS_FILENAME
    coherenceFormulaPath = dataPath + COHERENCE_FILENAME


def isValidDirectory(dir):
    return any(fname == CAPTURE_FILE for fname in os.listdir(dir))


def setParameters(params):
    global paramsValues
    paramsValues = params

def setDate(date):
    global examDate
    examDate = date




def readAMCTables(dataPath):
    # Create your connection and return tables needed for computation
    try:
        cnx = sqlite3.connect(dataPath + CAPTURE_FILE)
        zone = pd.read_sql_query("SELECT * FROM capture_zone", cnx)
        cnx.close()
    except pd.io.sql.DatabaseError as e:
        raise IOError('File {0} is missing...'.format(CAPTURE_FILE))

    try:
        cnx = sqlite3.connect(dataPath + SCORING_FILE)
        answer = pd.read_sql_query("SELECT * FROM scoring_answer", cnx)
        variables = pd.read_sql_query("SELECT * FROM scoring_variables", cnx)
        questiontitle = pd.read_sql_query("SELECT * FROM scoring_title", cnx)
        cnx.close()
    except pd.io.sql.DatabaseError as e:
         raise IOError('File {0} is missing...'.format(SCORING_FILE))

    try:
        cnx = sqlite3.connect(dataPath + ASSOCIATION_FILE)
        association = pd.read_sql_query("SELECT * FROM association_association", cnx)
        cnx.close()
    except pd.io.sql.DatabaseError as e:
         raise IOError('File {0} is missing...'.format(ASSOCIATION_FILE))

    return zone, answer, association, variables, questiontitle


def getAMCQuestionTitle():
    try:
        cnx = sqlite3.connect(dataPath + SCORING_FILE)
        questionTitle = pd.read_sql_query("SELECT * FROM scoring_title", cnx)
        cnx.close()
    except pd.io.sql.DatabaseError as e:
         raise IOError('File {0} is missing...'.format(SCORING_FILE))

    return questionTitle


def getAMCAssociations():
    try:
        cnx = sqlite3.connect(dataPath + ASSOCIATION_FILE)
        association = pd.read_sql_query("SELECT * FROM association_association", cnx)
        cnx.close()
    except pd.io.sql.DatabaseError as e:
         raise IOError('File {0} is missing...'.format(ASSOCIATION_FILE))

    return association



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
    # listStudents = boxes['student'].unique()
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
    #       |Ticked | Non ticked |
    # True  |  1    |   -0.2     |
    # False | -0.2  |   +0.3     |
    #
    #       |Ticked | Non ticked |
    # True  |  TP   |    FN      |
    # False |  FP   |    TN      |
    #
    # Adds colums 'points' and 'maxPoints' to the dataframe boxes
    # points is the number of points earned for each student and each box
    boxes.loc[ boxes['ticked'] & boxes['correct'], 'points' ] = arrParams['TP']
    boxes.loc[ ~boxes['ticked'] & boxes['correct'], 'points'  ] = arrParams['FN']
    boxes.loc[ ~boxes['ticked'] & ~boxes['correct'], 'points'  ] = arrParams['TN']
    boxes.loc[ boxes['ticked'] & ~boxes['correct'], 'points'  ] = arrParams['FP']

    boxes.loc[ boxes['correct'], 'maxPoints' ] = arrParams['TP']
    boxes.loc[ ~boxes['correct'], 'maxPoints'  ] = arrParams['TN']


def MarkingQuestions(NbPointsQuestions, boxes, avoidNeg):
    # Computes the result without coherence
    resultat, resultatsPoints, maxPoints = initResults(NbPointsQuestions, boxes, avoidNeg)
    resultatsPoints = setHeaders(resultatsPoints, maxPoints)

    return resultat, resultatsPoints

def MarkingQuestionsWithCoherence(NbPointsQuestions, boxes, avoidNeg):
    # Computes the result with coherence
    listStudents = boxes['student'].unique()
    listQuestions = boxes['question'].unique()
    resultat, resultatsPoints, maxPoints = initResults(NbPointsQuestions, boxes, avoidNeg)

    formulas = parseCoherenceFormula()

    # Coherence for questions
    for i, student in enumerate(listStudents):
        for question in listQuestions:
            for indexFormula in range(0, len(formulas[0]), len(listStudents)):
                if formulas[0][indexFormula][0] == question:
                    break
            if formulas[0][indexFormula][0] != question:
                continue
            resultatsPoints.loc[question, student] = resultatsPoints.loc[question, student] + \
                                                     formulas[0][indexFormula + i][1]

    resultatsPoints = setHeaders(resultatsPoints, maxPoints)

    # Coherence for the entire exam
    for i, student in enumerate(listStudents):
        if formulas[0][0][0] == -1: # [Modifiers][Tuple][Index] depending on the structure of the coherenceFormula.json file
            resultatsPoints.loc['Note/20 (avec cohérence)', student] = \
                resultatsPoints.loc['Note/20', student] + formulas[0][i][1]

    resultatsPoints[resultatsPoints < 0] = 0.0
    resultatsPoints[resultatsPoints > 20] = 20.0

    return resultat, resultatsPoints


def initResults(NbPointsQuestions, boxes, avoidNeg):
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
    # Computes the points per student
    resultatsPoints.loc['Nombre Points',:] = resultatsPoints.sum()
    max_mark = 20
    min_mark = 0
    resultatsPoints.loc['Note/20', :] = (resultatsPoints.loc['Nombre Points',:] / maxPoints) * (max_mark - min_mark) + min_mark

    return resultatsPoints


def manageData(option1, option2):
    # Global function for the marking system
    # option1 is a function which computes with weights or not (NOT A BOOLEAN)
    # option2 is a function which computes with coherence or not (NOT A BOOLEAN)
    zone, answer, association, var,_ = readAMCTables(dataPath)
    boxes = makeBoxes(zone, answer, var )

    option1(boxes)

    schemeMarkingInQuestion1(boxes, paramsValues)

    # Example of marking scheme per question
    listQuestions = boxes['question'].unique()
    NbPointsQuestions = pd.DataFrame(index=range(1,listQuestions.shape[0] + 1), columns=['Points'])
    NbPointsQuestions['Points'] = 1

    # Final computation + mapping for student id to name
    resultat, resultatsPoints = option2(NbPointsQuestions, boxes, (not paramsValues['NegPoints']))
    studentIdToNameMapper = {association.loc[k,'student']: association.loc[k,'manual'] for k in association.index}
    resultatsPoints = resultatsPoints.rename(studentIdToNameMapper, axis=1)
    letterGrade = []
    for key, grade in resultatsPoints.iloc[-1].iteritems():
        if grade < 5:
            letter = 'F'
        elif grade < 10:
            letter = 'Fx'
        elif grade < 12:
            letter = 'E'
        elif grade < 14:
            letter = 'D'
        elif grade < 16:
            letter = 'C'
        elif grade < 18:
            letter = 'B'
        else:
            letter = 'A'
        letterGrade.append(letter)

    df1 = resultatsPoints.iloc[:-1].copy()
    dfG = pd.DataFrame(np.array(letterGrade).reshape(1,len(resultatsPoints.columns)), columns=resultatsPoints.columns.values, index=['Grade'])
    df2 = resultatsPoints.iloc[-1:].copy()
    resultatsPoints = df1.append(dfG)
    resultatsPoints = resultatsPoints.append(df2)
    return boxes, resultatsPoints



def computeDataPart(boxes):
    # Computes with default weights
    boxes["weight"] = paramsValues['Weight'] # default weight
    weights = boxes[['question', 'weight']]
    weights = weights.drop_duplicates('question')
    writeWeights(weights)


def updateDataPart(boxes):
    # Computes with new weights from the file weights.json
    weights = getWeights()
    listQuestions = boxes['question'].unique()
    for question in listQuestions:
        boxes.loc[boxes["question"] == question, "weight"] = weights.loc[weights["question"] == question, "weight"].item()


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
    return weights

def getNumberOfQuestions():
    boxes, resultatsPoints = updateData()
    listQuestions = boxes['question'].unique()
    numberOfQuestions = len(listQuestions)
    return numberOfQuestions

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

def getStudentQuestionsCorrect(student, boxes):
    # For each question returns true if the student answer correctly to all the choices and therefore question is correct
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

def getStudentAnswersCorrect(student, question, boxes):
    # For each question, for each choice, returns true if a student answers correctly for this choice
    studentAnswersCorrect = []
    boxes_onequestion = boxes.loc[(boxes['student'] == student) & (boxes['question'] == question)]
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

    # If there is no formula
    if data == [[], []]:
        return False

    return data

def getDataPath():
    return dataPath


def getStudentsAndQuestions():
    # Returns the list of students and their id and the list of questions
    boxes, resultatsPoints = updateData()
    association = getAMCAssociations()
    questionTitle = getAMCQuestionTitle()


    allStudents = {}
    allQuestions = {}

    for index, row in boxes.iterrows():
        questionId = row['question']
        studentId = row['student']

        if studentId not in allStudents:
            studentInfo = association.loc[association['student'] == studentId]
            studentName = studentInfo['manual'].item()
            allStudents[studentId] = _Student(id=studentId, name=studentName, globalResult=round(resultatsPoints.iloc[-1].loc[studentName], 2))

        allStudents[studentId].addAnswer(row['question'], row['answer'], row['ticked'])

        if questionId not in allQuestions:
            allQuestions[questionId] = _Question(id=row['question'], title=questionTitle.iloc[row['question'] - 1]['title'].encode('latin-1').decode('utf-8'))

        if not allQuestions[questionId].defined(row['answer']):
            allQuestions[questionId].addAnswer(row['answer'], row['correct'])

    return allQuestions, allStudents
