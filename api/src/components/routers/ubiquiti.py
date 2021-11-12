from fastapi import APIRouter, Depends
import requests

from ..tools.config.config_loader import config
from ..tools.time_utils import formatUptime
from ..dependencies import get_token_header

router = APIRouter(prefix="/api/v1.0/ressources/ubiquiti",
                   tags=["ubiquiti"],
                   responses={404: {"description": "Not found"}},
                   )


@router.get("/olt")
async def olt():
    response = requests.get('https://unms/nms/api/v2.1/devices/olts/' + config['id_ubiquiti'],
                            headers={'Accept': 'application/json',
                                     'x-auth-token': config['api_token']}, verify=False)
    olt = response.json()
    json = {
        "id": config['id_ubiquiti'],
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

@router.get("/onus")
async def onus():
    response = requests.get('https://unms/nms/api/v2.1/devices/onus?parentId=' + config['id_ubiquiti'],
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
                "parent": config['id_ubiquiti'],
                "site": {
                    "id": onu["identification"]["site"]["id"],
                    "name": onu["identification"]["site"]["name"],
                    "status": onu["identification"]["site"]["status"],
                }
            }
        )
    return onusList


