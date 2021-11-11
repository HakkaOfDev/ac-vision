from datetime import timedelta

import requests
from flask import Flask, jsonify

from client.src.routes.main_routes import main_routes
from client.src.routes.user_routes import user_routes

app = Flask(__name__, template_folder="templates")
app.register_blueprint(main_routes)
app.register_blueprint(user_routes)


@app.route('/api/onus')
def onus():
    onusList = getUbiquitiOnusDetails()
    return jsonify(onusList)


@app.route('/api/olts')
def olts():
    olt_ubiquiti = getUbiquitiOltDetails()
    return jsonify(olt_ubiquiti)


def getUbiquitiOltDetails():
    response = requests.get('https://unms/nms/api/v2.1/devices/olts/' + id_ubiquiti,
                            headers={'Accept': 'application/json',
                                     'x-auth-token': 'a60d1c57-576e-43ba-b05f-ec116ec20e85'}, verify=False)
    olt = response.json()
    json = {
        "id": id_ubiquiti,
        "ip": olt["ipAddress"],
        "status": olt["overview"]["status"],
        "uptime": formatUptime(olt["overview"]["uptime"]),
        "temperature": olt["overview"]["temperature"],
        "mac": olt["identification"]["mac"],
        "displayName": olt["identification"]["displayName"],
        "site": {
            "id": olt["identification"]["site"]["id"],
            "name": olt["identification"]["site"]["name"],
            "status": olt["identification"]["site"]["status"],
        },
        "interfaces": []
    }
    for int in olt["interfaces"]:
        json["interfaces"].append(
            {
                "position": int["identification"]["position"],
                "type": int["identification"]["type"],
                "displayName": int["identification"]["displayName"],
                "mac": int["identification"]["mac"],
                "description": int["identification"]["description"],
                "status": int["status"]["status"],
                "speed": int["status"]["description"],
            }
        )
    return json


def getUbiquitiOnusDetails():
    response = requests.get('https://unms/nms/api/v2.1/devices/onus?parentId=' + id_ubiquiti,
                            headers={'Accept': 'application/json',
                                     'x-auth-token': 'a60d1c57-576e-43ba-b05f-ec116ec20e85'}, verify=False)
    onusList = []
    for onu in response.json():
        onusList.append(
            {
                "id": onu["onu"]["id"],
                "port": onu["onu"]["port"],
                "profile": onu["onu"]["profile"],
                "rxPower": round(onu["onu"]["receivePower"], 2),
                "ip": onu["ipAddress"],
                "status": onu["overview"]["status"],
                "uptime": formatUptime(onu["overview"]["uptime"]),
                "distance": onu["overview"]["distance"],
                "mac": onu["identification"]["mac"],
                "displayName": onu["identification"]["displayName"],
                "serialNumber": onu["identification"]["serialNumber"],
                "parent": id_ubiquiti,
                "site": {
                    "id": onu["identification"]["site"]["id"],
                    "name": onu["identification"]["site"]["name"],
                    "status": onu["identification"]["site"]["status"],
                }
            }
        )
    return onusList


def formatUptime(s):
    if s is not None:
        x = str(timedelta(seconds=s)).split(':')
        s = f"{x[0]}h, {x[1]}m, {x[2]}s"
        return s


if __name__ == '__main__':
    app.run()
