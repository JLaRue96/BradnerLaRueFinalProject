import socket
import json
import sys
import time
import pickle

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

portOffset = input("enter player number: ") - 1;

remote_ip = "127.0.0.1"
port = 8888

clientSocket.connect((remote_ip , port + portOffset))
print("clent connected to game server")

newData = False

while not newData:
    dataIn = clientSocket.recv(4096)
    if dataIn:
        newData = True

dictIn = pickle.loads(dataIn)

numOptions = len(dictIn["options"])

print("Select from the following options: ")
for i in range(numOptions):
    print(str(i) + ": " + dictIn["options"][i])

selection = input("option number: ")