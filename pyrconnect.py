#!/usr/bin/python

import pexpect 
import os 
import sys
import time

EXPECT_TIMEOUT = 60 ; 


SSH_NEW_KEY_PROMPT="Are you sure you want to continue connecting";
SSH_PASSWORD_PROMT="%s@%s\'s password:"
ROUTER_USER_EXEC_MODE_PROMT=">"
ROUTER_ENABLE_PASSWORD_PROMT="Password:"
ROUTER_PROMPT="#"
#ROUTER_PRIVILAGED_MODE_PROMPT="#"
#ROUTER_GLOBAL_CONFIGURATION_PROMT="\(config\)#"


class SshConnect ( object ):
    def __init__ ( self, deviceip , username, password , enable_password ):
        self.deviceip_ = deviceip
        self.username_ = username
        self.password_ = password
        self.enable_password_= enable_password
        self.session_ = None;
    def connect (self):
        cmd = 'ssh %s@%s' % (self.username_, self.deviceip_ )
        #Spawn a new ssh session 
        self.session_ = pexpect.spawn(cmd)
        self.session_.logfile=sys.stdout

        # After spawning 3 cases need to e handle 
        ret = self.session_.expect( [ SSH_NEW_KEY_PROMPT,
				      SSH_PASSWORD_PROMT % ( self.username_, self.deviceip_ ),
                                      pexpect.TIMEOUT ], EXPECT_TIMEOUT )
        if ret == 0 :
            self.session_.sendline('yes')
            ret = self.session_.expect([SSH_NEW_KEY_PROMPT,
				    SSH_PASSWORD_PROMT % (self.username_, self.deviceip_ ),
                                    pexpect.TIMEOUT],EXPECT_TIMEOUT)
        if ret == 1 :
            self.session_.sendline( self.password_ )
        
        if ret == 2 :
            pass

        # Send carriage return and expect prompt
        #self.session_.sendline( "\r" )
        self.session_.expect( ROUTER_USER_EXEC_MODE_PROMT )
        self.session_.sendline( "enable" )
        self.session_.expect( ROUTER_ENABLE_PASSWORD_PROMT )
        self.session_.sendline( self.enable_password_ )
        
        self.session_.sendline( "\r" )
        self.session_.expect( ROUTER_PROMPT )
        print "DONE"
 
    def sendCmd ( self , cmd ):
        self.session_.sendline( cmd )
        self.session_.expect( ROUTER_PROMPT )
        time.sleep(2)
        return
    
    def getOutput ( self ):
        out = self.session_.before 
        return out 
     
if __name__ == "__main__" :
    username = "cisco"
    password = "cisco"
    deviceip = "192.168.56.202"
    enable_password = "cisco" 
    dutSession = SshConnect( deviceip, username, password, enable_password )
    dutSession.connect ()      
    try :  
        fo = open ( "R1.txt", "r" )
        for line in fo : 
            dutSession.sendCmd(line)
    except IOError :
        print "Error in opening File "
    else :
        print "Configuration done in the device"
        fo.closed

