#+----------------------------------------------------+
#| 23/03/2019 - Setting page
#| Created by Sahar Hosseini
#| description,
#| get  AMC params for each exam and save in a csv file
#+----------------------------------------------------+
import csv
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QCheckBox, QMessageBox,QTableWidgetItem,QHeaderView, QTableWidget,QFileDialog, QComboBox,  QGridLayout, QApplication, QFileDialog)

import pandas as pd
from pathlib import Path
class Setting(QWidget):

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
        self.lblTP = QLabel('TP: True Positive')
        self.lblFN = QLabel('FN: False Negative')
        self.lblTN = QLabel('TN: True Negative')
        self.lblFP = QLabel('FP: False Positive')
        self.lblPenalty= QLabel('Initial Penalty: ')
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

        # -------------upload dialog file
        self.btnImport = QPushButton('Import CSV', self)
        self.btnImport.clicked.connect(self.getCSV)

        self.df = pd.DataFrame()
        self.table = QTableWidget()
        # -------------arrange UI with labels, textboxes and buttons
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.cbExams, 0, 0)
        self.grid.addWidget(self.btnImport, 0, 1)

        self.grid.addWidget(self.lblTP, 2, 0)
        self.grid.addWidget(self.txtTP, 2, 1)

        self.grid.addWidget(self.lblFN, 2, 7)
        self.grid.addWidget(self.txtFN, 2, 8)

        self.grid.addWidget(self.lblTN, 3, 0)
        self.grid.addWidget(self.txtTN, 3, 1)

        self.grid.addWidget(self.lblFP, 3, 7)
        self.grid.addWidget(self.txtFP, 3, 8)

        self.grid.addWidget(self.lblPenalty, 2, 9)
        self.grid.addWidget(self.txtPenalty, 2, 10)

        self.grid.addWidget(self.lblWeight, 3, 9)
        self.grid.addWidget(self.txtWeight, 3, 10)

        self.grid.addWidget(btnOK, 9, 9)
        self.grid.addWidget(btnCancel, 9, 10)

        # -------------call layout
        self.setLayout(self.grid)
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
    # -------------save in a csv file
        fileName=self.cbExams.currentText()
        print(fileName)
        f = open(str(fileName)+'.csv', 'w')
        f.write(' TP, FN, TN, FP, Penalty, Weight\n'+
                self.txtTP.text()+"," + self.txtFN.text()
                +","+self.txtTN.text()+","+self.txtFP.text()
                +","+self.txtPenalty.text()
                +","+self.txtWeight.text()+"\n")
        f.close()
        self.close()
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

        #self.close() show csv file in table wiew
        '''self.table.setColumnCount(len(self.df.columns))
        self.table.setRowCount(len(self.df.index))
        rowName = []  # row name
        for i in range(len(self.df.index)):
            for j in range(len(self.df.columns)):
                rowName.append(self.df.columns[j])
                self.table.setItem(i, j, QTableWidgetItem(str(self.df.iloc[i, j])))

        print(rowName)
        self.table.setHorizontalHeaderLabels(rowName)
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()
        self.grid.addWidget(self.table,1,0)'''

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
    ex = Setting()
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
