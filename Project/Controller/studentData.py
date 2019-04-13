from Controller import readAMC as ReadAMC
import numpy as np

class StudentData:
    def __init__(self):
        self.computeData()

    def loadData(self, boxes, resultPoints):
        # print(resultPoints)
        # print(resultPoints.T)
        self.organizedTable = resultPoints.T
        # print("organizedTable: \n", self.organizedTable)
        df = resultPoints.values
        # print('df: ', df)
        score_chart = df[10,:].astype(int)
        # print("score_chart: ", score_chart)
        mark_chart = np.unique(score_chart)
        # print("mark_chart: ", mark_chart)
        eff_chart = []

        for i in range(len(mark_chart)):
            effective_chart = []
            effective_chart = np.count_nonzero(score_chart == mark_chart[i])
            eff_chart = np.append(eff_chart, effective_chart)
        # print(eff_chart.astype(int))
        self.dataX = mark_chart
        self.dataY = eff_chart

    def computeData(self):
        self.loadData(*ReadAMC.computeData())

    def updateData(self):
        self.loadData(*ReadAMC.updateData())

    def getScoreTable(self):
        return self.organizedTable
