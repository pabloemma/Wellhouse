#/usr/bin/env python3


"""
Class to connect to remote machine and execute the desired command
You need to make sure that you have a public ssh key on the remote machine.
In case you don't remember how to do this:
http://www.linuxproblem.org/art_9.html
"""



import subprocess
import sys
import os

class RemoteConnect(object):

    def __init__(self,hostip):

        self.hostip = hostip

    def CheckRemoteKey(self):
        """
        Here we check if the keyless ssh has been setup
        if not print error and exit
        """
        checkcmd = '  ssh -oNumberOfPasswordPrompts=0' +' pi@'+self.hostip +'  \"echo hello\" '

        result = os.system(checkcmd)


        if(result !=0):
            print(self.hostip,'does not have key setup yet \n')
            print('checkout http://www.linuxproblem.org/art_9.html')
            sys.exit(0)

        else:
            print('ssh key is setup, you are good to go')

    def ExecuteCommand1(self,checkcmd):

        result = os.system(checkcmd)
        if result == 0: print("You are running")
        return

    def ExecuteCommand(self , command):


        ssh = subprocess.Popen(["ssh", "%s" % 'pi@'+self.hostip, command],
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        if result == []:
            error = ssh.stderr.readlines()
            print(error)
            print ('problems with command ',command)
        else:
            print("you are running")

    def SetCommand(self, command):
        """
        creates the command for the subprocess
        """

        self.command = command

if __name__ == '__main__':
    hostip = '192.168.2.125'
    RC=RemoteConnect(hostip)
    RC.CheckRemoteKey()
    checkcmd = '  ssh -oNumberOfPasswordPrompts=0' + ' pi@' + hostip + '  \"python3 /home/pi/git/Wellhouse/src/wellhouse_control.py 192.168.2.23 &\" '
    RC.ExecuteCommand1(checkcmd)
    #command = "python3 /home/pi/git/Wellhouse/src/wellhouse_control.py & "
    #RC.ExecuteCommand(command)
