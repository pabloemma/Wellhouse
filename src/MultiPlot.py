




import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import numpy as np
import time
import datetime as dt
import sys
import pandas
import os
class MultiPlot(object):


    num_plots: object

    def __init__(self):

        #initialize some variables
        self.ymin = [] #list of yvalue limits
        self.ymax = []
        self.start_time = 0.
        self.max_time = 0.
        self.temp_y = [0.,0.,0.,0.,0.]

        # create universal home dir
        self.mydir = os.path.expanduser('~')



    def SetNumberOfPlots(self,number):
        self.num_plot = number
        return 0

    def SetupPlots(self):
        """sets up plots according to numbers
        if number is below 5 it is in one coloumn
        if larger than 5 but smaller than 9 two coulmns.
        """


        if(self.num_plot <9): # we just do one column
            self.fig,self.axarr = plt.subplots(self.num_plot,1,sharex=True,figsize=(10,8))
        #elif (self.num_plot > 4 ) and (self.num_plot < 9 ):
        #    ncols=2
        #    nrows = 4
        #    self.fig, self.axarr = plt.subplots(nrows=nrows,ncols=ncols, sharex=True, figsize=(10, 8))
         #   print(self.axarr)  #commented out since I would need to change the ndarra treatment to twodim treatment

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


    def DoPlots(self,x,y):

        col=['b','r','g','b','r']
        #convert unix time to regualr time first
        temp=[]

        for k in range(0,len(x)):
             temp.append(dt.datetime.fromtimestamp(x[k])) #hopefully converts time to datetime


        for k in range(self.num_plot):
            #self.axarr[k].scatter(self.temp_x, self.temp_y[k], color=col[k])
            self.axarr[k].plot_date(temp, y[k], color=col[k])
            #self.axarr[k].plot(x, y[k], color=col[k])
            # add grid
            self.axarr[k].grid(True,linewidth=.2)
            self.axarr[k].yaxis.set_minor_locator(AutoMinorLocator(5.))
            if(k <2) or k==4:
                self.axarr[k].yaxis.set_major_locator(MultipleLocator(10.))

            self.axarr[k].xaxis.set_major_formatter(md.DateFormatter('%m-%d %H:%M'))
            plt.setp(self.axarr[k].get_xticklabels(),rotation=45,horizontalalignment='right')
        # self.ax.scatter(dates,self.temp_y,color ='b')

        # self.ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d %H:%M'))
        # plt.xticks(rotation=90)
        #plt.tight_layout(pad=0,w_pad=-1.6,h_pad=-1)
        plt.savefig(self.mydir+'/wellhousefiles/test.png')
        plt.show(block=True)
        # now save the picture as a png fiile
        plt.pause(0.0001)  # Note this correction
