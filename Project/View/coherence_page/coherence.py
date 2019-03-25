import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QGridLayout, QSpacerItem
from Controller.logic.logic import *
from Controller.readAMC import getNumberOfQuestions

class CoherencePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Coherence')
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)

        title = QLabel("Please Enter your Coherence Formula for the exam")
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        self.coherenceFormula = QLineEdit("")
        self.coherenceFormula.resize(40, 40)
        self.layout.addWidget(self.coherenceFormula)

        self.sublayout = QGridLayout()
        self.sublayout.setColumnStretch(1, 2)
        self.sublayout.setSpacing(20)
        # self.sublayout.setColumnStretch(2, 4)
        # self.sublayout.addItem(QSpacerItem(0, 0))
        # self.sublayout.addItem(QSpacerItem(0, 0))
        for i in range(getNumberOfQuestions()[0]):
            self.createQuestionBox(i)
        self.layout.addLayout(self.sublayout)

        self.b1 = QPushButton("Compute the logic")
        self.b1.setCheckable(True)
        self.b1.toggle()
        self.b1.clicked.connect(self.computeLogic)
        self.layout.addWidget(self.b1)

        self.setLayout(self.layout)
        self.show()

    def createQuestionBox(self, i):
        title = QLabel("Question " + str(i + 1))
        title.setAlignment(Qt.AlignCenter)
        self.sublayout.addWidget(title)
        coherenceFormula = QLineEdit("")
        coherenceFormula.resize(20, 20)
        self.sublayout.addWidget(coherenceFormula)

    def computeLogic(self):
        print(self.coherenceFormula.text())
        logic = Logic(self.coherenceFormula.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex1 = CoherencePage()
    sys.exit(app.exec_())
