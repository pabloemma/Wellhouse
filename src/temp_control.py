# script to run wellhouse tempe

import os
import time
from subprocess import Popen, PIPE
import subprocess
import sys

# start the server
print("starting wellhouse server")

#nonblocking call with Popen
server_process = subprocess.Popen(["/usr/local/bin/python3", "wellhouse_server1.py"],close_fds=True)
#print(server_process)

print("wellhouse_server is running")

# os.system('/usr/local/bin/python3 wellhouse_server1.py &')

# give some time to have the systems start up
time.sleep(10)
print("starting up the remote connect")
#blocking call with call
client_process = subprocess.call(["/usr/local/bin/python3", "remote_connect.py" ])
print("dodn")
#stdout, stderr = client_process.communicate()

#if we die restart the script:
# but only for 10 counts
#count = 0
#while 1:

print("restart the script")
os.execv("/usr/local/bin/python3",["/usr/local/bin/python3","temp_control.py"])


# os.system("/usr/local/bin/python3 remote_connect.py ")
