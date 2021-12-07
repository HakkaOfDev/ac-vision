from pysnmp.entity.rfc3413.oneliner import cmdgen
from snmp_cmds import Session, SNMPTimeout


class SnmpUtils:
    """
    SNMP Utils Class for walk/bulk/get/set/table more easily in python.
    @author: HakkaOfDev
    @version: 1.0.1
    """

    def __init__(self, host: str, port: int = 161, read_community: str = "public", write_community: str = "private",
                 timeout: int = 1):
        """
        Default constructor
        :param host: IP of device
        :param port: PORT of SNMP Agent
        :param read_community: Community for read oids
        :param write_community: Community for write (set)
        :param timeout: Timeout for a request
        """
        self.host = host
        self.port = port
        self.read_community = read_community
        self.write_community = write_community
        self.timeout = timeout
        self.session = Session(ipaddress=host, port=port, read_community=read_community,
                               write_community=write_community,
                               timeout=timeout)

    def is_online(self):
        """
        Check if a device is online
        :return: boolean
        """
        try:
            self.get('1.3.6.1.2.1.1.5')
            return True
        except SNMPTimeout as exception:
            print(exception.message)
            return False

    def set(self, oid: str, value_type: str, value: str):
        """
        Set value of oid
        :param oid:
        :param value_type: can be one of i/u/t/a/o/s/x/d/b
        :param value:
        """
        self.session.set(oid=oid, value_type=value_type, value=value)

    def get(self, oid: str):
        """
        Get a specific value from an oid
        :param oid:
        :return: str: value
        """
        return self.session.walk(oid=oid)[0][-1]

    def get_by_id(self, oid: str, ID: int = 0):
        """
        Get a specific value from an oid with a specific id
        :param oid:
        :param ID:
        :return: str: value
        """
        return self.get(oid=f"{oid}.{ID}")

    def get_table(self, oid: str, sort_key: str = None):
        """
        Get a SNMP table
        :param oid:
        :param sort_key:
        :return: list of dicts
        """
        return self.session.get_table(oid=oid, sortkey=sort_key)

    def walk(self, oid: str):
        """
        Walk command for SNMP
        :param oid:
        :return: dict
        """
        return dict(self.session.walk(oid=oid))

    def bulk(self, *OIDS_list: list):
        """
        Bulk command for SNMP
        :param OIDS_list: list of oids
        :return: dict
        """
        errorIndication, errorStatus, errorIndex, snmpDataTable = cmdgen.CommandGenerator().bulkCmd(
            cmdgen.CommunityData(self.read_community),
            cmdgen.UdpTransportTarget((self.host, self.port)),
            0, 25,
            *OIDS_list,
            lexicographicMode=False
        )

        results = {}
        if not errorIndication and not errorStatus:
            for snmpDataTableRow in snmpDataTable:
                for name, val in snmpDataTableRow:
                    results[str(name)] = str(snmpDataTableRow[0]).split(" = ")[1]
        return results