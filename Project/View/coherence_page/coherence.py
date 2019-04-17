import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QGridLayout, QSpacerItem, QDialog, QMessageBox
from Controller.logic.logic import *
import Controller.readAMC as ReadAMC

class CoherencePage(QDialog):
    def __init__(self, parent=None):
        super(CoherencePage, self).__init__(parent)
        self.setWindowTitle('Coherence')
        self.setModal(True)

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
        for i in range(ReadAMC.getNumberOfQuestions()):
            self.createQuestionBox(i)
        self.layout.addLayout(self.sublayout)

        self.b1 = QPushButton("Compute the logic")
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
        listOfStudents = ReadAMC.getAllStudents()
        boxes, resultatsPoints = ReadAMC.updateData()

        print('Number of student: ', len(listOfStudents))
        if not self.generalCoherenceFormula.text():
            print("No formula for exam")
        else:
            # print(self.generalCoherenceFormula.text())
            try:
                logic = Logic(self.generalCoherenceFormula.text(), LogicElement.Q)
            except Exception as e:
                QMessageBox.critical(self, 'Coherence error', str(e), QMessageBox.Ok)
                return
            for i in listOfStudents:
                modifier = logic.checkResults(ReadAMC.getStudentQuestionsCorrect(i, boxes))
                listOfModifiers.append(tuple((-1, modifier)))
                listOfQuestionsText.append(self.generalCoherenceFormula.text())

            print('DONE')


        for i, coherenceFormula in enumerate(self.listOfQuestions, 1):
            # print(coherenceFormula.text())
            if not coherenceFormula.text():
                print("No formula for question " + str(i))
            else:
                try:
                    logic = Logic(coherenceFormula.text(), LogicElement.R)
                except Exception as e:
                    QMessageBox.critical(self, 'Coherence error - Question {0}'.format(i), str(e), QMessageBox.Ok)
                    return
                for j in listOfStudents:
                    modifier = logic.checkResults(ReadAMC.getStudentAnswersCorrect(j, i, boxes))
                    listOfModifiers.append(tuple((i, modifier)))
                    listOfQuestionsText.append(coherenceFormula.text())
        ReadAMC.writeCoherence([listOfModifiers, listOfQuestionsText])
        self.done(1)

    def displaySavedFormulas(self):
        formulas = ReadAMC.parseCoherenceFormula()
        if not formulas:
            return

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
