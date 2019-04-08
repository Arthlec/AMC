#+----------------------------------------------------+
#| 01/04/2019 - Report page for teachers
#| Created by Sahar Hosseini - Roman Blond
#| description,
#| report data as a table, chart and teachers enable to apply coherence, weight and penalty
#+----------------------------------------------------+
import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QCheckBox, QMessageBox,QFormLayout,QDialogButtonBox,QSpinBox,QHBoxLayout, QComboBox,QSlider,QGroupBox, QVBoxLayout, QGridLayout, QApplication)

from Project.Controller.logic.logic import *
from Project.Controller.readAMC import *


class lstQuestion(QWidget):
   b, c, v = computeData2()
   print(v)
   def __init__(self):
       super().__init__()
       self.currentIndex = 0
       self.lenData= len(self.v) -1
       self.initUI()

   def initUI(self):
        self.createFormGroupBox(self.currentIndex)
        self.grid = QGridLayout()
        self.grid.addWidget(self.formGroupBox,0,0)
        self.grid.addWidget(self.createBtnGroup(), 1, 0)
        self.setLayout(self.grid)
        self.setWindowTitle("Quetsion Report")
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
        print("new index")
        print(Index)
        self.formGroupBox = QGroupBox()
        layout = QFormLayout()
        row = self.v.iloc[Index]
        qNum = row[1]
        qChoices = row[2]
        lblQuestion = QLabel('Question ' + str(qNum) + ': text of question ' + str(qNum) + '?  ')

        txtCoher = QLineEdit("Coherence Formula")
        txtCoher.resize(20, 20)

        slider = QSlider(Qt.Horizontal)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(0.1)
        slider.setMinimum(0.0)
        slider.setMaximum(2.0)
        slider.setValue(1.0)
        slider.valueChanged.connect(self.addWeight)

        penalty = QSpinBox()
        chkList = []
        for i in range(qChoices):
            chkList.append(QCheckBox("Option " + str(i + 1)))

        layout.addRow(lblQuestion, txtCoher)
        layout.addRow(QLabel("Change the weight:"), slider)
        #layout.addRow(QLabel("Change Penalty:"), penalty)
        for i in range(qChoices):
            layout.addRow(chkList[i])

        self.formGroupBox.setLayout(layout)

   #-----------------------------function defination-----------------------
   def  addWeight(self):
       print("add weight")

   def clearForm(self,Index):
       self.formGroupBox.deleteLater()
       self.createFormGroupBox(Index)
       self.grid.addWidget(self.formGroupBox, 0, 0)
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
       print(len(self.v))
       if self.currentIndex == self.lenData:
           print("your are in last ")
       else:
           self.currentIndex = self.lenData
           self.clearForm(self.currentIndex)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = lstQuestion()
    sys.exit(app.exec_())
