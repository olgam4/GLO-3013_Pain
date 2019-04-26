from logging import getLogger

from gpiozero import MCP3008, BadPinFactory

from dexterity.domain.iChargeable import IChargeable

logger = getLogger(__name__)


class AdcCharge(IChargeable):
    def __init__(self) -> None:
        try:
            self._adc = MCP3008(channel=0, max_voltage=5)
        except BadPinFactory:
            self._adc = None
            logger.warning("No spi device found in gpio")

    def get_charge(self) -> float:
        if self._adc:
            return self._adc.value
        return 0
