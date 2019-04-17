#+----------------------------------------------------+
#| 13/04/2019 - Report page for student
#| Created by Sahar Hosseini and modified by Arthur Lecert
#| description,
#| report data for each student in each question point and total point of exam +
#|correction and studet answer
#+----------------------------------------------------+
import math

import matplotlib
import sys

import pandas as pd
from PyQt5.QtCore import  Qt
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QCheckBox, QMessageBox,QFormLayout,QDialogButtonBox,QSpinBox,QHBoxLayout, QComboBox,QSlider,QGroupBox, QVBoxLayout, QGridLayout, QApplication)
from scipy.stats import stats
import seaborn as sns, numpy as np
import Controller.readAMC as ReadAMC
from Controller.studentData import StudentData
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
   def __init__(self, parent=None, boxes = None):
       super(FirstQuestion, self).__init__(parent)
       self.setModal(True)

       self.controller = StudentData()
       self.scoreTable = self.controller.getScoreTable()  # main datalist
       self.lstStdName=[]

       listStudents = boxes['student'].unique()
       b = boxes.groupby(['student'])['question'].value_counts().to_frame('count').sort_values("question")
       print(b)
       c = pd.DataFrame(b).reset_index()
       self.v = c.loc[c['student'] == listStudents[0]]

       # b, c, self.v = ReadAMC.computeData2()

       self.zone, self.answer, self.studentNames, self.var ,self.questionTitles= ReadAMC.readAMCTables(ReadAMC.dataPath)
       self.boxes = boxes# ReadAMC.makeBoxes(self.zone, self.answer, self.var )
       # print("boxes: ", self.boxes)
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
       self.lstQstAns2=self.boxes[self.boxes['student']==self.stdID[0]]
       self.initUI()

   def initUI(self):
        self.createFormGroupBox(self.currentIndex)
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
       print(dataY)
       ax.scatter(dataY,dataX,color='orange')
       #ax.plot(dataY, dataX,color='green')
       #ax.boxplot(dataY)
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

   def createFormGroupBox(self, Index):
        self.formGroupBox = QGroupBox()
        layout = QFormLayout()
        row = self.v.iloc[Index]
        qNum = row[1]
        qChoices = row[2]
        self.std = self.scoreTable.loc[self.stdTitle, :]
        self.stdMark1 =   self.scoreTable.iloc[0, qNum]#self.std.iloc[Index]
        self.stdMark2 = self.std.iloc[-3]
        self.stdMark3 = self.std.iloc[-1]
        questionTitle=self.questionTitles[self.questionTitles['question']==qNum].title.reset_index(drop=True)
        lblQuestion = QLabel('Question ' + str(qNum) +  ':  '+ questionTitle[0].encode('latin-1').decode('utf-8'))
        lblMark = QLabel(self.stdTitle +"  point: "+str(round(self.stdMark1,2)))
        lblMark.setStyleSheet("QLabel {color : #562398; }")
        lblMark1 = QLabel("Exam Mark for "+ self.stdTitle +": " + str(round(self.stdMark3,1)))
        lblMark1.setStyleSheet("QLabel {color : #933333; }")


        # student answers
        lblStdAns = QLabel( self.stdTitle +" Answer")
        lblStdAns.setStyleSheet("QLabel {color : #562398; }")

        lstStdAns=self.lstQstAns2[self.lstQstAns2['question']==qNum].ticked.reset_index(drop=True)

        chkListStd = []
        for i in range(qChoices):
            ch=QCheckBox("Option " + str(i + 1))
            ch.setEnabled(False)
            if (lstStdAns[i] ==True ):
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



        #data for chart
        # self.dataX=[]
        self.dataX=self.lstStdName
        # self.dataY=[]
        self.dataY=self.scoreTable.iloc[:, qNum]

        layout.addRow(lblQuestion)
        layout.addRow(lblMark,lblMark1)

        layout.addRow(lblStdAns, lblCorrectAns)
        for i in range(qChoices):
            layout.addRow(chkListStd[i],chkListCorrect[i])

        self.formGroupBox.setLayout(layout)

   #-----------------------------function defination-----------------------

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
       self.createFigures(self.dataX, self.dataY)
       self.grid.addWidget(self.canvas, 2, 0)
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
