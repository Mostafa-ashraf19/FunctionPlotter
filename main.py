# Copyright (c) Mostafa Ashraf

# It's a base class of all user interface objects in PyQt.
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui, QtWidgets
from plotter import MplCanvas
import os
import sys
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

sys.path.append(os.path.abspath(os.path.join('..', 'FunctionPlotter')))
# Returns tuple of base and child class.
OUR_UI = loadUiType(os.path.join(
    os.path.dirname(__file__), 'UI/MainLayout.ui'))[0]


class MainWindow(QtWidgets.QMainWindow, OUR_UI):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.initiators()
        self.plotbtn.clicked.connect(lambda: self.on_plot_click())
        self.Resetbtn.clicked.connect(lambda: self.on_reset_click())

        

    def initiators(self):
        self.setWindowTitle('Function Plotter')
        self.FunArea.setPlaceholderText('Declare Function')
        self.MinX.setPlaceholderText('Min Fun Value')
        self.MaxX.setPlaceholderText('Max Fun Value')
        self.Xlabel.setPlaceholderText('Xlabel Name')
        self.Ylabel.setPlaceholderText('Ylabel Name')
        self.PlotName.setPlaceholderText('Graph Name')
        self.tabWidget.setTabText(0, 'Function Plate')
        self.tabWidget.setTabText(1, 'Function Points')

    def on_reset_click(self):
        self.sc.axes.cla()
        self.sc.draw()

    def on_plot_click(self):
        self.sc = MplCanvas(self)

        x = np.arange(0, 2, 0.01)
        y = np.array([self.sc.get_fun(val) for val in x])
        self.sc.axes.plot(x, y)

        #  Create toolbar, passing canvas as first parament,
        # parent (self, the MainWindow) as second.

        toolbar = NavigationToolbar(self.sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        # To add into widget.
        self.graph.setContentsMargins(0, 0, 0, 0)
        lay = QtWidgets.QHBoxLayout(self.graph)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(widget)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # Terminate system when window is terminated.
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
