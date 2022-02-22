from ast import match_case
import socket
import socketio
import re

import uvicorn
from components.redis.cache_updates import update_cache
import time


sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    print('connect ', sid)

    

REGEX = r"(?P<onu>ONU\([0-9],[0-9]*\)) (?P<status>(DE)?ACTIVATION) \(Reason: (?P<reason>[\w\s\(\)]*)\)"
def listener():
    uvicorn.run(app, host="0.0.0.0", port="6969")
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
            onu_info = {"onu": matches.group("onu"),
                        "status": matches.group("status"),
                        "reason": matches.group("reason")}
            sio.emit(onu_info)