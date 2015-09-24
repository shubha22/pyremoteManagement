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
        seq = ( self.deviceip_, "txt" ) 
        fname = '.'.join ( seq ) 
        print fname 
        try :
            fo = open ( fname, "r" )
            for line in fo :
                dutSession.sendCmd(line)
        except IOError :
            print "Error in opening File "
        else :
            print "Configuration done in the device",self.deviceip_
            fo.closed


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
