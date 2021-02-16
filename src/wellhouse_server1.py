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



from array import  array
from multiprocessing.connection import Client
#import KeyBoardPoller


# Collect events until released


class WHSERVER(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
       
        
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
            myline = 'time , ID ,Temp, Humidity,Pressure,Altitude \n'
            self.output.write(myline)
            self.output.flush()
             
            
        
        
    def Establish(self):
        '''
        establish connection with Client
        
        '''
        self.mysock = socket.socket() # create socket
        myip = '' #usually leave empty
        myport = 5478
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
           






        while True:
            try:
            # wait for data
                data = conn.recv(1024)
            #if not data: break
                if (len(data)>0): 
                    #decode bytes back to string for json
                    temp = data.decode("utf-8")
                   # convert string back into dictionary
                    data1 = json.loads(temp)

               
                
                
                    # write to csv file
                    myline = str(int(time.time()))+','+str(data1['ID'])+','+str(data1['Temp'])+','+str(data1['Humidity'])+','+str(data1['Pressure'])+','+str(data1['Altitude'])+'\n'
                    self.output.write(myline)
                    self.output.flush()
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

               
# help wth keyboards
        
            
if __name__ == '__main__':
    tel =WHSERVER()
    tel.OpenFile()
    tel.Establish()
    tel.Looping()
    tel.CloseAll()
   
