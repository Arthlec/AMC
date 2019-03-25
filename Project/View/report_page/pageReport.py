#+----------------------------------------------------+
#| 23/03/2019 - Report page for teachers
#| Created by Sahar Hosseini - Roman Blond
#| description,
#| report data as a table, chart and teachers enable to apply coherence, weight and penalty
#+----------------------------------------------------+
import sys
from PyQt5.QtWidgets import QScrollArea, QApplication, QDialog, QLineEdit, QAction, QTableWidget, QTableWidgetItem, QWidget, \
    QMainWindow, QLabel, QVBoxLayout, QGroupBox, QPushButton, \
    QGridLayout, QHBoxLayout, QTextEdit, QComboBox, QSizePolicy, QSlider
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Controller.readAMC import *
import numpy as np
from View.Charts import *

#+--------------global data that uses in this page
points, stdname = computeData()
df = stdname.as_matrix()
score_chart = df[10,:].astype(int)
print(score_chart)
mark_chart = np.unique(score_chart)
print(mark_chart)
eff_chart = []

for i in range(len(mark_chart)):
    effective_chart = []
    effective_chart = np.count_nonzero(score_chart == mark_chart[i])
    eff_chart = np.append(eff_chart, effective_chart)
print(eff_chart.astype(int))
X = mark_chart
Y = eff_chart
X_pie = ['8','9','12','13','14','15','16']

#+--------------main class
class ReportPage(QWidget):
    def initUI(self, mainWindow):
        mainWindow.title = 'AMC Report'
        self.createGridLayout()
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        mainWindow.setCentralWidget(self)

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("AMC report for teachers")

        # ---------------------grid layout --------------------
        layout = QGridLayout()
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 3)

        # ---------------------text boxes  --------------------
        txtCoherence = QLineEdit("Please Enter your Coherence Formula")
        txtCoherence.resize(20, 20)
        layout.addWidget(txtCoherence, 0, 0)
        cbChart = QComboBox()
        cbChart.addItem("Box Chart")
        cbChart.addItem("Violin Chart")
        cbChart.addItem("Line Chart")
        cbChart.addItem("Pie Chart")
        cbChart.resize(140, 30)
        layout.addWidget(cbChart, 0, 2)
        btnApply = QPushButton("Apply Coherence")
        btnApply.clicked.connect(self.onClickApply)
        layout.addWidget(btnApply, 0, 1)
        cbChart.currentIndexChanged.connect(self.OnChangeCbChart)
        # ---------------------table view --------------------
        scroll = QScrollArea()
        table = QTableWidget()
        scroll.setWidget(table)
        layout.addWidget(table, 1, 0)

        df = stdname.T # main data
        colName = []  # column name
        rowName = []  # row name
        table.setColumnCount(len(df.columns))
        table.setRowCount(len(df.index))
        for i in range(len(df.index)):
            colName.append(str(df.index[i]))
            for j in range(len(df.columns)):
                rowName.append(str(df.columns[j]))
                table.setItem(i, j, QTableWidgetItem(str(round(df.iloc[i, j], 1))))

        table.setHorizontalHeaderLabels(rowName)
        table.setVerticalHeaderLabels(colName)
        table.resizeRowsToContents()
        table.resizeColumnsToContents()

        # ---------------------slider  weight --------------------
        numberOfQuestions, arrCorrectAns = getNumberOfQuestions()
        layout.addWidget(buildSlider(arrCorrectAns=arrCorrectAns,numberOfQuestions=numberOfQuestions), 1, 1)

        # ---------------------chart view --------------------
        self.plot = PlotCanvas()
        self.plot.plot_box()

        layout.addWidget(self.plot, 1, 2)

        self.horizontalGroupBox.setLayout(layout)

    def onClickApply(self):
        print("click: run your coherence and update data ")

    def OnChangeCbChart(self,i):
        print(i)
        if i == 0:
            self.plot.plot_box()
        if i == 1:
            self.plot.plot_violin()
        if i == 2:
            self.plot.plot_histogram()
        if i == 3:
            self.plot.plot_pie()
            print("click: display your chart related to seelcted option ")

#+--------------builder slider has written by Arthur Lecert
class buildSlider(QWidget):
    def __init__(self, parent=None, initialValue=1.0, arrCorrectAns=[], numberOfQuestions=1):
        super(buildSlider, self).__init__(parent)

        # ---------------------weight
        self.layout = QVBoxLayout()
        for i in range(numberOfQuestions):#(1, numberOfQuestions + 1):
            self.addSlider(QLabel("Question " + str(i+1) +"  correctness: " + str(arrCorrectAns[i]) + "  %"), QLabel(str(initialValue)), initialValue)

        self.b1 = QPushButton("Save weight")
        self.b1.setCheckable(True)
        self.b1.toggle()
        self.b1.clicked.connect(self.writeWeights)
        self.layout.addWidget(self.b1)

        self.setLayout(self.layout)
        self.setWindowTitle("Module AMC")

    def addSlider(self, title, weightText, initialValue):
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        weightText.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(weightText)

        slider = DoubleSlider(Qt.Horizontal)
        slider.setMinimum(0.0)
        slider.setMaximum(1.0)
        slider.setValue(initialValue)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(0.1)

        self.layout.addWidget(slider)
        slider.valueChanged.connect(lambda: self.valuechange(weightText, slider))

    def valuechange(self, weightText, slider):
        weightText.setText(str(slider.value()))

    def writeWeights(self):
        n = 1
        print("writeWeights 1")
        print(self.layout.count())
        for i in range(2, self.layout.count(), 3):
            # print(n)
            # print(self.layout.itemAt(i).widget().value())
            changeWeight(n, self.layout.itemAt(i).widget().value())
            n += 1
        print(getWeights())


class DoubleSlider(QSlider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.decimals = 1
        self._max_int = 10 ** self.decimals

        super().setMinimum(0)
        super().setMaximum(self._max_int)

        self._min_value = 0.0
        self._max_value = 1.0

    @property
    def _value_range(self):
        return self._max_value - self._min_value

    def value(self):
        return float(super().value()) / self._max_int * self._value_range + self._min_value

    def setValue(self, value):
        super().setValue(int((value - self._min_value) / self._value_range * self._max_int))

    def setMinimum(self, value):
        if value > self._max_value:
            raise ValueError("Minimum limit cannot be higher than maximum")

        self._min_value = value
        self.setValue(self.value())

    def setMaximum(self, value):
        if value < self._min_value:
            raise ValueError("Minimum limit cannot be higher than maximum")

        self._max_value = value
        self.setValue(self.value())

    def minimum(self):
        return self._min_value

    def maximum(self):
        return self._max_value


def on_click(self):
       textboxValue = self.textbox.text()
       print(textboxValue)
       print("run coherence")
#+--------------chart class has written by Roman Blond

if __name__ == '__main__':


    app = QApplication(sys.argv)
    numberOfQuestions = getNumberOfQuestions()
    print(numberOfQuestions)
    #ex = window(numberOfQuestions=getNumberOfQuestions())
    #ex.show()
    ex1 = App()
    sys.exit(app.exec_())
