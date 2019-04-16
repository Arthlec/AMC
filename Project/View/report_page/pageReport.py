#+----------------------------------------------------+
#| 23/03/2019 - Report page for teachers
#| Created by Sahar Hosseini - Roman Blond chart
#| description,
#| report data as a table, chart and teachers enable to apply coherence, weight and penalty
#+----------------------------------------------------+
import sys
from PyQt5.QtWidgets import QWidget, QSlider, QGroupBox, QGridLayout, QLineEdit, \
                            QComboBox, QPushButton, QScrollArea, QTableWidget, QTableWidgetItem,  \
                            QVBoxLayout,QHBoxLayout, QLabel, QMainWindow, QApplication

from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# from Controller.readAMC import getNumberOfQuestions, changeWeight
from Controller.readAMC import *
from View.Charts import PlotCanvas
from Controller.studentData import StudentData
from View.coherence_page.coherence import *

#+--------------main class
class ReportPage(QWidget):
    def __init__(self, parent=None):
        super(ReportPage, self).__init__(parent)
        self.controller = StudentData()
        self.plot = PlotCanvas(self.controller.dataX, self.controller.dataY)

    def initUI(self, mainWindow):
        self.mainWindow = mainWindow
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



        #txtCoherence = QLineEdit("Please Enter your Coherence Formula")
        #txtCoherence.resize(20, 20)
        #layout.addWidget(txtCoherence, 0, 0)
        cbChart = QComboBox()

        for elt in self.comboOptions:
            cbChart.addItem(elt[0])
        cbChart.resize(140, 30)
        layout.addWidget(cbChart, 0, 2)
        layout.addWidget(self.createBtnGroup(), 0, 0)
        cbChart.currentIndexChanged.connect(self.OnChangeCbChart)
        # ---------------------table view --------------------
        # scroll = QScrollArea()
        self.table = QTableWidget()
        # scroll.setWidget(table)
        layout.addWidget(self.table, 1, 0)

        self.initData()
        self.sortTable()
        self.setTable()


        # ---------------------slider  weight --------------------
        numberOfQuestions, arrCorrectAns = getNumberOfQuestions()
        layout.addWidget(BuildSlider(self.controller, self.validateWieights, arrCorrectAns=arrCorrectAns,numberOfQuestions=numberOfQuestions), 1, 1)

        # ---------------------chart view --------------------
        self.plot.plot_box()

        layout.addWidget(self.plot, 1, 2)

        self.horizontalGroupBox.setLayout(layout)


    def sortTable(self):
        self.scoreTable.sort_index(inplace=True)
        columns = self.scoreTable.columns
        toSort = []
        notes = []
        for value in columns:
            if isinstance(value, int):
                toSort.append(value)
            else:
                notes.append(value)

        newColumns = sorted(toSort) + notes
        self.scoreTable = self.scoreTable[newColumns]


    def validateWieights(self):
        self.updateData()
        self.setTable()


    # Calls directly the good function in the array self.comboOptions
    def OnChangeCbChart(self,i):
        self.comboOptions[i][1]()


    def initData(self):
        boxes, resultatsPoints = ReadAMC.computeData()
        self.scoreTable = resultatsPoints.T

    def updateDataCoherence(self):
        boxes, resultatsPoints = ReadAMC.updateCoherence()
        self.scoreTable = resultatsPoints.T

    def updateData(self):
        boxes, resultatsPoints = ReadAMC.updateData()
        self.scoreTable = resultatsPoints.T



    def setTable(self):
        nbIndex = len(self.scoreTable.index)
        nbColumns = len(self.scoreTable.columns)

        colName = []   # column name
        rowName = []   # row name
        self.table.setColumnCount(nbColumns)
        self.table.setRowCount(nbIndex)
        for i in range(nbIndex):
            colName.append(str(self.scoreTable.index[i]))
            for j in range(nbColumns):
                rowName.append(str(self.scoreTable.columns[j]))
                self.table.setItem(i, j, QTableWidgetItem(str(round(self.scoreTable.iloc[i, j], 2))))

        self.table.setHorizontalHeaderLabels(rowName)
        self.table.setVerticalHeaderLabels(colName)
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()

    def createBtnGroup(self):
        groupBox = QGroupBox()
        btnCoherence = QPushButton("Coherence")
        btnPDF = QPushButton("Export as PDF")
        btnCSV = QPushButton("Export as CSV")
        btnPDF.clicked.connect(self.exportPDF)
        btnCSV.clicked.connect(self.exportCSV)
        btnCoherence.clicked.connect(self.showCoherence)
        hbox = QHBoxLayout()
        hbox.addWidget(btnCoherence)
        hbox.addWidget(btnPDF)
        hbox.addWidget(btnCSV)
        hbox.addStretch(1)
        groupBox.setLayout(hbox)
        return groupBox

    def showCoherence(self):
        coherencePage = CoherencePage(self.mainWindow)
        n = coherencePage.exec_()

        if n == 1:
            self.updateDataCoherence()
            self.setTable()

    def exportPDF(self):
         print("pdf")

    def exportCSV(self):
        print("CSV")

#+--------------builder slider has been written by Arthur Lecert
class BuildSlider(QWidget):
    def __init__(self, controller, onValidate, parent=None, initialValue=1.0, arrCorrectAns=[], numberOfQuestions=1):
        super(BuildSlider, self).__init__(parent)
        self.controller = controller
        self.onValidate = onValidate
        # ---------------------weight
        self.layout = QVBoxLayout()
        self.listOfQuestions = []
        for i in range(numberOfQuestions):
            self.addSlider(QLabel("Question " + str(i+1) +"  correctness: " + str(arrCorrectAns[i]) + "  %"), QLabel(str(initialValue)), initialValue)

        self.b1 = QPushButton("Save weight")
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
        self.onValidate()
        # self.controller.updateData()
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    report = ReportPage(window)
    report.initUI(window)
    window.showMaximized()
    sys.exit(app.exec_())
