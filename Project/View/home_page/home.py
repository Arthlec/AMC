
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

from Controller.readAMC import *


class _ListItem(QWidget):
    def __init__(self, name, path):
        super(_ListItem, self).__init__()
        self.name = name
        self.path = path

        titleFont = QFont()
        titleFont.setBold(True)
        titleFont.setPointSize(15)

        pathFont = QFont()
        pathFont.setPointSize(10)
        pathFont.setItalic(True)

        verticalLayout = QVBoxLayout()
        self.setLayout(verticalLayout)

        titleLabel = QLabel(self.name)
        titleLabel.setFont(titleFont)
        pathLabel = QLabel(self.path)
        pathLabel.setFont(pathFont)
        verticalLayout.addWidget(titleLabel)
        verticalLayout.addWidget(pathLabel)


class HomePage(QWidget):
    def initUI(self, mainWindow):
        mainWindow.setWindowTitle('AMC Module')

        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget(self.createTitle())
        verticalLayout.addWidget(self.createInterface())
        self.setLayout(verticalLayout)
        mainWindow.setCentralWidget(self)


    def createTitle(self):
        titleLabel = QLabel('Welcome to the MCQ correction tool')
        titleLabel.setAlignment(Qt.AlignCenter)

        titleFont = QFont()
        titleFont.setBold(True)
        titleFont.setPointSize(25)

        titleLabel.setFont(titleFont)
        return titleLabel

    def createInterface(self):
        widget = QWidget()

        grid = QGridLayout()
        widget.setLayout(grid)

        grid.addWidget(self.createNewCorrectionButton(), 1, 0, Qt.AlignCenter)
        grid.addWidget(self.createOldCorrectionsList(), 1, 1)

        for i in range(2):
            grid.setColumnStretch(i, 1)
            grid.setRowStretch(i, 1)

        return widget

    def createNewCorrectionButton(self):
        button = QPushButton('New correction')
        button.setStyleSheet("""
            QPushButton {
                    width: 30px
                    height: 100px
            }

        """)

        return button


    def createOldCorrectionsList(self):
        fakeList = [
            ['Exam8', 'C:/User/user/AMC/exam8'],
            ['Exam7', 'C:/User/user/AMC/exam7'],
            ['Exam6', 'C:/User/user/AMC/exam6'],
            ['Exam5', 'C:/User/user/AMC/exam5'],
            ['Exam4', 'C:/User/user/AMC/exam4'],
            ['Exam3', 'C:/User/user/AMC/exam3'],
            ['Exam2', 'C:/User/user/AMC/exam2'],
            ['Exam1', 'C:/User/user/AMC/exam1'],
        ]

        widget = QWidget()
        verticalLayout = QVBoxLayout()
        widget.setLayout(verticalLayout)
        for item in fakeList:
            verticalLayout.addWidget(_ListItem(item[0], item[1]))

        scrollArea = QScrollArea()
        scrollArea.setWidget(widget)

        return scrollArea



class App(QWidget):

    def __init__(self, parent=None):
        super(App, super).__init__(parent)
        self.title = 'AMC Result'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
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

        #---------------------table view --------------------
        scroll = QScrollArea()
        table = QTableWidget()
        text = QTextEdit()
        button = QPushButton()
        button = QPushButton('run coherence')
        button.clicked.connect(on_click)
        layout.addWidget(text, 0, 0)
        layout.addWidget(button, 0, 1)
        scroll.setWidget(table)
        layout.addWidget(table, 1, 0)
        layout.addWidget(window(numberOfQuestions=getNumberOfQuestions()), 1, 1)
        text.move(20, 20)
        text.setFixedSize(280, 30)
        button.move(20, 80)
        table.move(20, 100)

        std, points, stdname = showPoint()
        df = points
        table.setColumnCount(len(df.columns))
        table.setRowCount(len(df.index))
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))


        self.horizontalGroupBox.setLayout(layout)


class Example(QWidget):
    def __init__(self, parent=None):
        super(Example, self).__init__(parent)

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
    w = QMainWindow()
    w.showMaximized()
    sys.exit(app.exec_())
