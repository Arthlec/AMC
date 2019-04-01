#+----------------------------------------------------+
#| 01/04/2019 - Report page for teachers
#| Created by Sahar Hosseini - Roman Blond
#| description,
#| report data as a table, chart and teachers enable to apply coherence, weight and penalty
#+----------------------------------------------------+
import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QCheckBox, QMessageBox, QComboBox,QSlider,  QGridLayout, QApplication)

#+--------------main class
class lstQuestion(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'AMC Question Report'
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #---------------questions label
        self.lblQuestion = QLabel('Question1: How new marking module works?  ')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(20)

        self.slider.setSingleStep(1)

        self.txtCoher = QLineEdit("Coherence Formula")
        self.txtCoher.resize(20, 20)
        #---------------question choices
        ''' self.listCheckBox = ["Checkbox_1", "Checkbox_2", "Checkbox_3", "Checkbox_4", "Checkbox_5",
                      "Checkbox_6", "Checkbox_7", "Checkbox_8", "Checkbox_9", "Checkbox_10"]
 self.listLabel = ['', '', '', '', '', '', '', '', '', '', ]
 grid = QGridLayout()

 for i, v in enumerate(self.listCheckBox):
     self.listCheckBox[i] = QCheckBox(v)
     self.listLabel[i] = QLabel()
     grid.addWidget(self.listCheckBox[i], i, 0)
     grid.addWidget(self.listLabel[i], i, 1)'''

        self.chAuto1 = QCheckBox("Good quality")
        self.chAuto2 = QCheckBox("Poor quality")
        self.chAuto3 = QCheckBox("Avarage")
        self.chAuto4 = QCheckBox("No idea")

        #---------------navigation buttons

        btnFirst = QPushButton("First")
        btnPre = QPushButton("Previous")
        btnNext = QPushButton("Next")
        btnLast = QPushButton("Last")
        btnFirst.clicked.connect(self.goFirst)
        btnPre.clicked.connect(self.goPre)
        btnNext.clicked.connect(self.goNext)
        btnLast.clicked.connect(self.goLast)

        #---------------main grid

        grid = QGridLayout()
        grid.setSpacing(5)

        grid.addWidget(self.lblQuestion, 0, 0)
        grid.addWidget(self.slider, 0, 1)
        grid.addWidget(self.txtCoher, 0, 2)
        grid.addWidget(self.chAuto1, 1, 0)
        grid.addWidget(self.chAuto2, 2, 0)
        grid.addWidget(self.chAuto3, 3, 0)
        grid.addWidget(self.chAuto4, 4, 0)

        grid.addWidget(btnFirst, 5, 0)
        grid.addWidget(btnPre, 5, 1)
        grid.addWidget(btnNext, 5, 2)
        grid.addWidget(btnLast, 5, 3)
        # -------------call layout
        self.setLayout(grid)
        self.show()
    def goFirst(self):
         print("")
    def goPre(self):
         print("")

    def goNext(self):
        print("")

    def goLast(self):
        print("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = lstQuestion()
    sys.exit(app.exec_())