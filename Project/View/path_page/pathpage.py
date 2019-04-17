import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLineEdit, QLabel, QPushButton, \
    QFileDialog, QHBoxLayout, QDialog, QMessageBox

import Controller.readAMC as ReadAMC


class PathPage(QDialog):
    def __init__(self, parent=None):
        super(PathPage, self).__init__(parent)
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Enter data path')
        self.setModal(True)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)

        title = QLabel("Please enter the path to your data directory (the one with sqlite files)")
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        self.dataPathEditText = QLineEdit()

        self.dataPathEditText.resize(40, 40)
        self.layout.addWidget(self.dataPathEditText)

        self.sublayout = QHBoxLayout()
        self.sublayout.setSpacing(20)
        self.layout.addLayout(self.sublayout)

        self.b1 = QPushButton("Select Directory")
        self.b1.clicked.connect(self.chooseDirectory)
        self.layout.addWidget(self.b1)

        self.b2 = QPushButton("Confirm Directory")
        self.b2.clicked.connect(self.savePath)
        self.layout.addWidget(self.b2)

        self.setLayout(self.layout)
        self.show()

    def chooseDirectory(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if file != '':
            self.dataPathEditText.setText(file + "/")

    def savePath(self):
        dir = self.dataPathEditText.text()
        if dir != '' and ReadAMC.isValidDirectory(dir):
            ReadAMC.initDirectories(dir)
            self.done(1)
        else:
            QMessageBox.critical(self, 'Incorect path', 'The file you entered does not contain valid sqlite files...', QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex1 = PathPage()
    sys.exit(app.exec_())
