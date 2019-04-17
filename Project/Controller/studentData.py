from Controller import readAMC as ReadAMC
import numpy as np

class StudentData:
    def __init__(self):
        self.computeData()

    def loadData(self, boxes, resultPoints):
        self.organizedTable = resultPoints.T
        df = resultPoints.values
        score_chart_int = df[-1,:].astype(int)
        score_chart_double = [round(x, 2) for x in df[-1,:]]
        mark_chart = np.unique(score_chart_int)
        mark_chart_double = np.unique(score_chart_double)

        eff_chart = []
        eff_chart_double = []

        for i in range(len(mark_chart)):
            effective_chart = np.count_nonzero(score_chart_int == mark_chart[i])
            eff_chart = np.append(eff_chart, effective_chart)

        for i in range(len(mark_chart_double)):
            effective_chart_double = np.count_nonzero(score_chart_double == mark_chart_double[i])
            eff_chart_double = np.append(eff_chart_double, effective_chart_double)

        self.violinX = score_chart_int
        self.pieX = mark_chart
        self.pieY = eff_chart

        self.dataX = mark_chart_double
        self.dataY = eff_chart_double

    def computeData(self):
        self.loadData(*ReadAMC.computeData())

    def updateData(self):
        self.loadData(*ReadAMC.updateData())

    def getScoreTable(self):
        return self.organizedTable
