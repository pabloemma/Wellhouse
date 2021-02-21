import matplotlib.pyplot as plt
import numpy as np
import time





class MyPlot(object):

    def __init__(self):

    # Initialize plots

        #Get start time
        self.start_time = time.time()-5. # start time is programtime minus 5 sec
        self.max_time = self.start_time +3600.


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
        self.ax.set(xlim=(self.start_time, self.max_time), ylim=(0., 1.))

    def RunLoop(self,i=0):
        while i <100:
            self.temp_y = np.random.random();
            self.temp_x = time.time()
            self.x.append(self.temp_x);
            self.y.append(self.temp_y);
            time.sleep(.5)
            self.DoPlot()
            i+=1

    def DoPlot(self):
        plt.scatter(self.temp_x,self.temp_y);

        plt.show()
        plt.pause(0.0001) #Note this correction


if __name__ == '__main__':
    MyP = MyPlot()
    MyP.RunLoop()