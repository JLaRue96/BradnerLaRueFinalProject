import socket

import json

print("\nFill out the following fields:")
HOST = input("\nNet Send Server Public IP: ")
PORT = int(input("\nNet Send Server Port: "))

try:
    s = socket(AF_INET,SOCK_STREAM)
    s.connect((HOST,PORT))
    print("Connected to server:",HOST,)
except IOError:
    print("\nUndefined Connection Error Encountered")
    input("Press Enter to exit, then restart the script")
    sys.exit()

#dictionary that maps phases to command options
commands = {"pre-flop" : ["check", "bet", "fold"], "round-1" : ["check", "bet", "fold"]}

def send_cmd(command):
    #serialize command (useful for once they get more complex)
    try:
        data_string = json.dumps(command)
        s.send(data_string)
        reply = s.recv(1024)
    except IOError:
        print("\nIO Error detected, exiting")

