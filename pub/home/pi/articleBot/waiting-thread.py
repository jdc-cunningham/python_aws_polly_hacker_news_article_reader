import time, os, threading
from threading import Thread

poll_started = str = open('/home/pi/articleBot/poll_started.txt', 'r').read()

def start_poll():
    os.system('/usr/bin/python /home/pi/articleBot/poll-thread.py')

if (poll_started == 'no'):

    # start poll (by CRON)
    Thread(target=start_poll).start()

    # set poll started to yes
    f = open('/home/pi/articleBot/poll_started.txt', 'w')
    f.write('yes')  # python will convert \n to os.linesep
    f.close()
