import socket
import re
import socketio
import asyncio
import websockets
import json

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

async def listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 514))
    print('Start')
    REGEX = r"(?P<onu>ONU\([0-9],[0-9]*\)) (?P<status>(DE)?ACTIVATION) \((Reason: )?(?P<reason>[\w\s\(\)]*)\)"
    while True:
        print('Listening...')
        data,addr = s.recvfrom(4048)
        data = data.decode('utf-8')
        print(data)
        matches = re.search(REGEX, data)
        if matches:
            onu_info = {"onu": matches.group("onu"),
                        "status": matches.group("status"),
                        "reason": matches.group("reason")}
            print(onu_info)
            await websockets.send(json.dumps(onu_info))
        else:
            print('No matches found')

start_server = websockets.serve(listen, "0.0.0.0", 6969)



if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(start_server)
    print("Server websocket have boot")
    asyncio.get_event_loop().run_forever()
