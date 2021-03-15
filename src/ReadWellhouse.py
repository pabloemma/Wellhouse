"""
Will read the wellhouse files and display
"""

import pandas as PD
import MultiPlot as MMP
import time
import datetime as dt

class WellhouseRead(object):

    def __init__(self,filename):


        self.ReadCSV(filename)



    def ReadCSV(self,filename):
        """
        reads csv file into a pandas structure

        """
        self.mydata = mydata = PD.read_csv(filename)
        # this is a bit clumsier than I wanted, but this way it interfaces with multiplots
        for col in self.mydata.columns:
            print(col)
        self.time = self.mydata['time']
        self.Temp=self.mydata['Temp']
        self.Humi =self.mydata['Humidity']
        self.Press=self.mydata['Pressure']
        self.Alti=self.mydata['Altitude']
        self.Dew =self.mydata['Dewpoint']

    def SetAxisLimits(self,ymin,ymax):
        self.ymin = []
        self.ymax = []
        self.xmin = self.time[0]-60.
        self.xmax = self.time[len(self.time)-1]
        for k in range(len(ymin)):
            self.ymin.append(ymin[k])
            self.ymax.append(ymax[k])

        self.MMPL.SetAxisLimit(self.xmin,self.xmax,self.ymin,self.ymax)

    def SetupPlotSystem(self):

        self.MMPL = MMP.MultiPlot()
        # set the number of plots
        numpl=5
        self.MMPL.SetNumberOfPlots(numpl)
        self.MMPL.SetupPlots()
        self.MMPL.SetAxisLabels('Time', ['Temperature [F]', 'Humidity [%]', 'Pressure [hPa]', 'Altitude [m]', 'Dew [F]'])

    def DoPlots(self):


        x = self.time
        y = [self.Temp,self.Humi,self.Press,self.Alti,self.Dew]

        self.MMPL.DoPlots(x,y)
        time.sleep(60)


if __name__ == '__main__':
    dir = '/home/klein/wellhousefiles/'
    filename = dir +'2021-03-12wellhouse.csv'

    WR = WellhouseRead(filename)
    WR.SetupPlotSystem()


    ymin =[0., 0., 755., 980., 0.]
    ymax = [100., 100., 795., 1100., 100.]


    WR.SetAxisLimits(ymin,ymax)
    WR.DoPlots()