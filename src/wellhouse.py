# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


import time

#import board #!!!!!!! uncomment this on Linux
import busio
import adafruit_bme280
import random
import json

class Tmeas(object):
    """ class to measure the temperature from the Bosch BE280
    based on example code from adafruit using their library
    """

    def __init__(self,ID):
        '''
        ID is the temp sensor
        0: Well House
        1: Guest House
   
         '''
        self.testing = False  # this is a flag to test the program without sensor
                             #will do the connection to the server and send pseudo data
 
         
       
         
        # initialize the random generator for testing purposes
        if self.testing:
            random.seed()
         
        # the dictionary of values which will be sent to the main server
        self.ID = ID
        self.result = {'ID':ID,'Temp':0.,'Humidity':0.,'Pressure':0.,'Altitude':0.}


        #switch for debug
        self.debug = True
        
        # Create library object using our Bus I2C port
        if not self.testing:
            self.InitializeI2C()
        #else:
        #    while True:
                
        #        print(json.loads(self.PseudoData()))
        #        time.sleep(10)
            
  
        
    def InitializeI2C(self):
        """Initailze the I2C system"""
        i2c = busio.I2C(board.SCL, board.SDA)
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

        # OR create library object using our Bus SPI port
        # spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        # bme_cs = digitalio.DigitalInOut(board.D10)
        # bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

        # change this to match the location's pressure (hPa) at sea level
        self.bme280.sea_level_pressure = 1013.25
        
        
            
    def Measure(self):
        """ this returns a dictionary of values"""
        
        
        if(self.debug):
            print('measuring \n ')

            print("\nTemperature: %0.1f C" % bme280.temperature)
            print("Humidity: %0.1f %%" % bme280.relative_humidity)
            print("Pressure: %0.1f hPa" % bme280.pressure)
            print("Altitude = %0.2f meters" % bme280.altitude)
            
        
        self.result['Temp'] = self.bme280.temperature
        self.result['Humidity'] = self.bme280.humidity
        self.result['Pressure'] = self.bme280.pressure
        self.result['Altitude'] = self.bme280.altitude
        
        
        # the data communication expects a string so we use json.dumps(result)
        #on the send side and json.loads(result) on the reciever to get back to dict
        
    

        #return json.dumps(self.result)
        return self.result
    
    def PseudoData(self):
        """ create pseudo data for test purposes"""
        self.result['Temp'] = random.uniform(10.,80.)
        self.result['Humidity'] = random.uniform(10.,100.)
        self.result['Pressure'] = random.uniform(1000.,1100.)
        self.result['Altitude'] = 1014.
 
        #return json.dumps(self.result)
        return self.result




if __name__ == "__main__":
    TM = Tmeas(0)
    TM.Measure


