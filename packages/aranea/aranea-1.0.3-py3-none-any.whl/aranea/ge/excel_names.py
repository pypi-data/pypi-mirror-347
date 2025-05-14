"""Module for storing the names of the columns in the Excel file containing the ECU ratings."""

from enum import Enum

from aranea.models.graph_model import TechnicalCapabilityName


class ExcelColumnNames(Enum):
    """Column names of the Excel file containing the ECU ratings."""

    ECU_NAME = "ECU Name"
    SECURITY_CLASS = "Security Class"
    EXTERNAL_INTERFACE = "External Interface"
    GATEWAY = "GW"
    LIN_SLAVE = "Lin-Slave"
    DOMAIN = "Domain"
    TECHNICAL_CAPABILITY = "Technical Capability"
    CRITICAL_ELEMENT = "Critical Element"


YES_NO_COLUMNS: list[str] = [
    ExcelColumnNames.EXTERNAL_INTERFACE.value,
    ExcelColumnNames.GATEWAY.value,
    ExcelColumnNames.LIN_SLAVE.value,
    ExcelColumnNames.CRITICAL_ELEMENT.value,
]


class ExcelTechnicalCapabilityNames(Enum):
    """The following values of the enum (right side) are valid strings
    for the ``Technical Capability`` column in the Excel file.
    """

    ANALOG_BROADCAST = "Radio"
    BACKEND = "Cloud"
    BLUETOOTH = "BT"
    CAR_CHARGER = "PLC"
    CELLULAR = "5G"
    DIGITAL_BROADCAST = "DVB"
    NETWORK_SWITCH = "Switch"
    NFC = "NFC"
    OBD = "OBD"
    SATELLITE = "GNSS"
    USB = "USB"
    WIFI = "Wifi"


EXCEL_TECHNICAL_CAPABILITY_MAP: dict[str, TechnicalCapabilityName] = {
    ExcelTechnicalCapabilityNames.ANALOG_BROADCAST.value: TechnicalCapabilityName.ANALOG_BROADCAST,
    ExcelTechnicalCapabilityNames.BACKEND.value: TechnicalCapabilityName.BACKEND,
    ExcelTechnicalCapabilityNames.BLUETOOTH.value: TechnicalCapabilityName.BLUETOOTH,
    ExcelTechnicalCapabilityNames.CAR_CHARGER.value: TechnicalCapabilityName.CAR_CHARGER,
    ExcelTechnicalCapabilityNames.CELLULAR.value: TechnicalCapabilityName.CELLULAR,
    ExcelTechnicalCapabilityNames.DIGITAL_BROADCAST.value: TechnicalCapabilityName.DIGITAL_BROADCAST,
    ExcelTechnicalCapabilityNames.NETWORK_SWITCH.value: TechnicalCapabilityName.NETWORK_SWITCH,
    ExcelTechnicalCapabilityNames.NFC.value: TechnicalCapabilityName.NFC,
    ExcelTechnicalCapabilityNames.OBD.value: TechnicalCapabilityName.OBD,
    ExcelTechnicalCapabilityNames.SATELLITE.value: TechnicalCapabilityName.SATELLITE,
    ExcelTechnicalCapabilityNames.USB.value: TechnicalCapabilityName.USB,
    ExcelTechnicalCapabilityNames.WIFI.value: TechnicalCapabilityName.WIFI,
}
