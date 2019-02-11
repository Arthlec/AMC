import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ViewHome(QWidget):
    def __init__(self, parent=None):
        super(ViewHome, self).__init__(parent)
        self.initUI()

    def initUI(self):
        title = self.makeTitle()

        layout = QVBoxLayout()
        layout.addWidget(title)
        self.setLayout(layout)

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
