import matplotlib.pyplot as plt
import numpy as np
import time





class MyPlot(object):

    def __init__(self,ymin =0.,ymax =100.):

    # Initialize plots

        #Get start time
        self.start_time = time.time()-5. # start time is programtime minus 5 sec
        self.time_window = 100.
        self.max_time = self.start_time +self.time_window

        self.ymin = ymin
        self.ymax = ymax

        plt.ion() ## Note this correction
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1,1,1)


        # set axis
        self.SetAxis()

        self.x=list()
        self.y=list()

    def SetAxis(self):
        """
        We are setting the x and y axis
        xaxis is time. We use min to be start time -5 second, max 3600 after start
        """

        # set axis
        self.ax.set(xlim=(self.start_time, self.max_time), ylim=(self.ymin,self.ymax))
    def SetAxisLabels(self,xlab,ylab):
        """
        Set labels of axis
        """

        self.ax.set_xlabel(xlab)

        self.ax.set_ylabel(ylab)

    def RunLoop(self,i=0):
        """
        Only for test purposes
        """


        while i <100:
            y = np.random.random();
            self.SetValues(y)
            time.sleep(.5)
            self.DoPlot()
            i+=1

    def SetValues(self,y):
        """
        Sets the x = time and y values for the plot
        """
        self.temp_y = y
        self.temp_x = time.time()




        self.x.append(self.temp_x);
        self.y.append(self.temp_y);

    def DoPlot(self):

        # check if we need to extend the axis
        if(self.temp_x > self.max_time -5.):
            self.max_time = self.max_time + self.time_window

            #reset axis
            self.SetAxis()

        self.ax.scatter(self.temp_x,self.temp_y,color ='b')
        plt.show()
        plt.pause(0.0001) #Note this correction


if __name__ == '__main__':
    MyP = MyPlot(0.,1.)
    MyP.RunLoop()