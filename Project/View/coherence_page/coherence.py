import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QGridLayout, QSpacerItem
from Controller.logic.logic import *
from Controller.readAMC import getNumberOfQuestions, getAllStudents, getStudentAnswersCorrect, writeCoherence, \
    getStudentQuestionsCorrect, parseCoherenceFormula

class CoherencePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Coherence')
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.listOfQuestions = []

        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)

        title = QLabel("Please enter your coherence formulas for the exam and the questions")
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        self.generalCoherenceFormula = QLineEdit("")
        self.generalCoherenceFormula.resize(40, 40)
        self.layout.addWidget(self.generalCoherenceFormula)

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

        self.displaySavedFormulas()

        self.setLayout(self.layout)
        self.show()

    def createQuestionBox(self, i):
        title = QLabel("Question " + str(i + 1))
        title.setAlignment(Qt.AlignCenter)
        self.sublayout.addWidget(title)
        coherenceFormula = QLineEdit("")
        coherenceFormula.resize(20, 20)
        self.sublayout.addWidget(coherenceFormula)

        self.listOfQuestions.append(coherenceFormula)

    def computeLogic(self):
        listOfModifiers = []
        listOfQuestionsText = []
        listOfStudents = getAllStudents()
        if not self.generalCoherenceFormula.text():
            print("No formula for exam")
        else:
            # print(self.generalCoherenceFormula.text())
            logic = Logic(self.generalCoherenceFormula.text(), LogicElement.Q)
            for i in listOfStudents:
                modifier = logic.checkResults(getStudentQuestionsCorrect(i))
                listOfModifiers.append(tuple((-1, modifier)))
                listOfQuestionsText.append(self.generalCoherenceFormula.text())
        for i, coherenceFormula in enumerate(self.listOfQuestions, 1):
            # print(coherenceFormula.text())
            if not coherenceFormula.text():
                print("No formula for question " + str(i))
            else:
                for j in listOfStudents:
                    logic = Logic(coherenceFormula.text(), LogicElement.R)
                    modifier = logic.checkResults(getStudentAnswersCorrect(j, i))
                    listOfModifiers.append(tuple((i, modifier)))
                    listOfQuestionsText.append(coherenceFormula.text())
        writeCoherence([listOfModifiers, listOfQuestionsText])

    def displaySavedFormulas(self):
        formulas = parseCoherenceFormula()
        if formulas[0][0][0] == -1: # [Modifiers][Tuple][Index]
            self.generalCoherenceFormula.setText(formulas[1][0]) # [Text][Index]
        for i in range(1, len(self.listOfQuestions)):
            for j in range(len(formulas[0])):
                if formulas[0][j][0] == i:
                    self.listOfQuestions[i-1].setText(formulas[1][j])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex1 = CoherencePage()
    sys.exit(app.exec_())
