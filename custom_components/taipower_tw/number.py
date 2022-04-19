"""Taipower integration."""
import logging

from homeassistant.components.number import NumberEntity

from . import API, AMI_KEY, COORDINATOR, DOMAIN, TaipowerEntity, MONTH_KEY

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the number platform."""
    
    api = hass.data[DOMAIN][API]
    coordinator = hass.data[DOMAIN][COORDINATOR]

    for meter in api.meters.values():
        async_add_entities(
            [
                TaipowerAMISelectorNumberEntity(meter, coordinator),
                TaipowerMonthlyDataSelectorNumberEntity(meter, coordinator)
            ],
            update_before_add=True
        )


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the number platform from a config entry."""

    api = hass.data[DOMAIN][API]
    coordinator = hass.data[DOMAIN][COORDINATOR]

    for meter in api.meters.values():
        async_add_devices(
            [
                TaipowerAMISelectorNumberEntity(meter, coordinator),
                TaipowerMonthlyDataSelectorNumberEntity(meter, coordinator)
            ],
            update_before_add=True
        )


class TaipowerMonthlyDataSelectorNumberEntity(TaipowerEntity, NumberEntity):
    def __init__(self, meter, coordinator):
        super().__init__(meter, coordinator)
        self._value = 0

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._meter.name} {self._meter.number} Month Selector"
    
    @property
    def value(self):
        """Return the value of the entity."""
        return self._value

    @property
    def min_value(self):
        """Return the minimum month."""
        return 0

    @property
    def max_value(self):
        """Return the maximum month."""
        return len(self._meter.bill_records) - 1 if self._meter.bill_records is not None else 0

    @property
    def unique_id(self):
        return f"{self._meter.number}_monthly_data_selector_number"

    def set_value(self, value):
        """Set new month."""
        value = int(value)
        _LOGGER.debug(f"Set {self.name} value to {value}")
        self._value = value
        self.hass.data[DOMAIN][MONTH_KEY] = list(self._meter.bill_records.keys())[value]
        self.update()


class TaipowerAMISelectorNumberEntity(TaipowerEntity, NumberEntity):
    def __init__(self, meter, coordinator):
        super().__init__(meter, coordinator)
        self._value = 0

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._meter.name} {self._meter.number} AMI Selector"
    
    @property
    def value(self):
        """Return the value of the entity."""
        return self._value

    @property
    def min_value(self):
        """Return the minimum value."""
        return 0

    @property
    def max_value(self):
        """Return the maximum value."""
        return len(self._meter.ami) - 1 if self._meter.ami is not None else 0

    @property
    def unique_id(self):
        return f"{self._meter.number}_ami_selector_number"

    def set_value(self, value):
        """Set new value."""
        value = int(value)
        _LOGGER.debug(f"Set {self.name} value to {value}")
        self._value = value
        self.hass.data[DOMAIN][AMI_KEY] = list(self._meter.ami.keys())[value]
        self.update()