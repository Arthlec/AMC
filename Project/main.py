import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout

from View.home_page.home import HomePage


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.home = HomePage(self)
        self.initUI()

    def initUI(self):
        self.showHome()

    def showHome(self):
        self.home.initUI(self)
        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    sys.exit(app.exec_())
