#!/usr/bin/env python3

import sys
import subprocess
import socket
import argparse

import time
from colored import fg, bg, attr


def main (argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--port', help="just one port or a full range. Default: 1-1000" ,required=False)
    parser.add_argument('-s','--show', help="won't show closed if not specified.", required=False, action="store_true")
    parser.add_argument('-i','--ip', help="target IP.", required=True)
    args = parser.parse_args()
    target = args.ip
    ip_range= args.port

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

    code(target, s_port,f_port,show)


def code(target, s_port,f_port, show):
    print("")
    target = target
    s_port = s_port
    f_port = f_port
    targetIP = socket.gethostbyname(target)
    color_reset = attr('reset')
    start = time.time()

    print("Scanning remote host: ", targetIP, "\n")    

    try:
        for port in range(s_port,f_port):  
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(finish - start))

    print('\nElapsed Time: ', elapsed_time)
    print("")


if __name__ == "__main__":
    main(sys.argv[1:])
