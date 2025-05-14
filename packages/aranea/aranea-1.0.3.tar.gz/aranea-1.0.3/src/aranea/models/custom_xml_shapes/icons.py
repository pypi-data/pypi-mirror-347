"""
Module for creating image strings for custom icons in drawio.
"""

from enum import Enum
from typing import Dict

from jinja2 import Template

from aranea.models.custom_xml_shapes import jinja_environment
from aranea.models.custom_xml_shapes.custom_xml_shapes_utils import \
    get_mx_cell_image_str


class IconIdentifier(Enum):
    """
    Enum providing icon identifiers.
    """

    AMG = "AMG"
    NETWORK_SWITCH = "NETWORK_SWITCH"
    BACKEND = "BACKEND"
    CELLULAR = "CELLULAR"
    WIFI = "WIFI"
    BLUETOOTH = "BLUETOOTH"
    USB = "USB"
    SATELLITE = "SATELLITE"
    CAR_CHARGER = "CAR_CHARGER"
    DIGITAL_BROADCAST = "DIGITAL_BROADCAST"
    ANALOG_BROADCAST = "ANALOG_BROADCAST"
    NFC = "NFC"


class IconFactory:
    """
    Class for creating image strings for custom icons in drawio.
    """

    icon_identifier_templates: Dict[IconIdentifier, str] = {
        IconIdentifier.AMG: "amg_icon.svg.jinja",
        IconIdentifier.ANALOG_BROADCAST: "analog_broadcast_icon.svg.jinja",
        IconIdentifier.BACKEND: "backend_icon.svg.jinja",
        IconIdentifier.BLUETOOTH: "bluetooth_icon.svg.jinja",
        IconIdentifier.CAR_CHARGER: "car_charger_icon.svg.jinja",
        IconIdentifier.CELLULAR: "cellular_icon.svg.jinja",
        IconIdentifier.DIGITAL_BROADCAST: "digital_broadcast_icon.svg.jinja",
        IconIdentifier.NETWORK_SWITCH: "network_switch_icon.svg.jinja",
        IconIdentifier.NFC: "nfc_icon.svg.jinja",
        IconIdentifier.SATELLITE: "satellite_icon.svg.jinja",
        IconIdentifier.USB: "usb_icon.svg.jinja",
        IconIdentifier.WIFI: "wifi_icon.svg.jinja",
    }

    def get_icon_str(self, icon_identifier: IconIdentifier) -> str:
        """
        Function for getting icon strings.

        :param icon_identifier: The icon identifier.
        :type icon_identifier: IconIdentifier
        :return: The icon string.
        :rtype: str
        """
        icon_template: Template = jinja_environment.get_template(
            self.icon_identifier_templates[icon_identifier]
        )
        return get_mx_cell_image_str(icon_template.render())
