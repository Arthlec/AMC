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
    def __init__(self,dataX, dataY, parent=None, width=5, height=4, dpi=100):
        self.dataX = dataX
        self.dataY = dataY

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


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
        self.axes.cla()
        self.axes.violinplot(self.dataX)
        self.setTitle()
        self.draw()

    def plot_histo__by_question(self):
        self.axes.cla()
        self.axes.plot(self.dataX, self.dataY)
        self.setTitle()
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Chart()
    sys.exit(app.exec_())
