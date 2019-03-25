import sys
import PyQt5.QtWidgets.QGridLayout

from PyQt5.QtWidgets import QApplication, QWidget


class CoherencePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Coherence')

        layout = QGridLayout()
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 3)

        txtCoherence = QLineEdit("Please Enter your Coherence Formula")
        txtCoherence.resize(20, 20)
        layout.addWidget(txtCoherence, 0, 0)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex1 = CoherencePage()
    sys.exit(app.exec_())
