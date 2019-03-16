import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QGroupBox, QPushButton, \
    QGridLayout, QHBoxLayout, QTextEdit, QComboBox, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from Project.Controller.readAMC import *

'''
class ViewHome(QWidget):
    def __init__(self, parent=None):
        # def __init__(self):
        super(ViewHome, self).__init__()
        self.initUI()

    def initUI(self):
        # title = self.makeTitle()
        newmcq = self.MakeNewMCQ()
        # prevmcq = self.makePreviousMCQ()
        layout = QVBoxLayout()
        # layout.addWidget(title)
        layout.addWidget(newmcq)
        # layout.addWidget(prevmcq)
        self.setLayout(layout)
        self.show()
        return newmcq

    def MakeNewMCQ(self):
        # Generate a report for a new mcq
        # wid1 = QGroupBox(title='Import a new MCQ')
        wid1 = QWidget()
        button = QPushButton('Import a new MCQ to create a report')
        layout1 = QHBoxLayout()
        layout1.addWidget(button)
        wid1.setLayout(layout1)
        return button

        # Content
        layout = QHBoxLayout()
        layout.addwidget(wid1, 0, 0)
        content = QWidget()
        content.setLayout(layout)
        return content


    def makeTitle(self):
        titleFont = QFont()
        titleFont.setBold(True)
        titleFont.setPointSize(20)
        title = QLabel('Bienvenue dans l\'outil de correction de QCM')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(titleFont)
        return title


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    view = ViewHome(window)
    window.setCentralWidget(view)
    window.setGeometry(700, 300, 1800, 1400)
    window.show()
    sys.exit(app.exec_())
'''


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
    def __init__(self, parent=None, initialValue=1.0):
        super(window, self).__init__(parent)

        layout = QVBoxLayout()
        self.title = QLabel("Poids des questions")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        self.createSlider(layout, initialValue)

        self.weight = QLabel(str(initialValue))
        self.weight.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.weight)

        self.b1 = QPushButton("Save weight")
        self.b1.setCheckable(True)
        self.b1.toggle()
        self.b1.clicked.connect(self.writeWeights)
        layout.addWidget(self.b1)

        self.setLayout(layout)
        self.setWindowTitle("Module AMC")

    def valuechange(self):
        self.weight.setText(str(self.sl.value()))

    def createSlider(self, layout,initialValue):
        self.sl = DoubleSlider(Qt.Horizontal)
        self.sl.setMinimum(0.0)
        self.sl.setMaximum(1.0)
        self.sl.setValue(initialValue)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(0.1)

        layout.addWidget(self.sl)
        self.sl.valueChanged.connect(self.valuechange)

    def writeWeights(self):
        changeWeight(self.sl.value())

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = window(initialValue=computeData())
    ex.show()
    sys.exit(app.exec_())