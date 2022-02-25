import socket
import logging
import re
import json
import threading
from websocket_server import WebsocketServer
import websockets
import asyncio

'''
def register_new_client(client, server):
    print(f"New client added ! {client['address'][0]} on port {client['address'][1]}")

def on_message_received(client,server,message):
    print(message)

server = WebsocketServer(host='0.0.0.0', port=6969, loglevel=logging.INFO)
server.set_fn_new_client(register_new_client)
server.set_fn_message_received(on_message_received)
'''
async def listen(websocket, path):
    print("Start listening..")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 514))
    REGEX = r"(?P<onu>ONU\([0-9],[0-9]*\)) (?P<status>(DE)?ACTIVATION) \(Reason: (?P<reason>[\w\s\(\)]*)\)"
    while True:
        print('listening...')
        data = s.recv(4048)
        data = data.decode('utf-8')
        print(data)
        matches = re.search(REGEX, data)
        if matches:
            onu_info = {"onu": matches.group("onu"),
                        "status": matches.group("status"),
                        "reason": matches.group("reason")}
            print(onu_info)
            await websocket.send(json.dumps(onu_info))
            #server.send_message_to_all(json.dumps(onu_info))
        else:
            await websocket.send(json.dumps({"message": "Aucune données, matches not found"}))


if __name__ == '__main__':
    print("Running.")
    start_server = websockets.serve(listen, "0.0.0.0", 6969)
    asyncio.get_event_loop().run_until_complete(start_server)   
    asyncio.get_event_loop().run_forever()
    #server.run_forever(threaded=True)
    #listen()