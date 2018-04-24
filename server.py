import socket

import json

latest_command = ""

def unpack_cmd(data):
    latest_command = json.loads(data)

