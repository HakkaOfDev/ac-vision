import json
from types import SimpleNamespace

from pysnmp.entity.engine import SnmpEngine
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.hlapi import nextCmd, CommunityData, UdpTransportTarget, ContextData
from pysnmp.smi.rfc1902 import ObjectType, ObjectIdentity

PATH_TO_LIST = "OIDS.json"

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

    def defineOIDsList(self):
        with open(PATH_TO_LIST, ) as file:
            self.oids = json.loads(file.read().replace('\n', ''), object_hook=lambda d: SimpleNamespace(**d))

    def get(self, oid):
        return list(self.walk(oid, 1).values())[-1]

    def getByID(self, oid, id):
        return list(self.walk(oid + "." + str(id), 1).values())[-1]

    def isConnected(self):
        try:
            self.find("1.3.6.1")
            return True
        except:
            return False

    def bulk(self, *oids_list):
        errorIndication, errorStatus, errorIndex, snmpDataTable = cmdgen.CommandGenerator().bulkCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget((self.host, self.port)),
            0, 25,
            *oids_list,
        )

        if not errorIndication and not errorStatus:
            results = {}
            for snmpDataTableRow in snmpDataTable:
                for name, val in snmpDataTableRow:
                    results[str(name)] = str(snmpDataTableRow[0]).split(" = ")[1]

            return results
        return None

    def set(self, oid, value):
        errorIndication, errorStatus, errorIndex, snmpData = cmdgen.CommandGenerator().setCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget((self.host, self.port)),
            (ObjectType(ObjectIdentity(oid)), value)
        )
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and snmpData[int(errorIndex) - 1][0] or '?'
            ))

    def walk(self, oid, n=0, dotPrefix=False):
        if dotPrefix:
            oid = "." + oid

        results = {}
        i = 0
        for (errorIndication, errorStatus, errorIndex, snmpData) in nextCmd(SnmpEngine(),
                                                                            CommunityData(self.community),
                                                                            UdpTransportTarget((self.host, self.port)),
                                                                            ContextData(),
                                                                            ObjectType(ObjectIdentity(oid))):
            if not errorIndication and not errorStatus:
                for data in snmpData:
                    if n == 0:
                        results[str(data[0].__str__).split("payload [")[1][:-4]] = \
                            str(data[1].__str__).split("payload [")[1][:-3]
                    elif n != i:
                        results[str(data[0].__str__).split("payload [")[1][:-4]] = \
                            str(data[1].__str__).split("payload [")[1][:-3]
                        i += 1
                    else:
                        return results
        return None