def convert_mac(mac, change=False):
    if change:
        mac = hex(int(mac, 16) - 1)[2:]
    else:
        mac = mac[2:]
    return mac[:2] + ":" + ":".join([mac[i] + mac[i + 1] for i in range(2, 12, 2)])
