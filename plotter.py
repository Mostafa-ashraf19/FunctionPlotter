# Copyright (c) Mostafa Ashraf
# All Styling follows Google Stylings

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import matplotlib
import re
matplotlib.use('Qt5Agg')


class Plotter(FigureCanvasQTAgg):
    '''
    The Plotter inherits |FigureCanvasQTAgg| contains its features. Responsible for parsing, 
    analyzing, and evaluate the user-defined function, 
    return calculation of the function for a certain value.
    '''

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.grid()
        super(Plotter, self).__init__(fig)

    def eval_fun(self, x):
        '''Calculate the value of the function at a certain x.

        Args:
            x (float): The value wants to calculate the function.

        Returns:
            float: value of function at X.
        '''
        return eval(self.equation)

    def parse_equation(self, equation):
        '''Analyze the equation.

        Args:
            equation (str): The equations that's user passed.

        Returns:
            Bool: True if no error, otherwise False.
        '''
        if not ('+' in equation or '-' in equation or '*' in equation or '/' in equation or '^' in equation):
            return False
        if '^' in equation:
            equation = equation.replace('^', '**')
        self.equation = equation
        return True


if __name__ == '__main__':
    # Test cases.
    x = Plotter()
    x.parse_equation('((5*x^3)+2*(x))')
    print(x.eval_fun(2))
    print(x.eval_fun(0.1))
    print(x.eval_fun(-.3))
