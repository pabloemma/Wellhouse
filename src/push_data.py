# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import socket
import sys
from multiprocessing.connection import Client
class Push(object):
    '''
    classdocs
    '''


    def __init__(self,ip_server,server_port):
        '''
        Constructor
        '''
        self.temp_server = ip_server # connect with ip of server
        self.temp_port = server_port
	print( "Temp server", self.temp_server,"on port ", self.temp_port)
    
    def Connect2Server(self):
        '''
        this establisk the socket connection with the server
        '''
        self.mysocket = socket.socket()  #use default protocol and stream
        # now connect to the server
        print ("Esatablishing connection")
        self.mysocket.connect((self.temp_server,self.temp_port))
    def PushData(self,databuffer): 
        '''
        pushes data to server
        '''
	
        # make sure we know that we transmitted all the bytes
	# pack in the last digits of the IP address
	ip = self.get_ip_address()
	ip_tup = ip.split(".")
	ip_temp = ip_tup[3]+','  # add comma as separator
	
	databuffer = ip_temp + databuffer
	
        temp=len(databuffer.encode('utf-8')) # length in bytes of databuffer, whih needs to be a string
        bytes_sent =self.mysocket.send(databuffer) # returns number of bytes sent
        if(temp - bytes_sent != 0):
            print( "got ",temp," bytes  but sent ",bytes_sent,"  bytes")
        # get ack back from server
        #response = self.mysocket.recv(1024)
        #print (response) 
        
    def get_ip_address(self):
        """ get ip address"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
        
           
    def CloseConnection(self):  
        '''
        closes all connections
        '''
        self.mysocket.close()
         
if __name__ == '__main__':
    ip_server = '192.168.2.24' # change for apporpitae server
    server_port = 5478
    
    MyPush = Push(ip_server,server_port)
    MyPush.Connect2Server()
    MyPush.PushData('R0430')
    MyPush.CloseConnection()





