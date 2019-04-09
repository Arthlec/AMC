import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
from View.home_page.home import HomePage

class FirstWindow(QWidget):
    def initUI(self, mainWindow):
        mainWindow.setWindowTitle('Fenetre 1')
        self.centralWidget = QWidget(mainWindow)

        self.button = QPushButton('Aloha', self.centralWidget)
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        mainWindow.setLayout(layout)
        mainWindow.setCentralWidget(self.centralWidget)

class SecondWindow(QWidget):
    def initUI(self, mainWindow):
        mainWindow.setWindowTitle('Fenetre 2')
        self.centralWidget = QWidget(mainWindow)

        self.button = QPushButton('Wesh', self.centralWidget)
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        mainWindow.setLayout(layout)
        mainWindow.setCentralWidget(self.centralWidget)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.home = HomePage(self)
        # self.reportPage = ReportPage(self)
        # self.second = SecondWindow(self)
        self.initUI()

    def initUI(self):
        self.showHome()

    def showHome(self):
        self.home.initUI(self)
        self.show()

    def showReportPage(self):
        self.reportPage.initUI(self)
        self.show()

    def showSecond(self):
        self.second.initUI(self)
        self.second.button.clicked.connect(self.showFirst)
        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    sys.exit(app.exec_())
