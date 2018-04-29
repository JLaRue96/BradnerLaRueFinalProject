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
        self.num_players = 2
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
        pickledObj = pickle.dumps(data, -1)

        self.conn[playerNum].sendall(pickledObj)

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