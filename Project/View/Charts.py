import sys

from PyQt5.QtWidgets import QApplication, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# PlotCanvas is also a QWidget
class PlotCanvas(FigureCanvas):
    def __init__(self, controller, parent=None, width=5, height=4, dpi=100):
        self.controller = controller

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def refresh(self):
        self.controller.updateData()


    def setTitle(self):
        self.axes.set_title('Repartition of score in the class')


    def plot_line(self):
        self.axes.cla()       # Clears the axes
        self.axes.plot(self.controller.dataX, self.controller.dataY)
        self.setTitle()
        self.draw()

    def plot_pie(self):
        self.axes.cla()
        self.axes.pie(self.controller.pieY, labels=self.controller.pieX)
        self.setTitle()
        self.draw()

    def plot_box(self):
        self.axes.cla()
        self.axes.boxplot(self.controller.dataX)
        self.setTitle()
        self.draw()

    def plot_violin(self):
        self.axes.cla()
        self.axes.violinplot(self.controller.violinX)
        self.setTitle()
        self.draw()

    def plot_histo__by_question(self):
        self.axes.cla()
        self.axes.plot(self.controller.dataX, self.controller.pieY)
        self.setTitle()
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Chart()
    sys.exit(app.exec_())
