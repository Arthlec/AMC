import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QGroupBox, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ViewHome(QWidget):
    def __init__(self, parent=None):
        # def __init__(self):
        super(ViewHome, self).__init__()
        self.initUI()

    def initUI(self):
        # title = self.makeTitle()
        newmcq = self.makeNewMCQ()
        # prevmcq = self.makePreviousMCQ()
        layout = QGridLayout()
        # layout.addWidget(title)
        layout.addwidget(newmcq)
        # layout.addWidget(prevmcq)
        self.setLayout(layout)
        self.show()

    def MakeNewMCQ(self):
        # Generate a report for a new mcq
        wid1 = QGroupBox(title='Import a new MCQ')
        layout1 = QVBoxLayout()
        button = QPushButton('Import a new MCQ to create a report')
        layout1.addWidget(button)
        wid1.setLayout(layout1)

        # Content
        layout = QGridlayout()
        layout.addwidget(wid1, 0, 0)
        content = QQwidget()
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
