
'''
:author: pbrian <paul@mikadosoftware.com>

Quick start
-----------

On ubuntu:

   

bibliography:

http://skype4py.sourceforge.net/doc/html/
  Oddly the source is missing from skype.com and hard to find on sourceforge.

http://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html
   USeful kickstarter

http://www.futuredesktop.com/tmp/py-test1.py
and
http://ubuntuforums.org/showthread.php?t=1652554
  Seems to have leaned heavily on skype4py


WHy not use Skype4py?
---------------------
Frankly, because i cannot download it - I simply cannot get it off sourceforge.
Admittedly I have not tried hard, as I have put together this script to solve my problems.  But the author Arkadiusz Wahlig, seems to have left it or gotten lost by Skype moving developer.skype around and I don't know where to go next.

Anyway...


Notify - There are 2 buses - one for client to Skype /com/Skype and one for Skyoe to us /com/Skype/Client.  This will call a Notify Interface on the dbus and put messages on there.  So what we need to do is create a dbus service method called Notify that does something pythonic with a text string handed to it.

Basically read the remote dbus.  i have nicked most of that code from Skype4py

'''

import os
import sys
import dbus
import dbus.service
import time
import gobject

from dbus.mainloop.glib import DBusGMainLoop

from threading import Thread

class pySkypeError(Exception):
    ''' '''
    pass

class SkypeNotify(dbus.service.Object):

    """DBus object which exports a Notify method. This will be called
    by Skype for all notifications with the notification string as a
    parameter. The Notify method of this class calls in turn the
    callable passed to the constructor.
    """

    def __init__(self, bus):
        dbus.service.Object.__init__(self, bus, '/com/Skype/Client')
        print 'Skype notify init done'

    @dbus.service.method(dbus_interface='com.Skype.API.Client')
    def Notify(self, com):
        print 'it works, that s what I got from Skype:'
        print com

class pySkype(Thread):
    '''Create a connection via dbus to Skype, returning a dbus object
    
    self.skypeo is the dbus object, with ability to:

    s.skypeo.Invoke(CALL +4407540456115)

    '''
   
    def __init__(self):
        #dbus requires this mainloop approach. Cannot be a simple script as I hoped it could be
        session_dbus = dbus.SessionBus(mainloop=DBusGMainLoop(set_as_default=True))
        try:
            dbus_obj = session_dbus.get_object('com.Skype.API', '/com/Skype')
        except Exception, e: 
            raise pySkypeError('Unable to connect to skype on dbus - %s' % e)
        ## bind to skype 
        resp = dbus_obj.Invoke('NAME pySkype')
        if resp != u'OK': raise pySkypeError('Failed to register NAME')
        resp =  dbus_obj.Invoke('PROTOCOL 7')
        if resp != u'PROTOCOL 7': raise pySkypeError('Failed to register PROTOCOL')

        ### add notify 
        self.skype_notify = SkypeNotify(session_dbus)
        self.skypeo = dbus_obj
        gobject.threads_init()

        Thread.__init__(self)

    def run(self):
        self.mainloop = gobject.MainLoop()
        context = self.mainloop.get_context()
        while True:
            context.iteration(False)
            time.sleep(0.2)

    def invoke(self, cmd, *arglist):
        ''' '''
        fullcmd = '%s %s' % (cmd, ' '.join(arglist))
        resp = self.skypeo.Invoke(fullcmd)
        
