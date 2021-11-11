import time

import requests
import urllib3
from flask import Flask, render_template, jsonify

app = Flask(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api_token = "a60d1c57-576e-43ba-b05f-ec116ec20e85"
id_ubiquiti = "c4a201ea-ffba-4c25-8d71-161c06917464"


@app.route('/')
def index():
    return render_template('templates/index.html')


@app.route('/workflow')
def workflow():
    return render_template('templates/workflow.html')


@app.route('/devices')
def devices():
    onus_ubiquiti = getOnusDetails()
    olt_ubiquiti = getOltDetails()
    return render_template('templates/devices.html', onus_ubiquiti=onus_ubiquiti, olt_ubiquiti=olt_ubiquiti)


@app.route('/api/onus')
def onus():
    onusList = getOnusDetails()
    return jsonify(onusList)


@app.route('/api/olts')
def olts():
    olt = getOltDetails()
    return jsonify(olt)


def getOltDetails():
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


def getOnusDetails():
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


def formatUptime(sec):
    return ("None", time.strftime("%wD, %Hh, %Mm, %Ss", time.gmtime(sec)))[sec is not None]


if __name__ == '__main__':
    app.run()
