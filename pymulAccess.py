#!/usr/bin/python 

import threading 
import os
from pyrconnect import SshConnect

def checkPing ( ipadd ) :
    ipadd_ = ipadd
    response = os.system ( 'ping -c 2 ' + ipadd )
    return response
       

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
        response = checkPing ( self.deviceip_ )
        print response
        if response == 0 :
            dutSession = SshConnect( self.deviceip_, self.username_, self.password_, self.enable_password_ )
            dutSession.connect () 
            seq = ( self.deviceip_, "txt" ) 
            fname = '.'.join ( seq ) 
            try :
                fo = open ( fname, "r" )
                for line in fo :
                    dutSession.sendCmd(line)
            except IOError :
                    print "Error in opening File "
            else :
                print "Configuration done in the device",self.deviceip_
                fo.closed
        else :
            print "Device ",self.deviceip_," is not reachable. Please fix the connection issue and retry configuration"


if __name__ == "__main__" :
    print "Main SART"
    c = 0
    t = [ ]  
    try :
        fo = open ( "config.txt", "r" )
        for line in fo :
            l = line.split( ',' )
            t.append( rConnect ( l[0],l[1],l[2],l[3].strip( '\n' ) ))
            t[c].start()
            c += 1 
        print "Main END"
    except IOError :
        print "Require file is missing"
