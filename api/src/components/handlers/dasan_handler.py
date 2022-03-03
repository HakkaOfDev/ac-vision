from re import S
from fastapi import Depends
from flask import session
from ..tools.snmp.oids import OIDS
from ..tools.snmp.snmp_utils import SnmpUtils
from ..tools.time_utils import format_uptime, format_dasan_olt_uptime
from ..sql_app import fonction
from ..sql_app.database import SessionLocal

class DasanWorkflow:

    def __init__(self, ip):
        self.ip = ip

    def get_olt(self):
        olt = SnmpUtils(self.ip)
        return {
            "model": "olt-dasan",
            "ipAddress": self.ip,
            "status": ("inactive", "active")[olt.is_online()],
            "uptime": (format_dasan_olt_uptime(olt.get(OIDS.SYSTEM_UPTIME.value)), '')[
                olt.get(OIDS.SYSTEM_UPTIME.value) is None],
            "temperature": olt.get(OIDS.SYSTEM_TEMPERATURE.value),
            "macAddress": olt.get(OIDS.SYSTEM_MAC.value).replace(' ', ':')[1:-2].upper(),
            "displayName": olt.get(OIDS.SYSTEM_NAME.value)[1:-1],
            "site": "IUT CHALONS"
        }

    def get_onus(self):
        session = SessionLocal()
        olt = SnmpUtils(self.ip)
        onus_table = olt.get_table(OIDS.ONU_TABLE.value)
        onus_table.pop(-1)
        ips = olt.bulk(OIDS.ONU_MAC.value)
        onus = []
        for onu in onus_table:
            if int(onu.get('sleGponOnuInactiveTime').split(' ')[0]) < 604800:  # equivalent to 7 days
                onu_obj = {
                    "onuId": (int(onu.get('sleGponOnuId'))),
                    "model": "onu-dasan",
                    "rxPower": (int(onu.get('sleGponOnuRxPower').split(' ')[0]) / 10, '')[
                        onu.get('sleGponOnuRxPower') is None],
                    "gponPort": onu.get('index').split('.')[0],
                    "macAddress": onu.get('sleGponOnuHwAddress').replace(' ', ':')[:-1],
                    "distance": (onu.get('sleGponOnuDistance').split(' ')[0], '')[onu.get('sleGponOnuRxPower') is None],
                    "profile": onu.get('sleGponOnuProfile'),
                    "displayName": fonction.get_onusd(session, int(onu.get('sleGponOnuId'))),
                    "serialNumber": onu.get('sleGponOnuSerial'),
                    "status": onu.get('sleGponOnuStatus'),
                    "uptime": (format_uptime(int(onu.get('sleGponOnuLinkUpTime').split(' ')[0]), 4), '')[
                        onu.get('sleGponOnuLinkUpTime') is None],
                    "inactiveTime": (format_uptime(int(onu.get('sleGponOnuInactiveTime').split(' ')[0]), 4), '')[onu.get('sleGponOnuLinkUpTime') is None],
                    "ipAddress": '',
                    "site": "IUT CHALONS"
                }
                for ip, mac in ips.items():
                    formatted_mac = '0x' + onu.get('sleGponOnuHwAddress').replace(' ', '').lower()
                    if mac == formatted_mac:
                        onu_obj['ipAddress'] = ip[37:]
                onus.append(onu_obj)
        return onus
