# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
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
             
            
        
        
    def Establish(self):
        '''
        establish connection with Client
        for us that should be 192.168.2.22
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
                    myline = str(int(time.time()))+','+str(data1['ID'])+','+str(data1['Temp'])+','+str(data1['Humidity'])+','+str(data1['Pressure'])+','+str(data1['Altitude'])
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
   
