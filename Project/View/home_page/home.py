
import sys
from PyQt5.QtWidgets import QWidget, QAction
from PyQt5.QtGui import QIcon

from Controller.readAMC import *


class HomePage(QWidget):
    def initUI(self, mainWindow):
        mainWindow.setWindowTitle('AMC Module')

        mainMenu = mainWindow.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')

        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(mainWindow.close)
        fileMenu.addAction(exitButton)

        self.show()

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
    boxes , resultatsPoints = computeData()
    print(resultatsPoints)
    boxes, resultatsPoints = updateData()
    print(resultatsPoints)
    # print(getWeights())
    # app = QApplication(sys.argv)
    # ex = window(numberOfQuestions=getNumberOfQuestions())
    # ex.show()
    # ex1 = AppMain()
    # ex = Chart()
    # sys.exit(app.exec_())
