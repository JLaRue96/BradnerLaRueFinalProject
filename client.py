import socket
import json
import sys
import time
import pickle

def setUpConnection(ip, port):
    """establish a tcp connection to the game server"""
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((remote_ip , port))
    print("client connected to game server")

    return clientSocket

def recvDict(clientSocket):
    """wait for a dictionary to come from the server"""
    newData = False
    while not newData:
        dataIn = clientSocket.recv(4096)
        if dataIn:
            newData = True

    dictIn = pickle.loads(dataIn)
    return dictIn

def getOption(dictIn):
    """present options to user, have him selct among those"""

    if not dictIn["options"]:
        print(dictIn["message"])
        return {}

    numOptions = len(dictIn["options"])

    print(dictIn["message"])

    print("Select from the following options: ")
    for i in range(numOptions):
        print(str(i) + ": " + dictIn["options"][i])

    selectionNum = input("option number: ")
    selection = dictIn["options"][selectionNum]

    returnDict = {"selection" : selection}

    print("you chose " + returnDict["selection"])

    return returnDict

def sendDict(returnDict, clientSocket):
    """send a dictionary to the server"""
    dataOut = pickle.dumps(returnDict, -1)
    clientSocket.sendall(dataOut)

def getAmount():
    """Find out how much the user wants to bet"""
    wager = input("enter wager amount: ")
    return wager

portOffset = input("enter player number: ") - 1;
port = 8888 + portOffset;
remote_ip = "127.0.0.1"

clientSocket = setUpConnection(remote_ip, port)

playing = True

while (playing):
    dictIn = recvDict(clientSocket)

    returnDict = getOption(dictIn)

    if returnDict:

        if (returnDict["selection"] == "quit"):
            playing = False
        elif (returnDict["selection"] == "bet" or returnDict["selection"] == "raise"):
            returnDict["amount"] = getAmount()

    sendDict(returnDict, clientSocket)