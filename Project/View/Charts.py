from Controller.readAMC import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import matplotlib.mlab as mlab


std, points = computeData()
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
X = mark_chart
Y = eff_chart

X_pie = mark_chart
class Chart(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.title = 'Repartition of score for this MCQ'
        self.width = 600
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        m = PlotCanvas(self, width=5, height=4)
        m.move(0,0)

        self.show()


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
        # self.plot_histogram()
        # self.plot_pie()
        # self.plot_box()
        self.plot_violin()

    def plot_histogram(self):
        ax = self.figure.add_subplot(111)
        ax.plot(X, Y)
        ax.set_title('Repartition of score in the class')
        self.draw()

    def plot_pie(self):
        ax = self.figure.add_subplot(111)
        ax.pie(Y, labels=X_pie)
        ax.set_title('Repartition of score in the class')
        self.draw()

    def plot_box(self):
        ax = self.figure.add_subplot(111)
        ax.boxplot(X)
        ax.set_title('Repartition of score in the class')
        self.draw()

    def plot_violin(self):
        # sns.set
        # sns.violinplot(data=X)
        sns.set()
        tips = sns.load_dataset("tips")
        ax = sns.violinplot(x=tips["total_bill"])
        self.sns.plt.show()

        # self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Chart()
    sys.exit(app.exec_())
