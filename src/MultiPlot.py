




import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import numpy as np
import time
import datetime as dt
import sys
class MultiPlot(object):


    num_plots: object

    def __init__(self):

        #initialize some variables
        self.ymin = [] #list of yvalue limits
        self.ymax = []
        self.start_time = 0.
        self.max_time = 0.



    def SetNumberOfPlots(self,number):
        self.num_plot = number
        return 0

    def SetupPlots(self):
        """sets up plots according to numbers
        if number is below 5 it is in one coloumn
        if larger than 5 but smaller than 9 two coulmns.
        """


        if(self.num_plot <5): # we just do one column
            self.fig,self.axarr = plt.subplots(self.num_plot,1,sharex=True,figsize=(10,8))
        elif (self.num_plot >4 ) and (self.num_plot < 9 ):
            ncols=2
            nrows = 4
            self.fig, self.axarr = plt.subplots(nrows=nrows,ncols=ncols, sharex=True, figsize=(10, 8))

        else:
            print(' more than 8 plots not iplemented')
            sys.exit(0)

        return 0


    def SetAxis(self):
        """
        We are setting the x and y axis
        xaxis is time.
        """

        # set axis
        for k in range(self.num_plot):
            self.axarr[k].set(xlim=(dt.datetime.fromtimestamp(self.start_time), dt.datetime.fromtimestamp(self.max_time)), ylim=(self.ymin[k], self.ymax[k]))


    def SetAxisLabels(self, xlab, ylab):
        """
        Set labels of axis
        """

        for k in range(self.num_plot):
            self.axarr[k].set_xlabel(xlab)
            self.axarr[k].set_ylabel(ylab[k])

    def SetAxisLimit(self,xmin,xmax,ymin,ymax):
        """
        xlimits are in unix time
        y whatever the measurement is, ylimits are tuple
        """

        self.start_time = xmin
        self.max_time = xmax
        for k in range(self.num_plot):
            self.ymin.append(ymin[k])
            self.ymax.append(ymax[k])