# script to run wellhouse tempe

import os
import time
from subprocess import Popen, PIPE
import subprocess
import sys
import os

# start the server
print("starting wellhouse server")

#nonblocking call with Popen
workdir ='/Users/klein/NetBeansProjects/Wellhouse/src/'
server_process = subprocess.Popen(["/usr/local/bin/python3", workdir+"wellhouse_server1.py"],close_fds=True)
#print(server_process)

print("wellhouse_server is running")

# os.system('/usr/local/bin/python3 wellhouse_server1.py &')

# give some time to have the systems start up
time.sleep(10)
print("starting up the remote connect")
#blocking call with call
client_process = subprocess.call(["/usr/local/bin/python3", workdir+"remote_connect.py" ])
print("dodn")
#stdout, stderr = client_process.communicate()

#if we die restart the script:
# but only for 10 counts
#count = 0
#while 1:

#lets make sure we don't have too many counts
# check if file exitst

with open('/Users/klein/wellhousefiles/countloop.txt','r+') as f:
    text = f.read()
    newtext= int(text)+1
    if(newtext > 10):
        # set number back to 0
        f.seek(0)
        f.write(0)
        f.truncate()

        sys.exit(1000)
    else:
        f.seek(0)
        f.write(str(newtext))
        f.truncate()
        print("restart the script")
        os.execv("/usr/local/bin/python3",["/usr/local/bin/python3","temp_control.py"])


# os.system("/usr/local/bin/python3 remote_connect.py ")
