# Project views
## Prototype
Here is a prototype provided in order to normalize the creation of views.
Please use it when creating a view for the project so that it is simpler to
read by everybody or to debug.

* Each view should be in its own file.
* Each view should be implemented as a class that inherits from QWidget
* The aim of a view is to be later on integrated in a QMainWindow object
* More info at that link: https://stackoverflow.com/questions/41290035/pyqt-change-gui-layout-after-button-is-clicked
* The navigation buttons (to go from a view to the other) should be set as class members and the clicked signal will be set in the QMainWindow  
* Please break the creation of the view into functions as much as possible to make it easier to understand. For example, one function for each group of widget

* Add a main function in the code, so that you can easily debug what you're doing

Example:
```python
import sys
from PyQt5.QtWidgets import QApplication, QWidget

class MyView(QWidget):
  def __init__(self, parent=None):
      # important
      super(MyView, self).__init__(parent)

      # Then define your view as you wish
      self.layout = QHBoxLayout()
      self.layout.addWidget(QLabel('Hello'))
      self.layout.addWidget(QLabel('World'))

      # No need for self.show() at the end


# Code executed when the file is launched as main program
if __name__ == '__main__':
  app = QApplication(sys)
  window = QMainWindow()
  view = MyView(parent=window)
  window.setCentralWidget(view)
  sys.exit(app.exec_())
```
