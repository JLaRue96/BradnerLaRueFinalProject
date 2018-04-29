import socket
import sys
import time
import cPickle as pickle
import json

class HoldEmServer:

    def __init__(self):
        self.client_list = []
        self.HOST = ''
        self.PORT = 8888
        self.num_players = 1
        self.connections = {}
        self.addresses = {}
        self.sockets = {}
        self.conn = {}
        self.addr = {}

        try:
            for i in range(self.num_players):
                self.sockets[i] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("socket created")
                self.sockets[i].bind((self.HOST, self.PORT + i))
        except socket.error:
            print("failed to create socket")
            sys.exit();

    def shutDown(self):
        for i in range(self.num_players):
            self.sockets[i].close()

    def acceptClients(self):
        #listen for 2 players
        for i in range(self.num_players):
            self.sockets[i].listen(1)
            self.conn[i], self.addr[i] = self.sockets[i].accept()
            print("connection " + str(i + 1) + " of " + str(self.num_players) + " established.")

    def collectCommand(self, stateMsg, options, playerNum):
        data = {"message" : stateMsg, "options" : options}

        self.sendDict(data, playerNum)

        dictIn = self.getResponse(playerNum)
        
        print("client selection: " + dictIn["selection"])

        return dictIn

    def getResponse(self, playerNum):
        newData = False
        while not newData:
            dataIn = self.conn[playerNum].recv(4096)
            if dataIn:
                newData = True

        dictIn = pickle.loads(dataIn)

        return dictIn

    def sendDict(self, dict, playerNum):
        pickledObj = pickle.dumps(dict, -1)
        self.conn[playerNum].sendall(pickledObj)
        return True

    def unpack_data(self, data):
        new_dict = pickle.loads(data)
        return new_dict

    def pack_dict(self, dict):
        data = pickle.dumps(dict)

myServer = HoldEmServer()
myServer.acceptClients()
#test sending of data here
myServer.collectCommand("test game state", ["bet", "fold"], 0)   
time.sleep(5)
myServer.shutDown()