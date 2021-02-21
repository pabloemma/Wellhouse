import matplotlib.pyplot as plt
import numpy as np
import time




class MyPlot(object):

    def __init__(self):

    # Initialize plots


        plt.ion() ## Note this correction
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1,1,1)


        # set axis
        self.ax.set(xlim=(0,100.),ylim=(0.,1.))

        self.x=list()
        self.y=list()


    def RunLoop(self,i=0):
        while i <200:
            self.temp_y=np.random.random();
            self.x.append(i);
            self.y.append(self.temp_y);
            time.sleep(.5)
            self.DoPlot(i)
            i+=1

    def DoPlot(self,i):
        plt.scatter(i,self.temp_y);

        plt.show()
        plt.pause(0.0001) #Note this correction


if __name__ == '__main__':
    MyP = MyPlot()
    MyP.RunLoop()