import socket
import requests
import logging
import re
import json
from websocket_server import WebsocketServer


def register_new_client(client, server):
    print("New client added !")

server = WebsocketServer(host='0.0.0.0', port=6969, loglevel=logging.INFO)
server.set_fn_new_client(register_new_client)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", 514))

REGEX = r"(?P<onu>ONU\([0-9],[0-9]*\)) (?P<status>(DE)?ACTIVATION) \(Reason: (?P<reason>[\w\s\(\)]*)\)"

def listen():
    while True:
        data = s.recv(4048)
        data = data.decode('utf-8')
        print(data)
        matches = re.search(REGEX, data)
        if matches:
            requests.get('http://ac-vision/api/v1.0/ressources/map/update')
            print('Cache updated')
            onu_info = {"onu": matches.group("onu"),
                        "status": matches.group("status"),
                        "reason": matches.group("reason")}
            print(onu_info)
            server.send_message_to_all(json.dumps(onu_info))

if __name__ == '__main__':
    server.run_forever(threaded=True)
    listen()