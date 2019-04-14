#+----------------------------------------------------+
#| 13/04/2019 - Report page for student
#| Created by Sahar Hosseini
#| description,
#| report data for each student in each question point and total point of exam +
#|correction and studet answer
#+----------------------------------------------------+
import matplotlib
import sys

from PyQt5.QtCore import  Qt
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QCheckBox, QMessageBox,QFormLayout,QDialogButtonBox,QSpinBox,QHBoxLayout, QComboBox,QSlider,QGroupBox, QVBoxLayout, QGridLayout, QApplication)

from Project.Controller.readAMC import *
from Project.Controller.studentData import StudentData

dataPathAnswers = str(Path(__file__).resolve().parent.parent).replace("\\", "/") + "/../Real Data/"

# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')

# Matplotlib canvas class to create figure
class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

# Matplotlib widget
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = MplCanvas()                  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

class lstQuestion(QWidget):


   def __init__(self):
       super().__init__()
       self.controller = StudentData()
       self.scoreTable = self.controller.getScoreTable()  # main datalist
       self.lstStdName=[]
       b, c, self.v = computeData2()

       _, self.answer, self.studentNames, _ = readAMCTables(dataPathAnswers)
       nbIndex = len(self.scoreTable.index)
       self.currentIndex = 0
       self.lenData= len(self.v) -1
       self.stdMark1=0
       self.stdMark2 = 0
       self.stdMark3 = 0
       self.stdTitle=""
       for i in range(nbIndex):
           self.lstStdName.append(str(self.scoreTable.index[i]))

       self.stdTitle=self.lstStdName[0]
       self.stdID =[]
       self.stdID=self.studentNames[self.studentNames['manual'] == self.stdTitle].student
       self.lstQstAns=self.answer[self.answer['student'] == self.stdID[0]]
       self.initUI()
   def initUI(self):
        self.createFormGroupBox(self.currentIndex)
        self.grid = QGridLayout()
        self.comboStdName=QComboBox()
        self.comboStdName.addItems(self.lstStdName)
        self.comboStdName.currentIndexChanged.connect(self.OnChangelstStdName)
        self.grid.addWidget(self.comboStdName, 0, 0)
        self.grid.addWidget(self.formGroupBox,1,0)
        self.grid.addWidget(self.createBtnGroup(), 2, 0)
        self.setLayout(self.grid)
        self.setWindowTitle("Student Report")
        self.show()

   def createBtnGroup(self):
       groupBox = QGroupBox()
       btnFirst = QPushButton("First")
       btnPre = QPushButton("Previous")
       btnNext = QPushButton("Next")
       btnLast = QPushButton("Last")

       btnFirst.clicked.connect(self.goFirst)
       btnPre.clicked.connect(self.goPre)
       btnNext.clicked.connect(self.goNext)
       btnLast.clicked.connect(self.goLast)
       hbox = QHBoxLayout()
       hbox.addWidget(btnFirst)
       hbox.addWidget(btnPre)
       hbox.addWidget(btnNext)
       hbox.addWidget(btnLast)
       hbox.addStretch(1)
       groupBox.setLayout(hbox)
       return groupBox

   def createFormGroupBox(self, Index):
        self.formGroupBox = QGroupBox()
        layout = QFormLayout()
        row = self.v.iloc[Index]
        qNum = row[1]
        qChoices = row[2]
        self.std = self.scoreTable.loc[self.stdTitle, :]
        self.stdMark1 = self.std.iloc[Index]
        self.stdMark2 = self.std.iloc[-3]
        self.stdMark3 = self.std.iloc[-1]
        lblQuestion = QLabel('Question ' + str(qNum) +  '?  ')
        lblMark = QLabel( self.stdTitle +"  point: "+str(round(self.stdMark1,1)))
        lblMark.setStyleSheet("QLabel {color : #562398; }")
        lblMark1 = QLabel("Exam Mark for "+ self.stdTitle +": " + str(round(self.stdMark3,1)))
        lblMark1.setStyleSheet("QLabel {color : #933333; }")


        # student answers
        lblStdAns = QLabel( self.stdTitle +" Answer")
        lblStdAns.setStyleSheet("QLabel {color : #562398; }")
        lstStdAns = self.lstQstAns[self.lstQstAns['question'] == qNum].answer.reset_index(drop=True)
        chkListStd = []
        for i in range(qChoices):
            ch=QCheckBox("Option " + str(i + 1))
            ch.setEnabled(False)
            if (lstStdAns[i] > 0 ):
               ch.setChecked(True)
            chkListStd.append(ch)

        # correct answers
        lblCorrectAns = QLabel("Correction")
        lblCorrectAns.setStyleSheet("QLabel {color : green; }")
        lstCorrectAns = self.lstQstAns[self.lstQstAns['question'] == qNum].correct.reset_index(drop=True)
        chkListCorrect = []
        for i in range(qChoices):
            ch=QCheckBox("Option " + str(i + 1))
            ch.setEnabled(False)
            if (lstCorrectAns[i] == 1):
               ch.setChecked(True)
            chkListCorrect.append(ch)

        layout.addRow(lblQuestion,lblMark1)
        layout.addRow("",lblMark)

        #layout.addRow(self.plot_data)
        layout.addRow(lblStdAns, lblCorrectAns)
        for i in range(qChoices):
            layout.addRow(chkListStd[i],chkListCorrect[i])

        self.formGroupBox.setLayout(layout)

   #-----------------------------function defination-----------------------
   def plot_data(self):
       x = range(0, 10)
       y = range(0, 20, 2)
       self.plotWidget.canvas.ax.plot(x, y)
       self.plotWidget.canvas.draw()

   def OnChangelstStdName(self, i):
       self.stdTitle = self.comboStdName.currentText()
       self.stdID = self.studentNames[self.studentNames['manual'] == self.stdTitle].student.reset_index(drop=True)
       self.lstQstAns = self.answer[self.answer['student'] == self.stdID[0]]
       self.currentIndex = 0
       self.clearForm(self.currentIndex)

   def clearForm(self,Index):
       self.formGroupBox.deleteLater()
       self.createFormGroupBox(Index)
       self.grid.addWidget(self.formGroupBox, 1, 0)
   #-------------------------navigation ------------------------------------
   def goFirst(self):
       if self.currentIndex == 0:
           print("your are in first ")
       else:
           self.currentIndex = 0
           self.clearForm(self.currentIndex)

   def goPre(self):
       if self.currentIndex == 0:
           print("your are in first ")
       else:
           self.currentIndex = self.currentIndex - 1
           self.clearForm(self.currentIndex)

   def goNext(self):
       if self.currentIndex == self.lenData:
           print("your are in last ")
       else:
           self.currentIndex = self.currentIndex + 1
           self.clearForm(self.currentIndex)

   def goLast(self):
       if self.currentIndex == self.lenData:
           print("your are in last ")
       else:
           self.currentIndex = self.lenData
           self.clearForm(self.currentIndex)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = lstQuestion()
    sys.exit(app.exec_())
