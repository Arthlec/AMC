from Controller import readAMC as ReadAMC
import numpy as np

class StudentData:
    def __init__(self):
        self.loadData()

    def loadData(self):
        boxes, resultPoints = ReadAMC.computeData()
        # print(resultPoints)
        # print(resultPoints.T)
        self.organizedTable = resultPoints.T
        df = resultPoints.as_matrix()
        # print(df)
        score_chart = df[10,:].astype(int)
        # print(score_chart)
        mark_chart = np.unique(score_chart)
        # print(mark_chart)
        eff_chart = []

        for i in range(len(mark_chart)):
            effective_chart = []
            effective_chart = np.count_nonzero(score_chart == mark_chart[i])
            eff_chart = np.append(eff_chart, effective_chart)
        # print(eff_chart.astype(int))
        self.dataX = mark_chart
        self.dataY = eff_chart

    def getScoreTable(self):
        return self.organizedTable
