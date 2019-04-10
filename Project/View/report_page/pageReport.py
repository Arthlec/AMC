#+----------------------------------------------------+
#| 23/03/2019 - Report page for teachers
#| Created by Sahar Hosseini - Roman Blond
#| description,
#| report data as a table, chart and teachers enable to apply coherence, weight and penalty
#+----------------------------------------------------+
import sys
from PyQt5.QtWidgets import QWidget, QSlider, QGroupBox, QGridLayout, QLineEdit, \
                            QComboBox, QPushButton, QScrollArea, QTableWidget, QTableWidgetItem,  \
                            QVBoxLayout, QLabel

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
    def __init__(self, parent=None):
        super(ReportPage, self).__init__(parent)
        self.plot = PlotCanvas()

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
        for i in range(3):
            layout.setColumnStretch(i, 1)

        # ---------------------text boxes  --------------------
        # Put all of the choices together, linking the name and the function to call
        self.comboOptions = [
            ["Box Chart",     self.plot.plot_box],
            ["Violin Chart",  self.plot.plot_violin],
            ["Line Chart",    self.plot.plot_histogram],
            ["Pie Chart",     self.plot.plot_pie],
        ]

        txtCoherence = QLineEdit("Please Enter your Coherence Formula")
        txtCoherence.resize(20, 20)
        layout.addWidget(txtCoherence, 0, 0)
        cbChart = QComboBox()

        for elt in self.comboOptions:
            cbChart.addItem(elt[0])
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
        self.plot.plot_box()

        layout.addWidget(self.plot, 1, 2)

        self.horizontalGroupBox.setLayout(layout)

    def onClickApply(self):
        print("click: run your coherence and update data ")

    # Calls directly the good function in the array self.comboOptions
    def OnChangeCbChart(self,i):
        self.comboOptions[i][1]()


#+--------------builder slider has been written by Arthur Lecert
class buildSlider(QWidget):
    def __init__(self, parent=None, initialValue=1.0, arrCorrectAns=[], numberOfQuestions=1):
        super(buildSlider, self).__init__(parent)

        # ---------------------weight
        self.layout = QVBoxLayout()
        self.listOfQuestions = []
        for i in range(numberOfQuestions):
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
        slider.setMaximum(2.0)
        slider.setValue(initialValue)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(20)

        self.layout.addWidget(slider)
        slider.valueChanged.connect(lambda: self.valuechange(weightText, slider))

        self.listOfQuestions.append(slider)

    def valuechange(self, weightText, slider):
        weightText.setText(str(slider.value()))

    def writeWeights(self):
        for i, slider in enumerate(self.listOfQuestions):
            changeWeight(i + 1, slider.value())
        updateData()
        # print(getWeights())


class DoubleSlider(QSlider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.decimals = 2
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
#+--------------chart class has been written by Roman Blond

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    report = ReportPage(window)
    report.initUI(window)
    window.showMaximized()
    sys.exit(app.exec_())
