#+----------------------------------------------------+
#| 13/04/2019 - Report page for student
#| Created by Sahar Hosseini and modified by Arthur Lecert
#| description,
#| report data for each student in each question point and total point of exam +
#|correction and studet answer
#+----------------------------------------------------+

import matplotlib
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QCheckBox, QFormLayout, QHBoxLayout, QComboBox, QGroupBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas

from View.Charts import *
from View.coherence_page.coherence import *

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

class FirstQuestion(QDialog):
   def __init__(self, parent=None, boxes = None, scoreTable = None):
       super(FirstQuestion, self).__init__(parent)
       self.setModal(True)

       self.allQuestions, self.allStudents = ReadAMC.getStudentsAndQuestions()

       self.scoreTable = scoreTable
       self.lstStdName=[]

       for i in range(len(self.allStudents)):
           self.lstStdName.append(str(self.scoreTable.index[i]))

       self.currentQuestion = 1
       self.lstStdName.sort()
       for key, student in self.allStudents.items():
           if student.name == self.lstStdName[0]:
               self.currentStudent = student.id

       self.initUI()

   def initUI(self):
        self.createFormGroupBox()
        self.grid = QGridLayout()
        self.comboStdName=QComboBox()
        self.comboStdName.addItems(self.lstStdName)
        self.comboStdName.currentIndexChanged.connect(self.OnChangelstStdName)
        self.grid.addWidget(self.comboStdName, 0, 0)
        self.grid.addWidget(self.formGroupBox,1,0)

        # chart variables
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.createFigures(self.dataX, self.dataY)
        self.grid.addWidget(self.canvas,2,0)

        self.grid.addWidget(self.createBtnGroup(), 3, 0)
        self.setLayout(self.grid)
        self.setWindowTitle("Student Report")

        self.show()

   def createFigures(self,dataX,dataY):
        ax = self.figure.add_subplot(111)
        ax.cla()
        ax.scatter(dataY,dataX,color='orange')

        student = self.allStudents[self.currentStudent]
        score = self.scoreTable.iloc[:, self.currentQuestion-1].loc[student.name]

        ax.scatter(score, student.name, s=250, linewidths= 1.5, facecolors='none', edgecolors='r')

        self.canvas.draw()

   def createBtnGroup(self):
       groupBox = QGroupBox()
       btnFirst = QPushButton("<<")
       btnPre = QPushButton("<")
       btnNext = QPushButton(">")
       btnLast = QPushButton(">>")

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

   def createFormGroupBox(self):
        self.formGroupBox = QGroupBox()
        layout = QFormLayout()
        # row = self.v.iloc[Index]

        student = self.allStudents[self.currentStudent]
        question = self.allQuestions[self.currentQuestion]

        globalResult = round(self.scoreTable.loc[student.name].iloc[-1], 2)
        questionResult = round(self.scoreTable.loc[student.name, self.currentQuestion], 2)

        lblQuestion = QLabel('Question {0} : {1}'.format(self.currentQuestion, question.title))
        lblMark = QLabel("Points: {0}".format(questionResult))
        lblMark.setStyleSheet("QLabel {color : #562398; }")
        lblMark1 = QLabel("Exam Mark : {0}".format(globalResult))
        lblMark1.setStyleSheet("QLabel {color : #933333; }")

        # student answers
        lblStdAns = QLabel(student.name +" answers")
        lblStdAns.setStyleSheet("QLabel {color : #562398; }")

        # correct answers
        lblCorrectAns = QLabel("Correction")
        lblCorrectAns.setStyleSheet("QLabel {color : green; }")

        chkListStd = []
        chkListCorrect = []
        for i in range(len(question.answers)):
            chStudent = QCheckBox("Option {0}".format(i + 1))
            chCorrect = QCheckBox("Option {0}".format(i + 1))
            chStudent.setEnabled(False)
            chCorrect.setEnabled(False)
            chCorrect.setChecked(question.answers[i])
            chStudent.setChecked(student.questions[self.currentQuestion][i])
            chkListStd.append(chStudent)
            chkListCorrect.append(chCorrect)



        #data for chart
        self.dataX=self.lstStdName
        self.dataY=self.scoreTable.iloc[:, self.currentQuestion-1]

        layout.addRow(lblQuestion)
        layout.addRow(lblMark,lblMark1)

        layout.addRow(lblStdAns, lblCorrectAns)
        for i in range(len(question.answers)):
            layout.addRow(chkListStd[i], chkListCorrect[i])

        self.formGroupBox.setLayout(layout)

   #-----------------------------function defination-----------------------

   def OnChangelstStdName(self):
       studentName = self.comboStdName.currentText()
       for key, student in self.allStudents.items():
           if student.name == studentName:
               self.currentStudent = student.id

       self.clearForm()

   def clearForm(self):
       self.formGroupBox.deleteLater()
       self.createFormGroupBox()
       self.grid.addWidget(self.formGroupBox, 1, 0)
       self.createFigures(self.dataX, self.dataY)
       self.grid.addWidget(self.canvas, 2, 0)

   #-------------------------navigation ------------------------------------
   def goFirst(self):
       if self.currentQuestion != 1:
           self.currentQuestion = 1
           self.clearForm()

   def goPre(self):
       if self.currentQuestion != 1:
           self.currentQuestion -= 1
           self.clearForm()

   def goNext(self):
       if self.currentQuestion != len(self.allQuestions):
           self.currentQuestion += 1
           self.clearForm()

   def goLast(self):
       if self.currentQuestion != len(self.allQuestions):
           self.currentQuestion = len(self.allQuestions)
           self.clearForm()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = lstQuestion()
    sys.exit(app.exec_())
