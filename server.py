import socket
import json
import sys
import time

class HoldEmServer:

    def __init__(self):
        self.client_list = []
        self.HOST = ''
        self.PORT = 8888
        self.num_players = 2
        self.connections = {}
        self.addresses = {}

        try:
            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("socket created")
        except socket.error:
            print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
            sys.exit();

        try:
            self.serversocket.bind((self.HOST, self.PORT))
        except socket.error:
            print("bind failed")

    def acceptClients(self):
        #listen for 2 players
        self.serversocket.listen(self.num_players)
        print("socket listening for " + str(self.num_players) + " players to connect")
        for i in range(2):
            conn, addr = self.serversocket.accept()
            print("connection " + str(i + 1) + " of " + str(self.num_players) + " established.")

    def collectCommand(stateMsg, options, self):
        data = {"message" : stateMsg, "options" : options}

    def unpack_data(data, self):
        new_dict = json.loads(data)
        return new_dict

    def pack_dict(dict, self):
        data = json.dumps(dict)

myServer = HoldEmServer()
myServer.acceptClients()
time.sleep(5)