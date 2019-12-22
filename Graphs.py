import matplotlib.pyplot as plt
import matplotlib as mpl
import pylab
from numpy import pi, cos, sin
import math

def Graph_01 (x, y, name_x, name_y, name_graph, label):
    fig = plt.figure()
    plt.plot(x,y,label=label)
    plt.xlabel(name_x, fontsize = 13)
    plt.ylabel(name_y, fontsize = 13)
    plt.title(name_graph, fontsize = 13)
    plt.legend()
    plt.grid(b=None, which='major', axis='both', color = 'black', alpha = 0.4)
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['font.family'] = 'Calibri'
    plt.show()
    #fig.savefig(filename + '.pdf')
