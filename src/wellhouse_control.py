# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.



import time
import wellhouse as WH
import push_data as PD
if __name__ == '__main__':
    #establish connection
    ip_server = '192.168.2.24' # change for apporpitae server this is andi airbook
    #ip_server = '192.168.2.41' # change for apporpitae server
    server_port = 5478
    # serial connection device
    device_name = '/dev/ttyS0'

    MyPush = PD.Push(ip_server,server_port)
    MyPush.Connect2Server()
    # now open up the serial port
    WH1 = WH.Tmeas(0)
    while 1:
        data = WH1.Measure()
        print('wellhouse control',data)
        MyPush.PushData(data)
        time.sleep(600)
 
    MyPush.CloseConnection()    
    