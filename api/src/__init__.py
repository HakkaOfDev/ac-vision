import socket
import re
import time

port = 514
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))

while True:
    data, addr = s.recvfrom(4048)
    data = data.decode('utf-8')
    print(data)
    REGEX = r"(?P<onu>ONU\([0-9],[0-9]*\)) (?P<status>(DE)?ACTIVATION) \(Reason: (?P<reason>[\w\s\(\)]*)\)"
    matches = re.search(REGEX, data)
    if matches:
        print(matches)
        print(matches.group("onu"))
        print(matches.group("status"))
        print(matches.group("reason"))

# print(matches.group("reason"))  (Reason: (?P<reason>[\s\w()]*)
