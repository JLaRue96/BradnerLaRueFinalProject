import socket
import json
import sys
import time
import pickle

def setUpConnection(ip, port):
    """
    Establish a tcp connection to the game server
    :param ip: IP address
    :param port: Port number
    :return: Socket of client.
    """
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((remote_ip , port))
    print("client connected to game server")

    return clientSocket

def recvDict(clientSocket):
    """
    Wait for a dictionary to come from the server
    :param clientSocket: Socket where client connects to server.
    :return: Dictionary from the server
    """
    newData = False
    while not newData:
        dataIn = clientSocket.recv(4096)
        if dataIn:
            newData = True

    dictIn = pickle.loads(dataIn)
    return dictIn

def getOption(dictIn):
    """
    User selects a given option.
    :param dictIn: Dictionary that contains options
    :return: dictionary with information regarding user input
    """

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
    """
    Sends a dictionary to the server.
    :param returnDict: Dictionary to send to server
    :param clientSocket: Socket that client is connected to
    """
    dataOut = pickle.dumps(returnDict, -1)
    clientSocket.sendall(dataOut)

def getAmount():
    """
    Find out how much the user wants to bet
    :return: integer amount that the user wants to bet.
    """
    wager = input("enter wager amount: ")
    return wager


"""
The 'main' functionality of the client script.

Sets up a connection to the server and, while playing, 
it receives and handles dictionaries sent from the server.
A return dictionary is then sent back to the server.
"""
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