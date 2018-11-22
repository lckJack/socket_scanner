#!/usr/bin/env python3
import sys
import subprocess
import socket
import argparse

import time
from colored import fg, bg, attr
from pynput import keyboard
   
    

def on_press(key):
    try: k = key.char
    except: k = key.name
    if key == keyboard.Key.esc: return False
    if k in ['space']:
        current = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
        percentage = round((100*c_port) / (int(f_port)-int(s_port)), 2)
        remaining = time.strftime("%H:%M:%S", time.gmtime(timeout*(f_port-1)))

        print(fg(108)+" Stats: "+current+" time elapsed. Remaining time: "+remaining+". Current port:",c_port,"About",percentage,"% done. "+attr('reset'))
        return False

def main (argv):

    global start_time
    global s_port
    global f_port
    global timeout
    global target
    global show

    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--port', help="just one port or a full range. Default: 1-1000" ,required=False)
    parser.add_argument('-s','--show', help="won't show closed if not specified.", required=False, action="store_true")
    parser.add_argument('-t','--timeout', help="connection timeout. Default: 5", required=False)
    parser.add_argument('-i','--ip', help="target IP.", required=True)
    args = parser.parse_args()
    target = args.ip
    ip_range= args.port
    timeout= args.timeout

    if( args.timeout ):
        timeout = int(args.timeout)
    else:
        timeout = 5


    if( args.show ):
        show = 1
    else:
        show = 0

    if( ip_range ):
        if( "-" in ip_range ):
            ip_range = ip_range.split("-")
            s_port = int(ip_range[0])
            f_port = int(ip_range[1])+1

        elif( int(ip_range) ):
            s_port = int(ip_range)
            f_port = int(ip_range)+1

        else:
            s_port = 1
            f_port = 1001
    
    else:
            s_port = 1
            f_port = 1001

    start_time = time.time()
    target = target

    code()


def code():

    global c_port #current

    lis = keyboard.Listener(on_press=on_press)    

    print("")
    targetIP = socket.gethostbyname(target)

    color_reset = attr('reset')

    print("Scanning remote host: ", targetIP, "\n")

    
    try:

        for port in range(s_port,f_port):  

            c_port = port
            
            if not lis.is_alive():
                del lis
                lis = keyboard.Listener(on_press=on_press)
                lis.start()
            

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((targetIP, port))
            if result == 0:
                print("    Port["+str(port)+"]:  "+fg(82)+"Open"+color_reset)
            else:
                if(  show == 1 ):
                    print("    Port["+str(port)+"]:  "+fg(196)+"Closed"+color_reset)

            sock.close()

    except socket.error:
        print("Error. Check that IP...")
        sys.exit()
   

    finish = time.time()

    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(finish - start_time))


    print('\nElapsed Time: ', elapsed_time)
    print("")


if __name__ == "__main__":
    main(sys.argv[1:])

