import requests
from flask import Flask, render_template

app = Flask(__name__)

api_token = "a60d1c57-576e-43ba-b05f-ec116ec20e85"
id_ubiquiti = "c4a201ea-ffba-4c25-8d71-161c06917464"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/workflow')
def workflow():
    response = requests.get('https://unms/nms/api/v2.1/devices/onus?parentId=' + id_ubiquiti,
                            headers={'Accept': 'application/json',
                                     'x-auth-token': 'a60d1c57-576e-43ba-b05f-ec116ec20e85'}, verify=False)
    onus = []
    for onu in response.json():
        onus.append(
            {
                "id": onu["onu"]["id"],
                "port": onu["onu"]["port"],
                "profile": onu["onu"]["profile"],
                "rxPower": onu["onu"]["receivePower"],
                "ip": onu["ipAddress"],
                "status": onu["overview"]["status"],
                "uptime": onu["overview"]["uptime"],
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

    nodes = []
    edges = []

    # FAI
    nodes.append(
        {
            "id": 0,
            "label": "FAI",
            "shape": "image",
            "image": "https://www.wifi-france.com/images/stories/virtuemart/product/ER-12_Top_Angle_14df3455-0ce0-47ff-a689-9f32a9e3e1c3_grande.png",
            "font": {
                "strokeWidth": 3
            }
        }
    )

    # OLTs
    nodes.append(
        {
            "id": 1,
            "label": "OLT Dasan",
            "shape": "image",
            "image": "https://www.wifi-france.com/images/stories/virtuemart/product/ER-12_Top_Angle_14df3455-0ce0-47ff-a689-9f32a9e3e1c3_grande.png",
            "font": {
                "strokeWidth": 3
            }
        }
    )

    nodes.append(
        {
            "id": 2,
            "label": "OLT Ubiquiti",
            "shape": "image",
            "image": "https://www.wifi-france.com/images/stories/virtuemart/product/ER-12_Top_Angle_14df3455-0ce0-47ff-a689-9f32a9e3e1c3_grande.png",
            "font": {
                "strokeWidth": 3
            }
        }
    )

    # Link FAI OLTs
    edges.append(
        {
            "from": 0,
            "to": 1,
            "color": "rgba(110, 231, 183, 1)",
            "length": 25,
        }
    )

    edges.append(
        {
            "from": 0,
            "to": 2,
            "color": "rgba(110, 231, 183, 1)",
            "length": 25,
        }
    )

    # ONUs
    i = 10
    for node in onus:
        nodes.append({
            "id": i,
            "label": node["displayName"],
            "shape": "image",
            "image": "https://www.wifi-france.com/images/stories/virtuemart/product/ER-12_Top_Angle_14df3455-0ce0-47ff-a689-9f32a9e3e1c3_grande.png",
            "font": {
                "strokeWidth": 3
            }
        })
        edges.append({
            "from": 2,
            "to": i,
            "color": ("rgba(252, 165, 165, 1)", "rgba(110, 231, 183, 1)")[node["status"] == "active"],
            "length": 350,
            "label": str(node["rxPower"]),
            "title": "Status: <span class='text-red-300'>" + node["status"] + "</span>\\nRxPower: <span class='text-red-300'>" + str(node["rxPower"]) + "</span>"
        }
        )
        i += 1
    print(edges)
    return render_template('workflow.html', nodes=nodes, edges=edges)


@app.route('/devices')
def devices():
    return render_template('devices.html')


if __name__ == '__main__':
    app.run()
