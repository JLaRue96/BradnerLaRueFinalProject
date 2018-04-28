import socket
import json
import sys
import time

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

remote_ip = "127.0.0.1"
port = 8888

clientSocket.connect((remote_ip , port))