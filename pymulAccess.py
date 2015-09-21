#!/usr/bin/python 

import threading 
from pyrconnect import SshConnect

class rConnect( threading.Thread ):
   
    def __init__ ( self, deviceip , username, password , enable_password ):
        threading.Thread.__init__(self)
        self.deviceip_ = deviceip
        self.username_ = username
        self.password_ = password
        self.enable_password_= enable_password
        print "[+] New thread started fo ==>  ",deviceip
    
    def run (self):
        print "Connection from : ",self.deviceip_
        dutSession = SshConnect( self.deviceip_, self.username_, self.password_, self.enable_password_ )
        dutSession.connect ()
        try :
            fo = open ( "R1.txt", "r" )
            for line in fo :
                dutSession.sendCmd(line)
        except IOError :
            print "Error in opening File "
        else :
            print "Configuration done in the device",self.deviceip_
            fo.closed


if __name__ == "__main__" :
    print "Main SART"
    #t1 = Thread ( target = rConnect, args = ( "192.168.56.201","cisco","cisco","cisco" ))
    #t2 = Thread ( target = rConnect, args = ( "192.168.56.202","cisco","cisco","cisco" ))
    t1 = rConnect ( "192.168.56.201","cisco","cisco","cisco" )
    t2 = rConnect ( "192.168.56.202","cisco","cisco","cisco" )
    t1.start()
    t2.start()
    print "Main END"
