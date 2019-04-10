import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy

# For the charts part
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# For the violin chart
import seaborn as sns
import matplotlib.pyplot as plt

from Controller import readAMC as ReadAMC

# PlotCanvas is also a QWidget
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.computeData()

    def computeData(self):
        std, points = ReadAMC.computeData()
        df = points
        df = df.as_matrix()
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


    def setTitle(self):
        self.axes.set_title('Repartition of score in the class')


    def plot_histogram(self):
        self.axes.cla()       # Clears the axes
        self.axes.plot(self.dataX, self.dataY)
        self.setTitle()
        self.draw()

    def plot_pie(self):
        self.axes.cla()
        self.axes.pie(self.dataY, labels=self.dataX)
        self.setTitle()
        self.draw()

    def plot_box(self):
        self.axes.cla()
        self.axes.boxplot(self.dataX)
        self.setTitle()
        self.draw()

    def plot_violin(self):
        pass
        # sns.set
        # sns.violinplot(data=X)
        # sns.set()
        # tips = sns.load_dataset("tips")
        # ax = sns.violinplot(x=tips["total_bill"])
        # self.sns.plt.show()

        # self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Chart()
    sys.exit(app.exec_())
