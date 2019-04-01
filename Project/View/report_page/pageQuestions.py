#+----------------------------------------------------+
#| 01/04/2019 - Report page for teachers
#| Created by Sahar Hosseini - Roman Blond
#| description,
#| report data as a table, chart and teachers enable to apply coherence, weight and penalty
#+----------------------------------------------------+
import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QCheckBox, QMessageBox, QComboBox,QSlider,QGroupBox, QVBoxLayout, QGridLayout, QApplication)

from Project.Controller.logic.logic import *
from Project.Controller.readAMC import *

#+--------------main class
class lstQuestion(QWidget):
    b, c, v = computeData2()
    print(b)  # include questions and number of choices
    print(c)
    print(v)  # use this one

    def __init__(self):
        super().__init__()
        self.title = 'AMC Question Report'
        self.left = 30
        self.top = 30
        self.width = 600
        self.height = 400
        self.currentIndex = 0
        self.initUI()

    def initUI(self):
        print("---------initUI---------")
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        btnFirst = QPushButton("First")
        btnPre = QPushButton("Previous")
        btnNext = QPushButton("Next")
        btnLast = QPushButton("Last")
        btnFirst.clicked.connect(self.goFirst)
        btnPre.clicked.connect(self.goPre)
        btnNext.clicked.connect(self.goNext)
        btnLast.clicked.connect(self.goLast)


        self.createQuestionView(self.currentIndex)
        self.windowLayout = QGridLayout()
        self.windowLayout.addWidget(self.horizontalGroupBox,0,0)
        self.windowLayout.addWidget(btnFirst,  1, 0)
        self.windowLayout.addWidget(btnPre, 1, 1)
        self.windowLayout.addWidget(btnNext, 1, 2)
        self.windowLayout.addWidget(btnLast,  1, 3)
        self.setLayout(self.windowLayout)
        self.show()
    def createQuestionView(self,Index):
        print("Index")
        print(Index)
        self.horizontalGroupBox = QGroupBox("AMC report for teachers")

        # ---------------------grid layout --------------------
        self.layout = QGridLayout()
        self.layout.setColumnStretch(0, 3)
        self.layout.setColumnStretch(1, 3)
        self.layout.setColumnStretch(2, 3)
        #main part
        # ---------------questions label
        row = self.v.iloc[Index]
        qNum = row[1]
        qChoices = row[2]
        print(row)
        print(qNum)
        self.lblQuestion = QLabel('Question ' + str(qNum) + ': How new marking module works?  ')
        self.lblQuestion1 = QLabel('!!!!show correctness of perecentage of this question %%% or chart ')

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(20)

        self.slider.setSingleStep(1)

        self.txtCoher = QLineEdit("Coherence Formula")
        self.txtCoher.resize(20, 20)
        # ---------------question choices
        self.chkList = []

        for i in range(qChoices):
            self.chkList.append(QCheckBox("Option " + str(i + 1)))

        self.layout.addWidget(self.lblQuestion, 0, 0)
        #layout.addWidget(self.lblQuestion1, 1, 2)
        self.layout.addWidget(self.slider, 1, 1)
        self.layout.addWidget(self.txtCoher, 0, 1)
        for i in range(qChoices):
            self.layout.addWidget(self.chkList[i], i + 1, 0)


        self.horizontalGroupBox.setLayout(self.layout)
    def goFirst(self):
         if self.currentIndex==0:
             print("your are in first ")
         else:
             self.currentIndex=0

         self.initUI()

    def goPre(self):
         print("")

    def goNext(self):
        print("next1")
        if self.currentIndex == len(self.v):
            print("next2")
            print("your are in last ")
        else:
            print("next3")
            self.currentIndex = self.currentIndex +1
            print(" self current index value next4")
        print(self.currentIndex)
        print("next5")
        self.createQuestionView(self.currentIndex)
        #self.initUI()

    def goLast(self):
        print("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = lstQuestion()
    sys.exit(app.exec_())