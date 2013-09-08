#!/usr/bin/python

""" A simple function plotter based on matplotlib, tkinter and numpy
See "Help" -> "Usage" for details on how to use different mathematical functions """

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkMessageBox import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from scipy.misc import factorial
from idlelib import ToolTip
import numpy as np
import matplotlib.pyplot as plt
import parser
import re

REPLACE_DIC = {'sin' : 'np.sin',
               'arcsin' : 'np.arcsin',
               'sinh' : 'np.sinh',
               'arcsinh' : 'np.arcsinh',
               'cos' : 'np.cos',
               'arccos' : 'np.arccos',
               'cosh' : 'np.cosh',
               'arccosh' : 'np.arccosh',
               'tan' : 'np.tan',
               'arctan' : 'np.arctan',
               'tanh' : 'np.tanh',
               'arctanh' : 'np.arctanh',
               'ln' : 'np.log',
               'log' : 'np.log',
               'log10' : 'np.log10',
               'log2' : 'np.log2',
               'exp' : 'np.exp',
               '^' : '**',
               'fac' : 'factorial',
               'sqrt' : 'np.sqrt',
               'pi' : 'np.pi',
               'PI' : 'np.pi',
               'sinc' : 'np.sinc'
               }


class App:

    def __init__(self, master):

        self.master = master
        self.initUI()
        self.x = 0
        self.y = 0
        self.legend = 0

    def initUI(self):
        """ Initialize the GUI-Elements """
        self.master.title("Formula Plotter")

        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        helpmenu = tk.Menu(menu)
        menu.add_cascade(label='Help', menu=helpmenu)
        helpmenu.add_command(label='Usage', command=self.instructions)

        scale_x_min = tk.Scale(self.master, from_=-500, to=0,
                               tickinterval=100, length=600,
                               orient='horizontal', command=self.set_x_min)
        scale_x_min.grid(row=4, column=1)
        self.x_min = tk.IntVar()

        scale_x_max = tk.Scale(self.master, from_=0, to=500,
                               tickinterval=100, length=600,
                               orient='horizontal', command=self.set_x_max)
        scale_x_max.grid(row=5, column=1)
        scale_x_max.set(10)
        self.x_max = tk.IntVar()

        replot_button = tk.Button(self.master, text='New plot',
                                  command=self.replot)
        replot_button.grid(row=0, column=2)
        ToolTip.ToolTip(replot_button,
                        'Clear current plot and draw new function')
        updateplot_button = tk.Button(self.master, text='Add to plot',
                                     command=self.update)
        updateplot_button.grid(row=0, column=3)
        ToolTip.ToolTip(updateplot_button,
                        'Draw new plot on existing')

        minima_button = tk.Button(self.master, text='Local Minima',
                                  command=self.minima)
        minima_button.grid(row=4, column=2)
        ToolTip.ToolTip(minima_button, 'Show local Minima')

        maxima_button = tk.Button(self.master, text='Local Maxima',
                                  command=self.maxima)
        maxima_button.grid(row=5, column=2)
        ToolTip.ToolTip(maxima_button, 'Show local Maxima')
        
        turning_button = tk.Button(self.master, text='Turning point',
                                   command=self.turning_point)
        turning_button.grid(row=6, column=2)
        ToolTip.ToolTip(turning_button, 'Show turning points')
        
        tk.Label(self.master, text='f (x) =').grid(row=0, column=0)
        tk.Label(self.master, text='x minimum').grid(row=4, column=0)
        tk.Label(self.master, text='x maximum').grid(row=5, column=0)

        self.formula = tk.Entry(self.master, width=80)
        self.formula.grid(row=0, column=1)
        self.formula.insert(0, 'sin(x)')

        fig = plt.figure()
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        toolbar = NavigationToolbar2TkAgg(canvas, self.master)
        canvas.get_tk_widget().grid(row=3, column=1)
        toolbar.grid(row=6, column=1)


    def compute_formula(self, accuracy):
        """ Compute the formula, based on re, compile and eval """
        self.x = np.arange(float(self.get_x_min()),
                      float(self.get_x_max()), accuracy)
        x = self.x
        formula_raw = self.formula.get().replace('e^x', 'exp(x)')
        formula_raw_exp = formula_raw.replace('e^', 'exp')
        formula_list = re.split('(\W)', formula_raw_exp)
        formula_replace = [REPLACE_DIC.get(item,item) for item in formula_list]
        formula_join = ''.join(formula_replace)
        formula_list_number = re.split('\d', formula_join)
        for i in xrange(1, len(formula_list_number)):
            try:
                if isinstance(float(formula_list_number[i]), float) and \
                   formula_list_number[i+1] == 'x':
                    formula_list_number.insert(i+1, '*')
            except ValueError:
                pass
        formula_finish = ''.join(formula_list_number)
        form = parser.expr(formula_finish).compile()
        try:
            self.y = eval(form)
            self.legend = self.formula.get()
        except NameError:
            self.y = np.sin(self.x)
            self.legend = 'sin(x)'
            
        return (self.x,self.y,self.legend)

    def replot(self):
        """ Clear old plot and draw new one """
        self.compute_formula(0.01)
        plt.clf()
        plt.plot(self.x,self.y,label=self.legend)
        plt.grid('on')
        plt.legend()
        plt.gcf().canvas.draw()

    def update(self):
        """ Add new plot to the old one(s) """
        self.compute_formula(0.01)
        plt.plot(self.x,self.y, label=self.legend)
        plt.legend()
        plt.gcf().canvas.draw()

    def minima(self):
        """ Calculate the local minimas from the last function """
        self.compute_formula(0.01)
        local_min = (np.diff(np.sign(np.diff(self.y))) > 0).nonzero()[0] + 1
        for i in self.x[local_min]:
            for j in self.y[local_min]:
                plt.text(i, j, [float(np.round(i, decimals=3)),
                                float(np.round(j, decimals=3))])
        plt.plot(self.x[local_min], self.y[local_min], "o")
        plt.gcf().canvas.draw()

    def maxima(self):
        """ Calculate the local maximas from the last function """
        self.compute_formula(0.01)
        local_max = (np.diff(np.sign(np.diff(self.y))) < 0).nonzero()[0] + 1
        for i in self.x[local_max]:
            for j in self.y[local_max]:
                plt.text(i, j, [float(np.round(i, decimals=3)),
                                float(np.round(j, decimals=3))])
        plt.plot(self.x[local_max], self.y[local_max], "o")
        plt.gcf().canvas.draw()

    def turning_point(self):
        """ Calculate the turning points from the last function """
        self.compute_formula(0.00001)
        for i in xrange(1, len(self.y)):
            if self.y[i] < 0 and self.y[i-1] > 0:
                average_y = (self.y[i] + self.y[i-1]) / 2
                average_x = (self.x[i] + self.x[i-1]) / 2
                plt.plot(average_x, average_y, "o")
                plt.text(average_x, average_y, [float(np.round(average_x,
                                                               decimals=3)),
                                                float(np.round(average_y,
                                                               decimals=3))])
                plt.gcf().canvas.draw()
            if self.y[i] > 0 and self.y[i-1] < 0:
                average_y = (self.y[i] + self.y[i-1]) / 2
                average_x = (self.x[i] + self.x[i-1]) / 2
                plt.plot(average_x, average_y, "o")
                np.set_printoptions(precision=3)
                plt.text(average_x, average_y, [float(np.round(average_x,
                                                               decimals=3)),
                                                float(np.round(average_y,
                                                               decimals=3))])
                plt.gcf().canvas.draw()

    def set_x_min(self, val):
        """ Set x-min value with the slider """
        value = int(float(val))
        self.x_min.set(value)

    def get_x_min(self):
        """ Return x-min value """
        return self.x_min.get()

    def set_x_max(self, val):
        """ Set x-max value with the slider """
        value = int(float(val))
        self.x_max.set(value)

    def get_x_max(self):
        """ Return x-max value """
        return self.x_max.get()
        
    def instructions(self):
        """ Opens a info-window and shows the content of usage.txt """
        instruction = open('usage.txt').read()
        showinfo(title='Usage', message=instruction)


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
