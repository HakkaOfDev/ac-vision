import socket
import re
import socketio
import eventlet
import threading
import asyncio

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 514))
REGEX = r"(?P<onu>ONU\([0-9],[0-9]*\)) (?P<status>(DE)?ACTIVATION) \((Reason: )?(?P<reason>[\w\s\(\)]*)\)"

def listen():
    while True:
        data,addr = s.recvfrom(4048)
        data = data.decode('utf-8')
        matches = re.search(REGEX, data)
        print(data)
        if matches:
            onu_info = {"onu": matches.group("onu"),
                        "status": matches.group("status"),
                        "reason": matches.group("reason")}
            sio.emit('ONU', onu_info)

@sio.on('READY')
def ready(sid):
    print('Ready to listening..')
    asyncio.create_task(listen())

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 6969)), app)