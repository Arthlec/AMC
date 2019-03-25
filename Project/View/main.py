import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
import home_page

class FirstWindow(QWidget):
    def initUI(self, mainWindow):
        mainWindow.setWindowTitle('Fentre 1')
        self.centralWidget = QWidget(mainWindow)

        self.button = QPushButton('Aloha', self.centralWidget)
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        mainWindow.setLayout(layout)
        mainWindow.setCentralWidget(self.centralWidget)

class SecondWindow(QWidget):
    def initUI(self, mainWindow):
        mainWindow.setWindowTitle('Fentre 2')
        self.centralWidget = QWidget(mainWindow)

        self.button = QPushButton('Wesh', self.centralWidget)
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        mainWindow.setLayout(layout)
        mainWindow.setCentralWidget(self.centralWidget)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.first = FirstWindow(self)
        self.second = SecondWindow(self)
        self.initUI()

    def initUI(self):
        
        self.showFirst()

    def showFirst(self):
        self.first.initUI(self)
        self.first.button.clicked.connect(self.showSecond)
        self.show()

    def showSecond(self):
        self.second.initUI(self)
        self.second.button.clicked.connect(self.showFirst)
        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
