import sys


def computeQuestionsPoints(stdScore) :
    stdQuestionsPoints = {}
    for i in stdScore :
        score = 0
        for j in stdScore[i] :
            # print(stdScore[i][j]['ans'])
            if stdScore[i][j]['ans'] == True:
                score += stdScore[i][j]['b']
            else :
                score += stdScore[i][j]['m']
        stdQuestionsPoints["student_" + str(i)] = score
    return stdQuestionsPoints

def computeFinalMark(stdQuestionPoints, stdScore):
    stdFinalMark = {}
    maxScore = 0
    maxMark = 0
    minMark = 0

    for i in stdScore["student_0"] :
        maxMark += stdScore["student_0"][i]['b']
        minMark += stdScore["student_0"][i]['m']
    # print(maxMark)
    # print(minMark)

    for i in stdQuestionPoints :
        if stdQuestionPoints[i] > maxScore:
            maxScore = stdQuestionPoints[i]
    # print(maxScore)

    for i in stdQuestionPoints :
        stdFinalMark[i] = round((stdQuestionPoints[i] / maxScore) * (maxMark - minMark) + minMark, 1)

    return stdFinalMark