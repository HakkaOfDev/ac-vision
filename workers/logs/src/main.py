import socket
import re
import json
import socketio

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 514))

if __name__ == '__main__':
    sio = socketio.Client()
    sio.connect('ws://ac-vision/ws/')
    REGEX = r"(?P<onu>ONU\([0-9],[0-9]*\)) (?P<status>(DE)?ACTIVATION) \(Reason: (?P<reason>[\w\s\(\)]*)\)"
    while True:
        data = s.recv(4048)
        data = data.decode('utf-8')
        print(data)
        matches = re.search(REGEX, data)
        if matches:
            onu_info = {"onu": matches.group("onu"),
                        "status": matches.group("status"),
                        "reason": matches.group("reason")}
            print(onu_info)
            sio.emit('ONU', json.dumps(onu_info))
        else:
            print('No matches found')