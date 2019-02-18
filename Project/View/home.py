import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QGroupBox, QPushButton, \
    QGridLayout, QHBoxLayout, QTextEdit, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())