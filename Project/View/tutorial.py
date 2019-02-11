# https://build-system.fman.io/pyqt5-tutorial

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class App(QWidget):
    def __init__(self, changeStyleCallback):
        super(App, self).__init__()
        self.changeStyleCallback = changeStyleCallback
        self.initUI()


    def initUI(self):
        self.title = 'Hello World'
        header = self.makeHeader()
        content = self.makeContent()
        layout = QVBoxLayout()
        layout.addWidget(header)
        layout.addWidget(content)
        self.setLayout(layout)
        self.show()


    def makeHeader(self):
        # Widget 1
        wid1 = QWidget()
        label1 = QLabel('Style:')
        combo1 = QComboBox()
        combo1.addItems(['Fusion', 'Windows', 'WindowsVista', 'Macintosh'])
        combo1.currentTextChanged.connect(self.changeStyleCallback)
        layout1 = QHBoxLayout()
        layout1.addWidget(label1)
        layout1.addWidget(combo1)
        wid1.setLayout(layout1)

        # Widget 2
        wid2 = QWidget()
        check2 = QCheckBox()
        label2 = QLabel('Use style\'s standard palette')
        layout2 = QHBoxLayout()
        layout2.addWidget(check2)
        layout2.addWidget(label2)
        wid2.setLayout(layout2)

        # Widget 3
        wid3 = QWidget()
        check3 = QCheckBox()
        label3 = QLabel('Disable widgets')
        layout3 = QHBoxLayout()
        layout3.addWidget(check3)
        layout3.addWidget(label3)
        wid3.setLayout(layout3)


        # Header
        layout = QHBoxLayout()
        layout.addWidget(wid1)
        layout.addWidget(wid2)
        layout.addWidget(wid3)
        header = QWidget()
        header.setLayout(layout)
        return header


    def makeContent(self):
        # Group 1
        wid1 = QGroupBox(title='Group 1')
        layout1 = QVBoxLayout()
        for i in range(1,4):
            layout1.addWidget(QRadioButton('Radio Button ' + str(i)))
        checkbox1 = QCheckBox('Tri-state checkbox')
        checkbox1.setTristate(True)
        layout1.addWidget(checkbox1)
        wid1.setLayout(layout1)

        # Group 2
        wid2 = QGroupBox(title='Group 2')
        layout2 = QVBoxLayout()
        button21 = QPushButton('Default Push Button')
        button22 = QPushButton('Flat Push Button')
        button22.setFlat(True)
        layout2.addWidget(button21)
        layout2.addWidget(button22)
        wid2.setLayout(layout2)

        # Group 3
        wid3 = QGroupBox(title='Group 3')
        wid3.setCheckable(True)
        layout3 = QVBoxLayout()
        line3 = QLineEdit()
        line3.setEchoMode(QLineEdit.Password)
        counter3 = QSpinBox()
        wid31 = QWidget()
        layout31 = QGridLayout()
        layout31.addWidget(QSlider(Qt.Horizontal), 0, 0)
        wid31.setLayout(layout31)

        layout3.addWidget(line3)
        layout3.addWidget(counter3)
        layout3.addWidget(wid31)
        wid3.setLayout(layout3)


        # Content
        layout = QGridLayout()
        layout.addWidget(wid1, 0, 0)
        layout.addWidget(wid2, 0, 1)
        layout.addWidget(wid3, 1, 1)
        content = QWidget()
        content.setLayout(layout)
        return content



def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    test = App(changeStyleCallback=lambda newStyle : app.setStyle(newStyle))
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
