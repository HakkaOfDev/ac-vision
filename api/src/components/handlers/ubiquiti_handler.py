import requests

from ..tools.time_utils import format_uptime


class UbiquitiWorkflow:

    def __init__(self, id, auth_token):
        self.id = id
        self.auth_token = auth_token

    def get_olt(self):
        response = requests.get('https://unms/nms/api/v2.1/devices/olts/' + self.id,
                                headers={'Accept': 'application/json',
                                         'x-auth-token': self.auth_token}, verify=False)
        olt = response.json()
        olt_obj = {
            "ipAddress": olt["ipAddress"],
            "status": olt["overview"]["status"],
            "uptime": format_uptime(olt["overview"]["uptime"], 4),
            "temperature": olt["overview"]["temperature"],
            "macAddress": olt["identification"]["mac"],
            "displayName": olt["identification"]["displayName"],
            "site": {
                "id": olt["identification"]["site"]["id"],
                "name": olt["identification"]["site"]["name"],
                "status": olt["identification"]["site"]["status"],
            },
            "interfaces": []
        }
        for int in olt["interfaces"]:
            olt_obj["interfaces"].append(
                {
                    "position": int["identification"]["position"],
                    "type": int["identification"]["type"],
                    "displayName": int["identification"]["displayName"],
                    "macAddress": int["identification"]["mac"],
                    "description": int["identification"]["description"],
                    "status": int["status"]["status"],
                    "speed": int["status"]["description"],
                }
            )
        return olt_obj

    def get_onus(self):
        response = requests.get('https://unms/nms/api/v2.1/devices/onus?parentId=' + self.id,
                                headers={'Accept': 'application/json',
                                         'x-auth-token': self.auth_token}, verify=False)
        onus_list = []
        for onu in response.json():
            onus_list.append(
                {
                    "id": onu["onu"]["id"],
                    "gponPort": onu["onu"]["port"],
                    "profile": onu["onu"]["profile"],
                    "rxPower": round(onu["onu"]["receivePower"], 2),
                    "ipAddress": onu["ipAddress"],
                    "status": onu["overview"]["status"],
                    "uptime": format_uptime(onu["overview"]["uptime"], 4),
                    "distance": onu["overview"]["distance"],
                    "macAddress": onu["identification"]["mac"],
                    "displayName": onu["identification"]["displayName"],
                    "serialNumber": onu["identification"]["serialNumber"],
                    "parent": self.id,
                    "site": {
                        "id": onu["identification"]["site"]["id"],
                        "name": onu["identification"]["site"]["name"],
                        "status": onu["identification"]["site"]["status"],
                    }
                }
            )
        return onus_list
