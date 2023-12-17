# Author: Andrew McConnell

import argparse
import paramiko
from getpass import getpass
from grep import Grep
import sys

argp = argparse.ArgumentParser(prog="fssh.py",
                               description="FortiManager/FortiAnalyzer ssh session broker that allows you to grep output")

argp.add_argument("-i", type=str, metavar="SECRETKEY", help="ssh -i flag, takes in a private key associated with the target server")
argp.add_argument("user@serv", type=str, metavar="USER@SERVER", help="Log into server as user, if no secret key supplied, then a password will be promtped")

args = argp.parse_args()

if __name__ == "__main__":

    if type(args) == str:
        print(args)
        sys.exit(1)
    
    keypath = ""

    try:
        keypath = args.i
    except:
        ## grab username and password prompt
        pass