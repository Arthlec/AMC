import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QApplication, QDialog, QAction, QTableWidget, QTableWidgetItem, QWidget, \
    QMainWindow, QLabel, QVBoxLayout, QGroupBox, QPushButton, \
    QGridLayout, QHBoxLayout, QTextEdit, QComboBox, QSlider
from PyQt5.QtCore import Qt
from Project.Controller.readAMC import *
import numpy as np

class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'AMC Report'
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)

        # ---------------------table view --------------------
        '''scroll = QScrollArea()
        table = QTableWidget()
        text = QTextEdit()
        button = QPushButton()
        button = QPushButton('run coherence')
        button.clicked.connect(on_click)
        layout.addWidget(text, 0, 0)
        layout.addWidget(button, 0, 1)
        scroll.setWidget(table)
        layout.addWidget(table, 1, 0)'''
        numberOfQuestions, arrCorrectAns = getNumberOfQuestions()
        layout.addWidget(window(arrCorrectAns=arrCorrectAns,numberOfQuestions=numberOfQuestions), 1, 1)
        ''' text.move(20, 20)
        text.setFixedSize(280, 30)
        button.move(20, 80)
        table.move(20, 100)

        points, stdname = showPoint()
        df = points
        table.setColumnCount(len(df.columns))
        table.setRowCount(len(df.index))
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))'''

        self.horizontalGroupBox.setLayout(layout)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        makenewmcq = QPushButton("Make a new MCQ")
        prevmcq = QGroupBox("show previous MCQ")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(makenewmcq)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(prevmcq)
        vbox1.addStretch(800)
        vbox1.addLayout(hbox)

        self.setLayout(vbox1)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Make a new MCQ')
        self.resize(400, 400)
        self.show()


class window(QWidget):
    def __init__(self, parent=None, initialValue=1.0, arrCorrectAns=[], numberOfQuestions=1):
        super(window, self).__init__(parent)

        self.horizontalGroupBox = QGroupBox("Grid")
        self.outerL = QGridLayout()
        self.outerL.setColumnStretch(1, 4)
        self.outerL.setColumnStretch(2, 4)
        # ---------------------weight
        self.layout = QVBoxLayout()
        for i in range(numberOfQuestions):#(1, numberOfQuestions + 1):
            self.addSlider(QLabel("Question " + str(i+1) +"  correctness" + str(arrCorrectAns[i]) + "  %"), QLabel(str(initialValue)), initialValue)

        self.b1 = QPushButton("Save weight")
        self.b1.setCheckable(True)
        self.b1.toggle()
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
        slider.setMaximum(1.0)
        slider.setValue(initialValue)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(0.1)

        self.layout.addWidget(slider)
        slider.valueChanged.connect(lambda: self.valuechange(weightText, slider))

    def valuechange(self, weightText, slider):
        weightText.setText(str(slider.value()))

    def writeWeights(self):
        n = 1
        print("writeWeights 1")
        print(self.layout.count())
        for i in range(2, self.layout.count(), 3):
            # print(n)
            # print(self.layout.itemAt(i).widget().value())
            changeWeight(n, self.layout.itemAt(i).widget().value())
            n += 1
        print(getWeights())


class DoubleSlider(QSlider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.decimals = 1
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


def on_click(self):
       textboxValue = self.textbox.text()
       print(textboxValue)
       print("run coherence")


if __name__ == '__main__':


    app = QApplication(sys.argv)
    numberOfQuestions = getNumberOfQuestions()
    print(numberOfQuestions)
    #ex = window(numberOfQuestions=getNumberOfQuestions())
    #ex.show()
    ex1 = App()
    sys.exit(app.exec_())
