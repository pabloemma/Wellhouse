#!/usr/bin/env python3
#encoding: UTF-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

""" found this on the internet and modified it
"""


import socket
import threading
import sys
import time
import os
import datetime
from datetime import  date ,timedelta


class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        print( int(time.time())) # strip frac seconds
        print( "starting up the wellhouse server on port" ,self.port)
        print( "**********************************\n\n")
        print( " to stop program, press Ctrl/c \n\n")
        print( "**********************************\n\n")


    def OpenFile(self):
        ''' the default filename is going to be the date of the day
        and it will be in append mode
        '''
        self.current_day = date.today()
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
             
        

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClientAK,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        print( " in listen")
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data 
                    response = data
                    print( "all", response)
                    #client.send(response)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False
            
            
    def listenToClientAK(self, client, address):
        size = 1024
        print( " in listen")
        while True:
             try:
            # wait for data
                data1 = client.recv(1024)
            #if not data: break
                if (len(data1)>0): 
                    #strip out ip
                    temp_data = data1.split(",")
                    data = temp_data[1]
                    
                #print( "this is the receiver and I got",data, len(data))
                    #print( int(time.time()) ,"   ",data , " mm")
                
                
                    if(len(data)==4):
                        #Check if data is an integer, otherwise ignore it
                        if data.isdigit():
                            fl_data = int(data)
                            myline = str(int(time.time()))+','+temp_data[0]+','+data +'\n'
                            print( myline)
                            # check if we have a new day
                            if(date.today()>self.current_day):
                                #we have a new day
                                self.output.close()
                                self.OpenFile()
                                
                            self.output.write(myline)

                        else:
                            print( "error in data block sent , not an integer")
                    else:
                        fl_data = 1
                    #client.send('thanks from server')
                    #self.mysock.close()
                else:
                    break
            #conn.close()
             except:
                client.close()
                return False
              
    def CloseAll(self):
        self.output.close()
        print( ' going away')

       
        sys.exit(0)

if __name__ == "__main__":
    """while True:
        port_num = input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass
    """
    serv = ThreadedServer('',5478)
    serv.OpenFile()
    serv.listen()
    serv.CloseAll()
    


