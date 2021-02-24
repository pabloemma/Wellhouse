import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import time
import datetime as dt
import sys


class MyMultiPlot(object):

    def __init__(self, ymin,ymax,num_plot=0):

        # Initialize plots
        # currently at the most 4 plots
        max_plot = 4
        self.num_plot = num_plot
        # Get start time
        self.start_time = time.time() - 5.  # start time is programtime minus 5 sec
        self.time_window = 100.
        self.max_time = self.start_time + self.time_window

        self.ymin = ymin #list for different plots
        self.ymax = ymax
        self.temp_y = [0.,0.,0.]

        plt.ion()  ## Note this correction
        #check for numbers
        if(num_plot > max_plot):
            print('can only do ', max_plot,' number of plots \n')
            sys.exit(0)

        self.fig, self.axarr = plt.subplots(self.num_plot,1,sharex=True)


        self.x = list() #always time
        self.y = list()
        # create list of list
        for k in range(num_plot):
            self.y.append(list())

        # set axis
        self.SetAxis()


    def SetAxis(self):
        """
        We are setting the x and y axis
        xaxis is time. We use min to be start time -5 second, max 3600 after start
        """

        # set axis
        for k in range(self.num_plot):
            self.axarr[k].set(xlim=(self.start_time, self.max_time), ylim=(self.ymin[k], self.ymax[k]))

    def SetAxisLabels(self, xlab, ylab):
        """
        Set labels of axis
        """

        for k in range(self.num_plot):
            self.axarr[k].set_xlabel(xlab)
            self.axarr[k].set_ylabel(ylab[k])

    def RunLoop(self, i=0):
        """
        Only for test purposes
        """

        while i < 100:
            y = np.random.random();
            self.SetValues(y)
            time.sleep(.5)
            self.DoPlot()
            i += 1

    def SetValues(self, y):
        """
        Sets the x = time and y values for the plot
        """
        self.temp_x = time.time()
        self.x.append(self.temp_x);
        for k in range(self.num_plot):
            self.temp_y[k] = y[k]

            self.y[k].append(y[k]);

    def DoPlots(self):

        # check if we need to extend the axis
        if (self.temp_x > self.max_time - 5.):
            self.max_time = self.max_time + self.time_window

            # reset axis
            self.SetAxis()
        # dates = dt.datetime.fromtimestamp(self.temp_x)
        col=['b','r','g']
        for k in range(self.num_plot):
            self.axarr[k].scatter(self.temp_x, self.temp_y[k], color=col[k])
        # self.ax.scatter(dates,self.temp_y,color ='b')

        # self.ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d %H:%M'))
        # plt.xticks(rotation=90)
        plt.tight_layout(pad=0,w_pad=-1.6,h_pad=-1)
        plt.show()
        plt.pause(0.0001)  # Note this correction


if __name__ == '__main__':
    MyP = MyPlot(0., 1.)
    MyP.RunLoop()
