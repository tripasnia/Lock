#!/usr/bin/env python

import time
from threading import Thread

def myfunc(count):
    print "myfunc entry"
    for i in range(count):
        time.sleep(2)
        print "loop:",(i+1)

def main():
    print "main"
    t = Thread(target=myfunc, args=(10,))
    print "Starting myfunc() thread"
    t.start()
    print "main still running"
    while True:
        time.sleep(1)
        print "tick"
        time.sleep(1)
        print "tock"
        if (not t.isAlive()):
            t.join()
            print "thread stopped"
            break;

    print "Done"

if __name__=='__main__':
    main()
