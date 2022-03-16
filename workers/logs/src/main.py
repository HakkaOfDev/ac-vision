import socket
import re
import socketio
from datetime import datetime

sio = socketio.Client()
sio.connect('http://server:6969')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 514))
REGEX = r"(?P<onu>ONU\([0-9],[0-9]*\)) (?P<status>(DE)?ACTIVATION) \((?:Reason:|SN:)(\s)?(?P<reason>(.)*)\)"

if __name__ == '__main__':
    while True:
        data,addr = s.recvfrom(4048)
        data = data.decode('utf-8')
        matches = re.search(REGEX, data)
        print(data)
        if matches:
            onu_info = {"onuid": matches.group("onu").split(',')[:1],
                        "status": matches.group("status"),
                        "reason": matches.group("reason"),
                        "date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
            print(onu_info)
            sio.emit('ONU_INFO', onu_info)