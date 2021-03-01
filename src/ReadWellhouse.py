"""
Will read the wellhouse files and display
"""

import pandas as PD
import MyMultiPlot as MMP
import time

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
        self.time = self.mydata['time ']
        self.Temp=self.mydata['Temp']
        self.Humi =self.mydata[' Humidity']
        self.Press=self.mydata['Pressure']
        self.Alti=self.mydata['Altitude ']
        self.Dew =self.mydata[' Dewpoint']

        self.MMPL = MMP.MyMultiPlot([0., 0., 755., 2150., 0.], [100., 100., 775., 2350., 100.], 5,start_time=self.time[0]-5)
        self.MMPL.SetAxisLabels('Time', ['Temperature [F]', 'Humidity [%]', 'Pressure [hPa]', 'Altitude [m]', 'Dew [F]'])

    def DoPlots(self):

        for k in range(len(self.Temp)):
            y = [self.Temp[k],self.Humi[k],self.Press[k],self.Alti[k],self.Dew[k]]

            self.MMPL.SetValues(y)
        self.MMPL.DoPlots()
        time.sleep(60)


if __name__ == '__main__':
    dir = '/Users/klein/wellhousefiles/'
    filename = dir +'2021-02-28wellhouse.csv'

    WR = WellhouseRead(filename)
    WR.DoPlots()