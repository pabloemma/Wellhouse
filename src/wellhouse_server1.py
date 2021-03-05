# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
"""
this is the main part of the temperature control.
In order for all the communication to work, first start wellhouse_server1.py
On the raspi, you need to run wellhouse_control.py, after the server has come up.
This in turn will call wellhouse.py, which is the actual T measurement and push_data.py
which pushes the data to the server.
Currently the wellhouse_control calls the pseudo data generator in wellhous.py
for the real deal we will need to change this

"""



import socket
import sys
import time
import os
import datetime
import json
import signal
import SendFileMail as SFM
from pathlib import Path
import numpy as np
import MyPlot as MP
import MyMultiPlot as MMP
from subprocess import Popen,PIPE
import math

#import stripper as ST


#from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np
#import matplotlib.animation as animation








# Collect events until released


class WHSERVER(object):
    '''
    classdocs
    '''


    def __init__(self,Multiplot=False):
        '''
        Constructor
        '''
       
        #alarm level , if temperature goes below this value we send an email.
        self.lowtemp = 36. # below 38 we will send an alarm
        self.email = 'pabloemma@gmail.com' #adress for warning
        self.counter = 0 # this counter makes sure that we don't get messages every time.
                         # we do it only every 50 times
        

        self.Multiplot = Multiplot
        #initalize the plotting
        if(Multiplot):
            self.MMPL = MMP.MyMultiPlot([0.,0.,755.,980.,0.],[100.,100.,795.,1100.,100.],5 )
            self.MMPL.SetAxisLabels('Time', ['Temperature [F]', 'Humidity [%]', 'Pressure [hPa]','Barometric P [hPa]','Dew [F]'])

        else:
            self.MPL = MP.MyPlot(ymin=0.,ymax = 100.)
            self.MPL.SetAxisLabels('Time', 'Temperature')

    def OpenFile(self):
        ''' the default filename is going to be the date of the day
        and it will be in append mode
        '''
        a = datetime.datetime.today().strftime('%Y-%m-%d')
        filename = a+'wellhouse.csv'
        # if filename exists we open in append mode
        #otherwise we will create it
        homedir = os.environ['HOME']
        filename = homedir + '/wellhousefiles/'+filename
        print( filename)
        if os.path.isfile(filename):
            self.output = open(filename,'a')
        else :
            self.output = open(filename,'w')
            # write the top line for the columns
            myline = 'time,ID,Temp,Humidity,Pressure,Altitude,Dewpoint\n'
            self.output.write(myline)
            self.output.flush()
             
            
    def CalculateDewPoint(self,Humid,Temp):
        b = 17.62
        c = 243.12


        mygamma = (b * Temp) / (c + Temp) + math.log(Humid / 100.0)
        dewpoint = (c * mygamma) / (b - mygamma)
        #print(dewpoint)
        return dewpoint

    def CalculateSeaLevelP(self,press,temp,alti):
        """ values in SI units """
        term1 = .0065*alti
        term2 = temp+term1+273.15
        term3 = (1-term1/term2)
        term4 = pow(term3,-5.257)
        return press*term4


    def Establish(self):
        '''
        establish connection with Client
        
        '''
        self.mysock = socket.socket() # create socket
        myip = '' #usually leave empty
        myport = 5478

    #check if port is used, and if so kill the process
        process = Popen(["lsof", "-i", ":{0}".format(myport)], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        for process in str(stdout.decode("utf-8")).split("\n")[1:]:
            data = [x for x in process.split(" ") if x != '']
            if (len(data) <= 1):
                continue
            print('killing process ',data[1], ' of user ',data[2])
            os.kill(int(data[1]), signal.SIGKILL)
            time.sleep(60)
        self.mysock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mysock.bind(('',myport))
        self.mysock.listen(5)
        
          # start listening
        
    def Looping(self):
        '''
        Here we listen for the Client
        '''
        #conn,addr = self.mysock.accept() # connection address pair
        conn,addr = self.mysock.accept() # connection address pair
        print( int(time.time())) # strip frac seconds)
        print( "established connection form ",addr)
        print( "**********************************\n\n")
        print( " to stop program, press Ctrl/c \n\n")
        print( "**********************************\n\n")


 # strip frac seconds

        temp_F = lambda x: (x * 1.8)+32.




        while True:
             try:
            # wait for data
                data = conn.recv(1024)
            #if not data: break
                if (len(data)>0): 
                    #decode bytes back to string for json
                    temp = data.decode("utf-8")
                    #print('temp',temp)
                   # convert string back into dictionary
                    try:
                        data1 = json.loads(temp)
                    except:
                        print('problem with jason data \n')
                        continue
                    # convert temperature
                    data1['Temp'] = temp_F(data1['Temp'])
                    data1['Dew']  =self.CalculateDewPoint(data1['Humidity'],data1['Temp'])
                    #check for the temperature and send alarm if temperature goes below value defined in the init part
                    if(data1['Temp'] < self.lowtemp):
                        self.SendAlarm(data1['ID'],data1['Temp'])

                        #self.PutAlarm()
                        
               
                
                    #plot data
                    temp_time = time.time()

                    print(self.CalculateSeaLevelP(data1['Pressure'],data1['Temp'],2281.1))

                    if(self.Multiplot):

                        y=[data1['Temp'],data1['Humidity'],data1['Pressure'],self.CalculateSeaLevelP(data1['Pressure'],data1['Temp'],2281.1), data1['Dew']]
                        self.MMPL.SetValues(y)
                        self.MMPL.DoPlots()
                    else:
                        self.MPL.SetValues(data1['Temp'])
                        self.MPL.DoPlot()
                    # write to csv file
                    myline = str(int(time.time()))+','+str(data1['ID'])+','+str(data1['Temp'])+','+str(data1['Humidity'])+','+str(data1['Pressure'])+','+str(data1['Altitude'])+','+str(data1['Dew'])+'\n'
                    self.output.write(myline)
                    self.output.flush() # this replaces the nobuffering in python2. Otherwise we would wait until a certain amount is taken.

                    if self.FlushTime():
                        self.output.close()
                        print("it is close to midnight, exiting")
                        sys.exit(0)
                    

                    
                    thanks ='thanks from server'
                    conn.send(thanks.encode("utf-8"))
                    #self.mysock.close()
                else:
                    break
             except (KeyboardInterrupt, SystemExit):
                print( "got interrupt")
                self.CloseAll()        
                #self.scope.emitter(int(data))
            #conn.close()
    def CloseAll(self):
        self.mysock.close()
        self.output.close()
        print( ' going away')

       
        sys.exit(0)


    def get_ip_address(self):
        """ get ip address"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]



    def FlushTime(self):

        """
        checks time and if its close tp midnight returns True
        """
        timelimit = 23 * 60. + 45  # this is how many minutes are to 23:45

        b = datetime.datetime.now()
        # fill in tuple
        a = b.timetuple()
        current_minute = a[3] * 60. + a[4]
        if (current_minute > timelimit):
            return True
        else:
            return False

    def PutAlarm(self):
        """
        gives alarm when temp too low
        """
        for k in range(2):

            os.system('say "Santa Fe we got a problem, wellhouse Temperature is low"')




        return

    def SendAlarm(self,ID,Temp):           
        """ this sends an email if Temperature is below the setpoint"""
  
        subject = ' Warning, Temp in sensor '+str(ID) +' low currently at ' +str(Temp)+'F'

        home = str(Path.home())   

        
        message = ' problems with temperature ' + str(ID)+'   '+str(Temp)+'F'
        if(self.counter == 0 ):
            sa = SFM.MyMail(self.email,subject, message)
            sa.send_email_pdf_figs(home+'/private/LCWA/andifile',message)
 
        self.counter +=1
        if self.counter == 49:
            self.counter = 0
        
        return
        


        
        
        
            
if __name__ == '__main__':
    tel =WHSERVER(Multiplot=True)
    tel.OpenFile()
    tel.Establish()
    tel.Looping()
    tel.CloseAll()
   




