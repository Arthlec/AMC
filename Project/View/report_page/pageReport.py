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
from PyQt5.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# from Controller.readAMC import getNumberOfQuestions, changeWeight
from Controller.readAMC import *
from View.Charts import PlotCanvas
from Controller.studentData import StudentData
from View.coherence_page.coherence import *
from View.setting_page.pageSetting import Settings
from View.report_page.pageStudents import FirstQuestion
from Controller.pdfExport import PDFExport

#+--------------main class
class ReportPage(QWidget):
    DEFAULT_CHART_INDEX = 3

    def __init__(self, parent=None):
        super(ReportPage, self).__init__(parent)
        self.controller = StudentData()
        self.plot = PlotCanvas(self.controller)

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

        # ---------------------Mean and STD  --------------------
        horizLayout = QHBoxLayout()
        row = QWidget(self.horizontalGroupBox)
        self.meanLabel = QLabel()
        self.stdLabel = QLabel()

        horizLayout.addWidget(self.meanLabel)
        horizLayout.addWidget(self.stdLabel)
        row.setLayout(horizLayout)

        layout.addWidget(row, 0, 1)

        # ---------------------Font of Mean and STD  --------------------
        meanFont = QFont()
        meanFont.setBold(True)
        meanFont.setPointSize(13.0)
        self.meanLabel.setStyleSheet('QLabel {color: #128700;}')
        self.stdLabel.setStyleSheet('QLabel {color: #4a006b;}')

        self.meanLabel.setFont(meanFont)
        self.stdLabel.setFont(meanFont)

        # ---------------------text boxes  --------------------
        # Put all of the choices together, linking the name and the function to call
        self.comboOptions = [
            ["Box Chart",     self.plot.plot_box],
            ["Violin Chart",  self.plot.plot_violin],
            ["Line Chart",    self.plot.plot_line],
            ["Pie Chart",     self.plot.plot_pie],
        ]

        self.cbChart = QComboBox()
        for elt in self.comboOptions:
            self.cbChart.addItem(elt[0])
        self.cbChart.setCurrentIndex(self.DEFAULT_CHART_INDEX)
        self.cbChart.resize(140, 30)
        layout.addWidget(self.cbChart, 0, 2)
        layout.addWidget(self.createBtnGroup(), 0, 0)
        self.cbChart.currentIndexChanged.connect(self.OnChangeCbChart)

        # ---------------------table view --------------------
        # scroll = QScrollArea()
        self.table = QTableWidget()
        # scroll.setWidget(table)
        layout.addWidget(self.table, 1, 0)

        self.initData()
        self.setTable()
        self.computeMeanAndSTD()


        # ---------------------slider  weight --------------------
        numberOfQuestions = self.getNumberOfQuestions()
        arrCorrectAns = self.getPercentage()
        print("arrCorrectAns : ", len(arrCorrectAns))
        print(arrCorrectAns)
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(BuildSlider(self.refreshInterface, arrCorrectAns=arrCorrectAns,numberOfQuestions=numberOfQuestions))
        layout.addWidget(scrollArea, 1, 1)

        # ---------------------chart view --------------------
        self.plot.plot_pie()
        self.selectedChart = self.DEFAULT_CHART_INDEX
        layout.addWidget(self.plot, 1, 2)

        self.horizontalGroupBox.setLayout(layout)

    def getNumberOfQuestions(self):
        listQuestions = self.boxes['question'].unique()
        numberOfQuestions = len(listQuestions)

        return numberOfQuestions

    def getPercentage(self):
        listStudents = self.boxes['student'].unique()
        numberOfStudents = len(listStudents)

        correctAns = []
        for i in range(len(self.scoreTable.columns)):
            numberOfOnes = 0
            for j in range(len(self.scoreTable.index)):
                if self.scoreTable.iloc[j, i] == 1:
                    numberOfOnes += 1
            correctAns.append(round((numberOfOnes / numberOfStudents) * 100, 0))
        return correctAns

    def computeMeanAndSTD(self):
        mean = self.scoreTable.iloc[:,-1].mean()
        std = self.scoreTable.iloc[:,-1].std()

        self.meanLabel.setText('Mean: {0}'.format(round(mean,2)))
        self.stdLabel.setText('STD: {0}'.format(round(std,2)))


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


    # Calls directly the good function in the array self.comboOptions
    def OnChangeCbChart(self,i):
        self.comboOptions[i][1]()
        self.selectedChart = i


    def initData(self):
        boxes, resultatsPoints = ReadAMC.computeData()
        self.scoreTable = resultatsPoints.T
        self.boxes = boxes

    def updateData(self):
        boxes, resultatsPoints = ReadAMC.updateData()
        self.scoreTable = resultatsPoints.T
        self.boxes = boxes


    def setTable(self):
        self.sortTable()
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

    def refreshInterface(self):
        self.updateData()
        self.setTable()
        self.plot.refresh()
        self.comboOptions[self.selectedChart][1]()
        self.computeMeanAndSTD()

    def createBtnGroup(self):
        groupBox = QGroupBox()
        btnHome = QPushButton("Home")
        btnCoherence = QPushButton("Coherence")
        btnSettings = QPushButton("Settings")
        btnPDF = QPushButton("Export as Markdown")
        btnCSV = QPushButton("Export as CSV")
        btnStudent = QPushButton("Student report")
        btnHome.clicked.connect(self.showHome)
        btnCoherence.clicked.connect(self.showCoherence)
        btnSettings.clicked.connect(self.showSettings)
        btnPDF.clicked.connect(self.exportPDF)
        btnCSV.clicked.connect(self.exportCSV)
        btnStudent.clicked.connect(self.showStudentReport)
        hbox = QHBoxLayout()
        hbox.addWidget(btnHome)
        hbox.addWidget(btnCoherence)
        hbox.addWidget(btnSettings)
        hbox.addWidget(btnPDF)
        hbox.addWidget(btnCSV)
        hbox.addWidget(btnStudent)
        hbox.addStretch(1)
        groupBox.setLayout(hbox)
        return groupBox

    def showHome(self):
        # Do not move this import, or the program crashes
        from View.home_page.home import HomePage
        home = HomePage(self.mainWindow)
        home.initUI(self.mainWindow)

    def showStudentReport(self):
        studentDialog = FirstQuestion(self.mainWindow)
        studentDialog.exec_()

    def showCoherence(self):
        coherencePage = CoherencePage(self.mainWindow)
        n = coherencePage.exec_()

        if n == 1:
            self.refreshInterface()

    def showSettings(self):
        settingsPage = Settings(self.mainWindow, fetchData=True)
        n = settingsPage.exec_()

        if n == 1:
            self.refreshInterface()

    def exportPDF(self):
         pdfExport = PDFExport()

    def exportCSV(self):
        print("CSV")

#+--------------builder slider has been written by Arthur Lecert
class BuildSlider(QWidget):
    def __init__(self, onValidate, parent=None, initialValue=1.0, arrCorrectAns=[], numberOfQuestions=1):
        super(BuildSlider, self).__init__(parent)
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
