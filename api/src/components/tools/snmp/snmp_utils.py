import sys

from pysnmp import hlapi
from pysnmp.entity.engine import SnmpEngine
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.hlapi import nextCmd, CommunityData, UdpTransportTarget, ContextData
from pysnmp.smi.rfc1902 import ObjectType, ObjectIdentity

PATH_TO_LIST = {
    "system": {
        "name": "1.3.6.1.2.1.1.5",
        "uptime": "1.3.6.1.2.1.1.3",
        "mac_address": "1.3.6.1.2.1.2.2.1.6",
        "temperature": "1.3.6.1.4.1.6296.9.1.1.2.5.1.3"
    },
    "interfaces": {
        "description": "1.3.6.1.2.1.2.2.1.2",
        "speed": "1.3.6.1.2.1.2.2.1.5",
        "mac_address": "1.3.6.1.2.1.2.2.1.6"
    },
    "olt_dasan": {
        "onu": {
            "rx_power": "1.3.6.1.4.1.6296.101.23.3.1.1.16",
            "mac_address": "1.3.6.1.4.1.6296.102.6.2.6.4.1.1.4",
            "distance": "1.3.6.1.4.1.6296.101.23.3.1.1.10",
            "profile": "1.3.6.1.4.1.6296.101.23.3.1.1.8",
            "name": "1.3.6.1.4.1.6296.101.23.3.1.1.4",
            "status": "1.3.6.1.4.1.6296.101.23.3.1.1.2",
            "uptime": "1.3.6.1.4.1.6296.101.23.3.1.1.61"
        }
    }
}


class SnmpUtils:
    """
    SNMP Utils Class for walk/bulk/set more easily in python.
    @author: HakkaOfDev
    @version: 1.0.0
    """

    def __init__(self, host, port=161, community="public"):
        self.host = host
        self.port = port
        self.community = community
        self.defineOIDsList()


    def isConnected(self):
        try:
            self.get("1.3.6.1")
            return True
        except:
            return False

    def get(self, oid):
        return list(self.walk(oid, 1).values())[-1]

    def getById(self, oid, id):
        item = self.walk(oid + "." + str(id - 1), 1)  # I dunno why, but you need -1 here..
        if str(id) == list(item.keys())[-1].split('.')[-1]:
            return list(item.values())[-1]
        else:
            return None

    def defineOIDsList(self):
        self.oids = PATH_TO_LIST

    def bulk(self, *oids_list):
        errorIndication, errorStatus, errorIndex, varBindTable = cmdgen.CommandGenerator().bulkCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget((self.host, self.port)),
            0, 25,
            *oids_list,
        )

        if errorIndication:
            print(errorIndication)

        elif errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBindTable[int(errorIndex) - 1][0] or '?'
            ))

        results = {}
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                results[str(name)] = str(varBindTableRow[0]).split(" = ")[1]

        return results

    """
    Sample code from : https://www.ictshore.com/sdn/python-snmp-tutorial/
    """

    def fetch(self, handler, count):
        result = []
        for i in range(count):
            try:
                error_indication, error_status, error_index, var_binds = next(handler)
                if not error_indication and not error_status:
                    items = {}
                    for var_bind in var_binds:
                        items[str(var_bind[0])] = self.cast(var_bind[1])
                    result.append(items)
                else:
                    raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
            except StopIteration:
                break
        return result

    def cast(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            try:
                return float(value)
            except (ValueError, TypeError):
                try:
                    return str(value)
                except (ValueError, TypeError):
                    pass
        return value

    def construct_value_pairs_int(self, list_of_pairs):
        pairs = []
        for key, value in list_of_pairs.items():
            pairs.append(hlapi.ObjectType(hlapi.ObjectIdentity(key), Integer(value)))
        return pairs

    def construct_value_pairs_str(self, list_of_pairs):
        pairs = []
        for key, value in list_of_pairs.items():
            pairs.append(hlapi.ObjectType(hlapi.ObjectIdentity(key), String(value)))
        return pairs

    def set_int(self, value_pairs, engine=hlapi.SnmpEngine(),
                context=hlapi.ContextData()):
        credentials = hlapi.CommunityData('public')
        handler = hlapi.setCmd(
            engine,
            credentials,
            hlapi.UdpTransportTarget((self.host, self.port)),
            context,
            *self.construct_value_pairs_int(value_pairs)
        )
        return fetch(handler, 1)[0]

    def set_str(self, value_pairs, engine=hlapi.SnmpEngine(),
                context=hlapi.ContextData()):
        credentials = hlapi.CommunityData('public')
        handler = hlapi.setCmd(
            engine,
            credentials,
            hlapi.UdpTransportTarget((self.host, self.port)),
            context,
            *self.construct_value_pairs_str(value_pairs)
        )
        return fetch(handler, 1)[0]

    def walk(self, oid, n=0, dotPrefix=False):
        if dotPrefix:
            oid = "." + oid

        results = {}
        i = 0
        for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(SnmpEngine(),
                                                                            CommunityData(self.community),
                                                                            UdpTransportTarget((self.host, self.port)),
                                                                            ContextData(),
                                                                            ObjectType(ObjectIdentity(oid))):
            if errorIndication:
                print(errorIndication, file=sys.stderr)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'),
                      file=sys.stderr)
                break
            else:
                for varBind in varBinds:
                    if n == 0:
                        results[str(varBind[0].__str__).split("payload [")[1][:-4]] = \
                            str(varBind[1].__str__).split("payload [")[1][:-3]
                    elif n != i:
                        results[str(varBind[0].__str__).split("payload [")[1][:-4]] = \
                            str(varBind[1].__str__).split("payload [")[1][:-3]
                        i += 1
                    else:
                        return results
        return results
