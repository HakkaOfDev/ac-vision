from fastapi import APIRouter, Depends
import requests
from ..dependencies import get_current_user
from ..tools.snmp import snmp_utils
from ..tools.time_utils import formatUptime

router = APIRouter(prefix="/api/v1.0/ressources/dasan",
                   tags=["dasan"],
                   dependencies=[Depends(get_current_user)],
                   responses={404: {"description": "Not found"}}
                   )


@router.get("/olt")
async def olt():
    dasan = snmp_utils.SnmpUtils("10.59.10.20")
    olt = {
        "ip": "10.59.10.20",
        "status": ("disconnected", "active")[dasan.isConnected()],
        "uptime": formatUptime(int(dasan.get(dasan.oids["system"]["uptime"]))),
        "temperature": dasan.get(dasan.oids["system"]["temperature"]),
        "mac": convert_mac(str(dasan.get(dasan.oids["system"]["mac_address"]))),
        "displayName": dasan.get(dasan.oids["system"]["name"]),
        "site": {
            "name": "IUT CHALONS"
        }
            }
    return olt

@router.get("/onus")
async def onus():
    dasan = snmp_utils.SnmpUtils("10.59.10.20")

    onus = []
    rxPower = list(dasan.bulk(dasan.oids["olt_dasan"]["onu"]["rx_power"]).values())
    mac_address = list(dasan.bulk(dasan.oids["olt_dasan"]["onu"]["mac_address"]).values())
    distance = list(dasan.bulk(dasan.oids["olt_dasan"]["onu"]["distance"]).values())
    profile = list(dasan.bulk(dasan.oids["olt_dasan"]["onu"]["profile"]).values())
    name = list(dasan.bulk(dasan.oids["olt_dasan"]["onu"]["name"]).values())
    status = list(dasan.bulk(dasan.oids["olt_dasan"]["onu"]["status"]).values())
    uptime = list(dasan.bulk(dasan.oids["olt_dasan"]["onu"]["uptime"]).values())
    ip = list(dasan.bulk(dasan.oids["olt_dasan"]["onu"]["mac_address"]).keys())
    for i in range(8):
        onus.append({
            "rxPower": (int(rxPower[i])/10),
            "port": 1,
            "mac": convert_mac(mac_address[i], True),
            "distance": distance[i],
            "profile": profile[i],
            "displayName": name[i],
            "status": ("active", "disconnected")[status[i] == 2],
            "uptime": formatUptime(int(uptime[i])),
            "ip": ip[i][37:],
            "site": {
                "name": "IUT CHALONS"
            }
        })
    return onus


def convert_mac(mac, change=False):
    if change:
        mac = hex(int(mac, 16)-1)[2:]
    else:
        mac = mac[2:]
    return mac[:2] + ":" + ":".join([mac[i] + mac[i+1] for i in range(2, 12, 2)])