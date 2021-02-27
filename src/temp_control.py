#script to run wellhouse tempe

import os
import time

#start the server
os.system('/usr/local/bin/python3 wellhouse_server1.py &')

# give some time to have the systems start up
time.sleep(40)

os.system('/usr/local/bin/python3 remote.connect.py &')