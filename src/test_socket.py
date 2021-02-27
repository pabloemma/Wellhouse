import socket
import os
from subprocess import Popen,PIPE
mysock = socket.socket() # create socket
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
    #os.kill(int(data[1]), signal.SIGKILL)
