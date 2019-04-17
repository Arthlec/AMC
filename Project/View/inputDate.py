from PyQt5.QtWidgets import QDialog, QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
import Controller.readAMC as ReadAMC



class DateInput(QDialog):
    def __init__(self, parent=None):
        super(DateInput, self).__init__(parent)
        self.setModal(True)
        self.initUI()

    def initUI(self):
        label = QLabel('Please enter the date of the exam (it will be written in the reports).', parent=self)
        self.textBox = QLineEdit(parent=self)

        horizGroup = QWidget()
        horizLayout = QHBoxLayout()
        buttonOk = QPushButton('Ok', parent=self)
        buttonCancel = QPushButton('Cancel', parent=self)
        buttonOk.clicked.connect(self.validate)
        buttonCancel.clicked.connect(self.close)
        horizLayout.addWidget(buttonOk)
        horizLayout.addWidget(buttonCancel)
        horizGroup.setLayout(horizLayout)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.textBox)
        layout.addWidget(horizGroup)

        self.setLayout(layout)

    def validate(self):
        if self.textBox.text() != '':
            ReadAMC.setDate(self.textBox.text())
            self.done(1)
