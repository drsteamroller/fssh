# Author: Andrew McConnell

import argparse
import paramiko
from getpass import getpass
from grep import Grep
from bucket_tracker import BuckeTracker
import sys


argp = argparse.ArgumentParser(prog="fssh.py",
                               description="FortiManager/FortiAnalyzer ssh session broker that allows you to grep output")

argp.add_argument("-i", type=str, metavar="SECRETKEY", help="ssh -i flag, takes in a private key associated with the target server")
argp.add_argument("-p", type=int, metavar="PORT", default=22, help="SSH port on target server, default 22")
argp.add_argument("-aa", "--auto-add-key-policy", action="store_true", help="If the key of the target server is unknown, either add it or reject it.")
argp.add_argument("user@serv", type=str, metavar="USER@SERVER", help="Log into server as user, if no secret key supplied, then a password will be promtped")


args = argp.parse_args()

if __name__ == "__main__":

    if type(args) == str:
        print(args)
        sys.exit(1)
    
    keypath = ""
    keyAddPolicy = paramiko.RejectPolicy()
    password = ""

    u_s = vars(args)['user@serv'].split("@")
    username = u_s[0]
    server = u_s[1]
    port = args.p

    if args.i:
        keypath = args.i
    else:
        password = getpass()
    
    if args.auto_add_key_policy:
        keyAddPolicy = paramiko.AutoAddPolicy()
    
    # Setup client-side connection
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(keyAddPolicy)
    client.load_system_host_keys()

     # Connect to server
    
    if keypath:
        try:
            client.connect(hostname=server, port=port, username=username, key_filename=keypath)
        except Exception as e:
            print(f"Something went wrong when connecting with a private key\n\t{e}")
            sys.exit(2)
        else:
            print("\nConnected!\n")

    else:
        try:
            client.connect(hostname=server, username=username, password=password, port=port)
        except Exception as e:
            print(f"Something went wrong when connecting with username/password\n\t{e}")
            sys.exit(2)
        else:
            print("\nConnected!\n")

    stdin, stdout, stderr = client.exec_command("")

    print(stdout.read().decode(), end="")
    userIn = input()
    bkt = BuckeTracker(client)
    grep = Grep()

    while "quit" not in userIn:
        
        grepCommand = ""

        # Check for '| grep' and remove it before sending command, set grep flag
        if "| grep" in userIn:
            split = userIn.split("|")
            userIn = split[0].strip()
            grepCommand = split[1].strip()

        if "config" in userIn:
            bkt.storeBucketLevel(userIn[0:-1])
            print(bkt.bkt)
            stdin, stdout, stderr = client.exec_command(userIn)
        elif len(userIn) and (userIn in "show" or userIn in "get"):
            stdin, stdout, stderr = bkt.show_or_get(userIn)
        else:
            stdin, stdout, stderr = client.exec_command(userIn)
            if stderr:
                print(stderr.read().decode(), end="")
        
        ## if grep flag set, instead of print, grep and returned filtered output 
        print(f"\n{stdout.read().decode()}", end="")

        userIn = input()

    client.close()