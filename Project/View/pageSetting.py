#+----------------------------------------------------+
#| 23/03/2019 - Setting page
#| Created by Sahar Hosseini
#| description,
#| get  AMC params for each exam and save in a csv file
#+----------------------------------------------------+
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QCheckBox, QMessageBox, QComboBox,  QGridLayout, QApplication)


class SETTING(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'AMC Setting'
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 400
        self.initUI()

    def initUI(self):
        #-------------define labels
        self.lblB = QLabel('B: ')
        self.lblM = QLabel('M: ')
        self.lblP = QLabel('P: ')
        self.lblD = QLabel('D: ')
        self.lblE = QLabel('E: ')
        self.lblV = QLabel('V: ')
        self.lblMax = QLabel('Max: ')
        self.lblHaut = QLabel('Haut: ')
        self.lblMZ = QLabel('MZ: ')
        self.lblPenalty= QLabel('Initial Penalty: ')
        self.lblWeight = QLabel('Initial Weight: ')

        # -------------define text box
        self.txtB = QLineEdit()
        self.txtB.resize(20, 20)
        self.txtM = QLineEdit()
        self.txtM.resize(20, 20)
        self.txtP = QLineEdit()
        self.txtP.resize(20, 20)
        self.txtD = QLineEdit()
        self.txtD.resize(20, 20)
        self.txtE = QLineEdit()
        self.txtE.resize(20, 20)
        self.txtV = QLineEdit()
        self.txtV.resize(20, 20)
        self.txtMax = QLineEdit()
        self.txtMax.resize(20, 20)
        self.txtHaut = QLineEdit()
        self.txtHaut.resize(20, 20)
        self.txtMZ = QLineEdit()
        self.txtMZ.resize(20, 20)
        self.txtPenalty = QLineEdit()
        self.txtPenalty.resize(20, 20)
        self.txtWeight = QLineEdit()
        self.txtWeight.resize(20, 20)

        # -------------define check box
        self.chAuto = QCheckBox("Auto")
        self.chAuto.stateChanged.connect(self.setAutoParams)

        #--------------define combobox list of exam
        self.cbExams = QComboBox()
        self.cbExams.addItem("Exam1")
        self.cbExams.addItem("Exam2")
        self.cbExams.addItem("Exam3")
        self.cbExams.addItem("Exam4")
        self.cbExams.addItem("All")
        self.cbExams.resize(140, 30)
        self.cbExams.currentIndexChanged.connect(self.cbExamOnchange)

        # -------------define buttons
        btnOK = QPushButton("OK")
        btnCancel = QPushButton("Cancel")
        btnOK.clicked.connect(self.saveParams)
        btnCancel.clicked.connect(self.cancelParams)

        # -------------arrange UI with labels, textboxes and buttons
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.cbExams, 0, 0)


        grid.addWidget(self.lblB, 1, 0)
        grid.addWidget(self.txtB, 1, 1)

        grid.addWidget(self.lblM, 1, 7)
        grid.addWidget(self.txtM, 1, 8)

        grid.addWidget(self.lblP, 2, 0)
        grid.addWidget(self.txtP, 2, 1)

        grid.addWidget(self.lblD, 2, 7)
        grid.addWidget(self.txtD, 2, 8)

        grid.addWidget(self.lblPenalty, 1, 9)
        grid.addWidget(self.txtPenalty, 1, 10)

        grid.addWidget(self.lblWeight, 2, 9)
        grid.addWidget(self.txtWeight, 2, 10)

        grid.addWidget(self.lblE, 3, 0)
        grid.addWidget(self.txtE, 3, 1)

        grid.addWidget(self.lblV, 3, 7)
        grid.addWidget(self.txtV, 3, 8)

        grid.addWidget(self.lblMax, 4, 0)
        grid.addWidget(self.txtMax, 4, 1)

        grid.addWidget(self.lblHaut, 4, 7)
        grid.addWidget(self.txtHaut, 4, 8)

        grid.addWidget(self.lblMZ, 5, 0)
        grid.addWidget(self.txtMZ, 5, 1)

        grid.addWidget(self.chAuto, 5, 8)
        grid.addWidget(btnOK, 9, 9)
        grid.addWidget(btnCancel, 9, 10)

        # -------------call layout
        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Setting')
        self.show()

    # -------------function set params auto
    def setAutoParams(self):
        print("click: setAutoParams")

    # -------------function set seam name
    def cbExamOnchange(self):
        print("click: cbExamOnchange")

    # -------------function set params auto
    def saveParams(self):
        print("click: saveParams")
        chAuto=False
        if self.chAuto.isChecked():
            chAuto="True"
        else:
            chAuto="False"

        #QMessageBox.question(self, 'AMC- These values effects on the marks,  after saveing theu will apply.'
        #                           ' Are you sure to save these values?  ', QMessageBox.Warning,QMessageBox.Warning)

    # -------------save in a csv file
        fileName=self.cbExams.currentText()
        print(fileName)
        f = open(str(fileName)+'.csv', 'w')
        f.write('auto, B, M, P, D, E, V, Max, Haut, MZ, Penalty, Weight\n'+
                chAuto+","+self.txtB.text()+"," + self.txtM.text()
                +","+self.txtP.text()+","+self.txtD.text()
                +","+self.txtE.text()+","+self.txtV.text()
                +","+self.txtMax.text()+","+self.txtHaut.text()
                +","+self.txtMZ.text()+","+self.txtPenalty.text()
                +","+self.txtWeight.text()+"\n")
        f.close()
        self.close()
    # -------------function set params auto
    def cancelParams(self):
        print("click: cancelParams")
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SETTING()
    sys.exit(app.exec_())


''' --------------sample how to read csv files
params = []
values = []
 
# open file
with open('params.csv', 'rb') as f:
    reader = csv.reader(f)
 
    # read file row by row
    rowNr = 0
    for row in reader:
        # Skip the header row.
        if rowNr >= 1:
            params.append(row[0])
            values.append(row[1])
 
        # Increase the row number
        rowNr = rowNr + 1
 
# Print data 
print params
print values
'''