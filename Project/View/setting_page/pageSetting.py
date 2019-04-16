#+----------------------------------------------------+
#| 23/03/2019 - Setting page
#| Created by Sahar Hosseini
#| description,
#| get  AMC params for each exam and save in a csv file
#+----------------------------------------------------+
import csv
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QCheckBox, QMessageBox,QTableWidgetItem,QHeaderView, QTableWidget,QFileDialog, QComboBox,  QGridLayout, QApplication, QFileDialog, QDialog)

import pandas as pd
from pathlib import Path
import Controller.readAMC as ReadAMC

class Settings(QDialog):
    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)
        self.initUI()

    def initUI(self):
        #-------------define labels
        self.lblTP = QLabel('TP: True Positive')
        self.lblFN = QLabel('FN: False Negative')
        self.lblTN = QLabel('TN: True Negative')
        self.lblFP = QLabel('FP: False Positive')
        self.lblWeight = QLabel('Initial Weight: ')

        # -------------define text box
        self.txtTP = QLineEdit()
        self.txtTP.resize(20, 20)
        self.txtFN = QLineEdit()
        self.txtFN.resize(20, 20)
        self.txtTN = QLineEdit()
        self.txtTN.resize(20, 20)
        self.txtFP = QLineEdit()
        self.txtFP.resize(20, 20)
        self.txtWeight = QLineEdit()
        self.txtWeight.resize(20, 20)

        # DEBUG:
        self.txtTP.setText('1.0')
        self.txtFN.setText('-1.0')
        self.txtTN.setText('1.0')
        self.txtFP.setText('-1.0')
        self.txtWeight.setText('1.0')
        # DEBUG

        # -------------define buttons
        btnOK = QPushButton("OK")
        btnCancel = QPushButton("Cancel")
        btnSave = QPushButton("Save")
        btnLoad = QPushButton("Load")
        btnOK.clicked.connect(self.nextView)
        btnCancel.clicked.connect(self.cancelParams)
        btnLoad.clicked.connect(self.loadParams)
        btnSave.clicked.connect(self.saveParams)

        # -------------arrange UI with labels, textboxes and buttons
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.lblTP, 2, 0)
        self.grid.addWidget(self.txtTP, 2, 1)

        self.grid.addWidget(self.lblFN, 2, 7)
        self.grid.addWidget(self.txtFN, 2, 8)

        self.grid.addWidget(self.lblTN, 3, 0)
        self.grid.addWidget(self.txtTN, 3, 1)

        self.grid.addWidget(self.lblFP, 3, 7)
        self.grid.addWidget(self.txtFP, 3, 8)

        self.grid.addWidget(self.lblWeight, 3, 9)
        self.grid.addWidget(self.txtWeight, 3, 10)

        self.grid.addWidget(btnLoad, 9, 7)
        self.grid.addWidget(btnSave, 9, 8)
        self.grid.addWidget(btnOK, 9, 9)
        self.grid.addWidget(btnCancel, 9, 10)

        # -------------call layout
        self.setLayout(self.grid)
        self.resize(350, 300)
        self.setModal(True)
        self.setWindowTitle('Settings')

    # -------------function set params auto
    def setAutoParams(self):
        print("click: setAutoParams")

    # -------------function set seam name
    def cbExamOnchange(self):
        print("click: cbExamOnchange")


    def nextView(self):
        if not self.checkTextBoxes():
            return

        params = {
            "TP" : float(self.txtTP.text()),
            "FN" : float(self.txtFN.text()),
            "TN" : float(self.txtTN.text()),
            "FP" : float(self.txtFP.text()),
            "Weight" : float(self.txtWeight.text()),
        }

        ReadAMC.setParameters(params)
        self.done(1)

    def loadParams(self):
        fileInfo = QFileDialog.getOpenFileName(self, "Select file with your parameters", filter="CSV (*.csv)")
        fileName = fileInfo[0]

        if fileName == '':
            return

        if not fileName.endswith('.csv'):
            fileName += '.csv'

        f = open(fileName, 'r')
        f.readline()    # First line is the title, we don't need it
        paramsString = f.readline()
        params = paramsString.split(',')

        self.txtTP.setText(params[0])
        self.txtFN.setText(params[1])
        self.txtTN.setText(params[2])
        self.txtFP.setText(params[3])
        self.txtWeight.setText(params[4])

    # -------------function set params auto
    def saveParams(self):
        if not self.checkTextBoxes():
            return

        # -------------save in a csv file
        fileInfo = QFileDialog.getSaveFileName(self, "Select file to save your parameters", filter="CSV (*.csv)")
        fileName = fileInfo[0]
        if fileName == '':
            return

        if not fileName.endswith('.csv'):
            fileName += '.csv'

        f = open(fileName, 'w')
        f.write('TP, FN, TN, FP, Weight\n'+
                self.txtTP.text()+"," + self.txtFN.text()
                +","+self.txtTN.text()+","+self.txtFP.text()
                +","+self.txtWeight.text()+"\n")
        f.close()


    def checkTextBoxes(self):
        return self.txtTP.text() != "" and self.txtFN.text() != "" and self.txtTN.text() != "" and self.txtFP.text() != "" and self.txtWeight.text() != ""

    # -------------function set params auto
    def cancelParams(self):
        print("click: cancelParams")
        self.close()

    def getCSV(self):
        filePath,_ = QFileDialog.getOpenFileName(self,
                                                     'CSV File',
                                                     '~/Desktop',
                                                     '*.csv')
        print(filePath)
        filename = Path(filePath).name
        fileName2 = self.cbExams.currentText()
        with open(str(filePath)) as f:
            with open(str(fileName2), "w") as f1:
                for line in f:
                        f1.write(line)

        f1.close()
        f.close()

    def readCSVData(self,filePath):
         params = []
         values = []
         # open file
         with open(str(filePath), 'rb') as f:
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
         return values,params

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Settings()
    sys.exit(app.exec_())
