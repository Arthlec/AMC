import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton,\
    QFileDialog, QHBoxLayout
from Controller.readAMC import getDefaultDataPath, writeDataPath

class PathPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DataPath')
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)

        title = QLabel("Please enter the path to your data directory (the one with sqlite files)")
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        self.dataPathEditText = QLineEdit(getDefaultDataPath())
        self.dataPathEditText.resize(40, 40)
        self.layout.addWidget(self.dataPathEditText)

        self.sublayout = QHBoxLayout()
        self.sublayout.setSpacing(20)
        self.layout.addLayout(self.sublayout)

        self.b1 = QPushButton("Select Directory")
        self.b1.setCheckable(True)
        self.b1.toggle()
        self.b1.clicked.connect(self.chooseDirectory)
        self.layout.addWidget(self.b1)

        self.b2 = QPushButton("Confirm Directory")
        self.b2.setCheckable(True)
        self.b2.toggle()
        self.b2.clicked.connect(self.savePath)
        self.layout.addWidget(self.b2)

        self.setLayout(self.layout)
        self.show()

    def chooseDirectory(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.dataPathEditText.setText(file + "/")

    def savePath(self):
        writeDataPath(self.dataPathEditText.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex1 = PathPage()
    sys.exit(app.exec_())
