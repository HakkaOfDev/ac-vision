#from ast import match_case
import socket
from websocket_server import WebsocketServer
import logging
import re

from components.redis.cache_updates import update_cache
import time

def register_new_client(client, server):
    print("New client added !")

server = WebsocketServer(host='0.0.0.0', port=6969, loglevel=logging.INFO)
server.set_fn_new_client(register_new_client)


@sio.event
async def connect(sid, environ):
    print('connect ', sid)

    

REGEX = r"(?P<onu>ONU\([0-9],[0-9]*\)) (?P<status>(DE)?ACTIVATION) \(Reason: (?P<reason>[\w\s\(\)]*)\)"
def listener():
    port = 514
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", port))
    while True:
        data, addr = s.recvfrom(4048)
        data = data.decode('utf-8')
        print(data)
        matches = re.search(REGEX, data)
        if matches:
            update_cache()
            print('cache updated')
            onu_info = {"onu": matches.group("onu"),
                        "status": matches.group("status"),
                        "reason": matches.group("reason")}
            send_message_to_all(onu_info)
