from enum import Enum


class OIDS(Enum):
    SYSTEM_UPTIME = "1.3.6.1.2.1.1.3"
    SYSTEM_NAME = "1.3.6.1.2.1.1.5"
    SYSTEM_MAC = "1.3.6.1.2.1.2.2.1.6"
    SYSTEM_TEMPERATURE = "1.3.6.1.4.1.6296.9.1.1.2.5.1.3"

    INTERFACES_DESCRIPTION = "1.3.6.1.2.1.2.2.1.2"
    INTERFACES_SPEED = "1.3.6.1.2.1.2.2.1.5"
    INTERFACES_MAC = "1.3.6.1.2.1.2.2.1.6"

    ONU_TABLE = "1.3.6.1.4.1.6296.101.23.3.1"
    ONU_SIGNAL = "1.3.6.1.4.1.6296.101.23.3.1.1.16"
    ONU_MAC = "1.3.6.1.4.1.6296.102.6.2.6.4.1.1.4"
    ONU_DISTANCE = "1.3.6.1.4.1.6296.101.23.3.1.1.10"
    ONU_PROFILE = "1.3.6.1.4.1.6296.101.23.3.1.1.8"
    ONU_NAME = "1.3.6.1.4.1.6296.101.23.3.1.1.4"
    ONU_STATUS = "1.3.6.1.4.1.6296.101.23.3.1.1.2"
    ONU_UPTIME = "1.3.6.1.4.1.6296.101.23.3.1.1.61"
    ONU_DESCRIPTION = "1.3.6.1.4.1.6296.101.23.3.1.1.18"
    