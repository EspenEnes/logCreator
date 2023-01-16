from random import randint

from PySide6 import QtWidgets, QtCore
from plotter import QplotWidget
import pyqtgraph as pg
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(0)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.x = [0]
        self.y = [0]

        # plot data: x, y values
        self.data_line = self.graphWidget.plot(self.x, self.y)

        self.yRange = [0,0]



    def updateY(self, new):
        if new > self.data_line.getViewBox().state["viewRange"][1][1]:
            self.yRange[1] = new
            self.graphWidget.setYRange(self.yRange[0], self.yRange[1])

        elif new < self.data_line.getViewBox().state["viewRange"][1][0]:
            self.yRange[0] = new
            self.graphWidget.setYRange(self.yRange[0], self.yRange[1])




    def update_plot_data(self):
        # self.x = self.x[1:]  # Remove the first y element.
        # self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.
        self.x.append(self.x[-1] + 1)


        # self.y = self.y[1:]  # Remove the first
        self.y.append(self.y[-1] + randint(-1, 1))  # Add a new random value.


        if len(self.x) > 2000:
            self.x = self.x[1:]
            self.y = self.y[1:]


        self.data_line.setData(self.x, self.y)  # Update the data.
        self.updateY(self.y[-1])




if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())