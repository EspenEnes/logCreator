from PySide6 import QtWidgets

class QplotWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Viewer")

