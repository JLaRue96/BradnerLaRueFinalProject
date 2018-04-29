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

testDict = {"cmd" : "bet", "value" : 25}
print(testDict["cmd"])

pickledObj = pickle.dumps(testDict)

clientSocket.sendall(pickledObj)

dictIn = pickle.loads(clientSocket.recv(4096))

print(dictIn["message"])