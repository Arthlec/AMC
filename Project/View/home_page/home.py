
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

from View.path_page.pathpage import PathPage
from View.setting_page.pageSetting import Settings
from View.report_page.pageReport import ReportPage

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
        self.mainWindow = mainWindow
        mainWindow.setWindowTitle('AMC Module')

        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget(self.createTitle())
        verticalLayout.addWidget(self.createInterface())
        self.setLayout(verticalLayout)
        self.mainWindow.setCentralWidget(self)


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
        self.newCorrectionButton = QPushButton('New correction')
        self.newCorrectionButton.setFixedSize(300, 100)
        font = QFont()
        font.setPointSize(12)
        self.newCorrectionButton.setFont(font)
        self.newCorrectionButton.clicked.connect(self.selectPath)

        return self.newCorrectionButton

    def selectPath(self):
        pathDialog = PathPage(self.mainWindow)
        n = pathDialog.exec_()
        if n == 1:
            n = 0
            pageSetting = Settings(self.mainWindow)
            n = pageSetting.exec_()
            if n == 1:
                reportPage = ReportPage(self.mainWindow)
                reportPage.initUI(self.mainWindow)



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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QMainWindow()
    w.showMaximized()
    sys.exit(app.exec_())
