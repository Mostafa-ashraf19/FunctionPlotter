# Copyright (c) Mostafa Ashraf

# It's a base class of all user interface objects in PyQt.
from PyQt5.QtWidgets import QApplication, QMessageBox
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
        self.on_text_changes()

    def initiators(self):
        self.setWindowTitle('Function Plotter')
        self.FunArea.setPlaceholderText('Declare Function')
        self.MinX.setPlaceholderText('Min Fun Value')
        self.MaxX.setPlaceholderText('Max Fun Value')
        self.Xlabel.setPlaceholderText('Xlabel Name')
        self.Ylabel.setPlaceholderText('Ylabel Name')
        self.PlotName.setPlaceholderText('Graph Name')
        self.tabWidget.setTabText(0, 'Function Palette')
        self.tabWidget.setTabText(1, 'Function Points')
        self.plotbtn.setEnabled(False)
        self.Resetbtn.setEnabled(False)
        self.svgraph.setEnabled(False)
        self.plotbtn.clicked.connect(lambda: self.on_plot_click())
        self.Resetbtn.clicked.connect(lambda: self.on_reset_click())
        self.svgraph.clicked.connect(lambda: self.on_save_graph())

    def warning_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText('More information')
        msg.setWindowTitle("Error")
        msg.exec_()

    def on_save_graph(self):
        """
        Save graph X, Y points
        E.g.
        -2,0,2,.....  # X
         4,0,4,.....  # Y
        """
        f = open(f'function {self.FunArea.text()} values.txt', 'a')
        f.write(','.join([str(a) for a in self.x_values]))
        f.write('\n')
        f.write(','.join([str(a) for a in self.x_values]))
        f.close()

    def on_text_changes(self):
        self.FunArea.textChanged.connect(lambda: self.enable_plot())
        self.MinX.textChanged.connect(lambda: self.enable_plot())
        self.MaxX.textChanged.connect(lambda: self.enable_plot())

    def enable_plot(self):
        if self.FunArea.text() != "" and self.MinX.text() != "" and self.MaxX.text() != "":
            self.plotbtn.setEnabled(True)

    def on_reset_click(self):
        self.sc.axes.cla()
        self.sc.draw()
        self.sc = None
        self.plotbtn.setEnabled(False)
        self.Resetbtn.setEnabled(False)
        self.svgraph.setEnabled(False)
        self.tableWidget.setRowCount(0)
        self.graph.itemAt(0).widget().deleteLater()
        self.FunArea.clear()
        self.MinX.clear()
        self.MaxX.clear()
        self.Xlabel.clear()
        self.Ylabel.clear()
        self.PlotName.clear()
        self.y_values = None
        self.x_values = None

    def fill_table(self, x, y):
        xlabel = 'X' if self.Xlabel.text() == "" else self.Xlabel.text()
        ylabel = 'Y' if self.Ylabel.text() == "" else self.Ylabel.text()

        self.tableWidget.setHorizontalHeaderLabels([xlabel, ylabel])
        x_len = len(x)
        self.tableWidget.setRowCount(x_len)
        for index in range(x_len):
            self.tableWidget.setItem(
                index, 0, QtWidgets.QTableWidgetItem(str(x[index])))
            self.tableWidget.setItem(
                index, 1, QtWidgets.QTableWidgetItem(str(y[index])))

        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)

    def validate_inputs(self):
        if not self.sc.parse_equation(self.FunArea.text()):
            return False, 0
        try:
            float(self.MinX.text()), float(self.MaxX.text())
        except ValueError:
            return False, 0

        return float(self.MinX.text()), float(self.MaxX.text())

    def on_plot_click(self):
        self.sc = MplCanvas(self)

        min_x, max_x = self.validate_inputs()
        if min_x == False:
            self.warning_message()
            return

        self.x_values = np.arange(min_x, max_x, 0.01)
        self.y_values = np.array([self.sc.eval_fun(val)
                                 for val in self.x_values])
        self.sc.axes.plot(self.x_values, self.y_values)

        xlabel = 'X' if self.Xlabel.text() == "" else self.Xlabel.text()
        ylabel = 'Y' if self.Ylabel.text() == "" else self.Ylabel.text()
        title = 'Function ' + \
            self.FunArea.text() if self.PlotName.text() == "" else self.PlotName.text()

        self.sc.axes.set_xlabel(xlabel)
        self.sc.axes.set_ylabel(ylabel)
        self.sc.axes.set_title(title)

        # Create toolbar, passing canvas as first parament,
        # parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        # To add into widget.
        self.graph.addWidget(widget)

        self.fill_table(self.x_values, self.y_values)
        self.Resetbtn.setEnabled(True)
        self.svgraph.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # Terminate system when window is terminated.
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
