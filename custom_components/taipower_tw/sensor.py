"""Taipower integration."""
import datetime
import logging

from homeassistant.components.sensor import (STATE_CLASS_MEASUREMENT,
                                             SensorEntity)
from homeassistant.const import (DEVICE_CLASS_DATE, DEVICE_CLASS_ENERGY,
                                 DEVICE_CLASS_MONETARY, ENERGY_KILO_WATT_HOUR)

from . import AMI_KEY, API, COORDINATOR, DOMAIN, MONTH_KEY, TaipowerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    
    api = hass.data[DOMAIN][API]
    coordinator = hass.data[DOMAIN][COORDINATOR]

    for meter in api.meters.values():
        if meter.type == "AMI":
            async_add_entities(
                [
                    TaipowerAMIOffPeakKwhSensorEntity(meter, coordinator),
                    TaipowerAMIHalfPeakKwhSensorEntity(meter, coordinator),
                    TaipowerAMISatPeakKwhSensorEntity(meter, coordinator),
                    TaipowerAMIPeakKwhSensorEntity(meter, coordinator),
                    TaipowerAMITotalKwhSensorEntity(meter, coordinator),
                    TaipowerAMIStartTimeIndicatorSensorEntity(meter, coordinator),
                    TaipowerAMIEndTimeIndicatorSensorEntity(meter, coordinator),
                    TaipowerBillChargePeriodSensorEntity(meter, coordinator),
                    TaipowerBillChargeSensorEntity(meter, coordinator),
                    TaipowerBillFormulaSensorEntity(meter, coordinator),
                    TaipowerBillKwhSensorEntity(meter, coordinator),
                    TaipowerBillMonthIndicatorSensorEntity(meter, coordinator),
                ],
            )


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the sensor platform from a config entry."""

    api = hass.data[DOMAIN][API]
    coordinator = hass.data[DOMAIN][COORDINATOR]

    for meter in api.meters.values():
        if meter.type == "AMI":
            async_add_devices(
                [
                    TaipowerAMIOffPeakKwhSensorEntity(meter, coordinator),
                    TaipowerAMIHalfPeakKwhSensorEntity(meter, coordinator),
                    TaipowerAMISatPeakKwhSensorEntity(meter, coordinator),
                    TaipowerAMIPeakKwhSensorEntity(meter, coordinator),
                    TaipowerAMITotalKwhSensorEntity(meter, coordinator),
                    TaipowerAMIStartTimeIndicatorSensorEntity(meter, coordinator),
                    TaipowerAMIEndTimeIndicatorSensorEntity(meter, coordinator),
                    TaipowerBillChargePeriodSensorEntity(meter, coordinator),
                    TaipowerBillChargeSensorEntity(meter, coordinator),
                    TaipowerBillFormulaSensorEntity(meter, coordinator),
                    TaipowerBillKwhSensorEntity(meter, coordinator),
                    TaipowerBillMonthIndicatorSensorEntity(meter, coordinator),
                ],
            )


class TaipowerAMIOffPeakKwhSensorEntity(TaipowerEntity, SensorEntity):
    def __init__(self, meter, coordinator):
        super().__init__(meter, coordinator)
    
    @property
    def available(self) -> bool:
        ami_key = self.hass.data[DOMAIN][AMI_KEY]
        if ami_key in self._meter.ami and self._meter.ami[ami_key].is_missing_data:
            return False
        return True

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._meter.name} {self._meter.number} AMI Off-peak Kw/h"

    @property
    def state(self):
        """Return the ami off-peak KW/H."""
        ami_key = self.hass.data[DOMAIN][AMI_KEY]
        if self._meter.ami is not None and ami_key in self._meter.ami:
            return self._meter.ami[ami_key].offpeak_kwh
        return None

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_ENERGY

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return ENERGY_KILO_WATT_HOUR

    @property
    def unique_id(self):
        return f"{self._meter.number}_ami_offpeak_kwh_sensor"
    
    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT


class TaipowerAMIHalfPeakKwhSensorEntity(TaipowerEntity, SensorEntity):
    def __init__(self, meter, coordinator):
        super().__init__(meter, coordinator)
    
    @property
    def available(self) -> bool:
        ami_key = self.hass.data[DOMAIN][AMI_KEY]
        if ami_key in self._meter.ami and self._meter.ami[ami_key].is_missing_data:
            return False
        return True

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._meter.name} {self._meter.number} AMI Half-peak Kw/h"

    @property
    def state(self):
        """Return the ami half-peak KW/H."""
        ami_key = self.hass.data[DOMAIN][AMI_KEY]
        if self._meter.ami is not None and ami_key in self._meter.ami:
            return self._meter.ami[ami_key].halfpeak_kwh
        return None

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_ENERGY

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return ENERGY_KILO_WATT_HOUR

    @property
    def unique_id(self):
        return f"{self._meter.number}_ami_halfpeak_kwh_sensor"
    
    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT


class TaipowerAMISatPeakKwhSensorEntity(TaipowerEntity, SensorEntity):
    def __init__(self, meter, coordinator):
        super().__init__(meter, coordinator)
    
    @property
    def available(self) -> bool:
        ami_key = self.hass.data[DOMAIN][AMI_KEY]
        if ami_key in self._meter.ami and self._meter.ami[ami_key].is_missing_data:
            return False
        return True

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._meter.name} {self._meter.number} AMI Saturday Half-peak Kw/h"

    @property
    def state(self):
        """Return the ami saturday half-peak KW/H."""
        ami_key = self.hass.data[DOMAIN][AMI_KEY]
        if self._meter.ami is not None and ami_key in self._meter.ami:
            return self._meter.ami[ami_key].satpeak_kwh
        return None

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_ENERGY

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return ENERGY_KILO_WATT_HOUR

    @property
    def unique_id(self):
        return f"{self._meter.number}_ami_satpeak_kwh_sensor"
    
    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT


class TaipowerAMIPeakKwhSensorEntity(TaipowerEntity, SensorEntity):
    def __init__(self, meter, coordinator):
        super().__init__(meter, coordinator)
    
    @property
    def available(self) -> bool:
        ami_key = self.hass.data[DOMAIN][AMI_KEY]
        if ami_key in self._meter.ami and self._meter.ami[ami_key].is_missing_data:
            return False
        return True

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._meter.name} {self._meter.number} AMI Peak Kw/h"

    @property
    def state(self):
        """Return the ami peak KW/H."""
        ami_key = self.hass.data[DOMAIN][AMI_KEY]
        if self._meter.ami is not None and ami_key in self._meter.ami:
            return self._meter.ami[ami_key].peak_kwh
        return None

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_ENERGY

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return ENERGY_KILO_WATT_HOUR

    @property
    def unique_id(self):
        return f"{self._meter.number}_ami_peak_kwh_sensor"
    
    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT


class TaipowerAMITotalKwhSensorEntity(TaipowerEntity, SensorEntity):
    def __init__(self, meter, coordinator):
        super().__init__(meter, coordinator)

    @property
    def available(self) -> bool:
        ami_key = self.hass.data[DOMAIN][AMI_KEY]
        if ami_key in self._meter.ami and self._meter.ami[ami_key].is_missing_data:
            return False
        return True

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._meter.name} {self._meter.number} AMI Total Kw/h"

    @property
    def state(self):
        """Return the ami total KW/H."""
        ami_key = self.hass.data[DOMAIN][AMI_KEY]
        if self._meter.ami is not None and ami_key in self._meter.ami:
            return self._meter.ami[ami_key].total_kwh
        return None

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_ENERGY

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return ENERGY_KILO_WATT_HOUR

    @property
    def unique_id(self):
        return f"{self._meter.number}_ami_total_kwh_sensor"
    
    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT


class TaipowerAMIStartTimeIndicatorSensorEntity(TaipowerEntity, SensorEntity):
    def __init__(self, meter, coordinator):
        super().__init__(meter, coordinator)

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._meter.name} {self._meter.number} AMI Start Time Indicator"

    @property
    def state(self):
        """Return the date and time in yyyy-mm-dd-hh format."""
        value = self.native_value
        if value is not None:
            return self.native_value.strftime("%Y-%m-%d-%H-%M-%S")
        return None
        
    @property
    def native_value(self):
        """Return the date and time in datetime.datetime object."""
        ami_key = self.hass.data[DOMAIN][AMI_KEY]
        if self._meter.ami is not None and ami_key in self._meter.ami:
            start_time = self._meter.ami[ami_key].start_time
            return datetime.datetime(int(start_time[0:4]), int(start_time[4:6]), int(start_time[6:8]), int(start_time[8:10]), int(start_time[10:12]), int(start_time[12:14]))
        return None

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_DATE

    @property
    def unique_id(self):
        return f"{self._meter.number}_ami_start_time_indicator_sensor"


class TaipowerAMIEndTimeIndicatorSensorEntity(TaipowerEntity, SensorEntity):
    def __init__(self, meter, coordinator):
        super().__init__(meter, coordinator)

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._meter.name} {self._meter.number} AMI End Time Indicator"

    @property
    def state(self):
        """Return the date and time in yyyy-mm-dd-hh format."""
        value = self.native_value
        if value is not None:
            return self.native_value.strftime("%Y-%m-%d-%H-%M-%S")
        return None
        
    @property
    def native_value(self):
        """Return the date and time in datetime.datetime object."""
        ami_key = self.hass.data[DOMAIN][AMI_KEY]
        if self._meter.ami is not None and ami_key in self._meter.ami:
            end_time = self._meter.ami[ami_key].end_time
            return datetime.datetime(int(end_time[0:4]), int(end_time[4:6]), int(end_time[6:8]), int(end_time[8:10]), int(end_time[10:12]), int(end_time[12:14]))
        return None

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_DATE

    @property
    def unique_id(self):
        return f"{self._meter.number}_ami_end_time_indicator_sensor"


class TaipowerBillChargePeriodSensorEntity(TaipowerEntity, SensorEntity):
    def __init__(self, meter, coordinator):
        super().__init__(meter, coordinator)
    
    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._meter.name} {self._meter.number} Bill Charge Period"
    
    @property
    def state(self):
        """Return the bill charge period."""
        month_key = self.hass.data[DOMAIN][MONTH_KEY]
        if self._meter.bill_records is not None and month_key in self._meter.bill_records:
            return self._meter.bill_records[month_key].period
        return None

    @property
    def unique_id(self):
        return f"{self._meter.number}_bill_charge_period_sensor"
    
    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT


class TaipowerBillChargeSensorEntity(TaipowerEntity, SensorEntity):
    def __init__(self, meter, coordinator):
        super().__init__(meter, coordinator)
    
    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._meter.name} {self._meter.number} Bill Charge"
    
    @property
    def state(self):
        """Return the bill charge."""
        month_key = self.hass.data[DOMAIN][MONTH_KEY]
        if self._meter.bill_records is not None and month_key in self._meter.bill_records:
            return self._meter.bill_records[month_key].charge
        return None

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_MONETARY

    @property
    def unique_id(self):
        return f"{self._meter.number}_bill_charge_sensor"
    
    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT


class TaipowerBillFormulaSensorEntity(TaipowerEntity, SensorEntity):
    def __init__(self, meter, coordinator):
        super().__init__(meter, coordinator)
    
    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._meter.name} {self._meter.number} Bill Formula"
    
    @property
    def state(self):
        """Return the bill formula."""
        month_key = self.hass.data[DOMAIN][MONTH_KEY]
        if self._meter.bill_records is not None and month_key in self._meter.bill_records:
            return self._meter.bill_records[month_key].formula
        return None

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_MONETARY

    @property
    def unique_id(self):
        return f"{self._meter.number}_bill_formula_sensor"
    
    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT


class TaipowerBillKwhSensorEntity(TaipowerEntity, SensorEntity):
    def __init__(self, meter, coordinator):
        super().__init__(meter, coordinator)

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._meter.name} {self._meter.number} Bill Kw/h"

    @property
    def state(self):
        """Return the bill KW/H."""
        month_key = self.hass.data[DOMAIN][MONTH_KEY]
        if self._meter.bill_records is not None and month_key in self._meter.bill_records:
            return self._meter.bill_records[month_key].kwh
        return None

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_ENERGY

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return ENERGY_KILO_WATT_HOUR

    @property
    def unique_id(self):
        return f"{self._meter.number}_bill_kwh_sensor"
    
    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT


class TaipowerBillMonthIndicatorSensorEntity(TaipowerEntity, SensorEntity):
    def __init__(self, meter, coordinator):
        super().__init__(meter, coordinator)

    @property
    def name(self):
        """Return the name of the entity."""
        return f"{self._meter.name} {self._meter.number} Bill Month Indicator"

    @property
    def state(self):
        """Return the month in yyyy-mm format."""
        value = self.native_value
        if value is not None:
            return self.native_value.strftime("%Y-%m")
        return None
        
    @property
    def native_value(self):
        """Return the month in datetime.date object."""
        month_key = self.hass.data[DOMAIN][MONTH_KEY]
        if month_key is not None:
            return datetime.date(int(month_key[0:4]), int(month_key[5:]), 1)
        return None

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_DATE

    @property
    def unique_id(self):
        return f"{self._meter.number}_bill_month_indicator_sensor"