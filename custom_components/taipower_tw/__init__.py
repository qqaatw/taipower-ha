"""Taipower integration."""
import asyncio
import logging
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Optional

import async_timeout
from homeassistant.helpers import discovery
from homeassistant.helpers.update_coordinator import (CoordinatorEntity,
                                                      DataUpdateCoordinator,
                                                      UpdateFailed)

from .const import (AMI_KEY, API, CONF_ACCOUNT, CONF_AMI_PERIOD, CONF_DEVICES,
                    CONF_PASSWORD, CONF_RETRY, CONFIG_SCHEMA, COORDINATOR,
                    DOMAIN, MONTH_KEY)

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["number", "sensor"]
DATA_UPDATE_INTERVAL = timedelta(minutes=30)
BASE_TIMEOUT = 5

from Taipower.api import TaipowerAPI


async def async_setup(hass, config):
    """Set up from the configuration.yaml"""
    if config.get(DOMAIN, None) is None:
        # skip if no config defined in configuration.yaml"""
        return True
    
    # translate correct words to typos, thanks to Taipower ^U^.
    if CONF_AMI_PERIOD in config[DOMAIN]:
        if config[DOMAIN][CONF_AMI_PERIOD] == "hourly":
            config[DOMAIN][CONF_AMI_PERIOD] = "hour"
        elif config[DOMAIN][CONF_AMI_PERIOD] == "quarter":
            config[DOMAIN][CONF_AMI_PERIOD] = "quater"

    _LOGGER.debug(
        {
            "CONF_ACCOUNT": config[DOMAIN].get(CONF_ACCOUNT),
            "CONF_PASSWORD": '*' * len(config[DOMAIN].get(CONF_PASSWORD)),
            "CONF_DEVICES": config[DOMAIN].get(CONF_DEVICES),
            "CONF_AMI_PERIOD": config[DOMAIN].get(CONF_AMI_PERIOD),
            "CONF_RETRY": config.get(CONF_RETRY),
        }
    )

    if config[DOMAIN].get(CONF_DEVICES) == []:
        config[DOMAIN][CONF_DEVICES] = None

    api = TaipowerAPI(
        account=config[DOMAIN].get(CONF_ACCOUNT),
        password=config[DOMAIN].get(CONF_PASSWORD),
        electric_numbers=config[DOMAIN].get(CONF_DEVICES),
        ami_period=config[DOMAIN].get(CONF_AMI_PERIOD),
        max_retries=config[DOMAIN].get(CONF_RETRY),
    )

    hass.data[DOMAIN] = {}
    hass.data[DOMAIN][API] = api
    hass.data[DOMAIN][AMI_KEY] = None
    hass.data[DOMAIN][MONTH_KEY] = None
    hass.data[DOMAIN][COORDINATOR] = None

    try:
        await hass.async_add_executor_job(api.login)
    except AssertionError as err:
        _LOGGER.error(f"Assertion check error: {err}")
        return False
    except RuntimeError as err:
        _LOGGER.error(f"Failed to login API: {err}")
        return False

    _LOGGER.debug(
        f"Electric meter info: {[meter for meter in api.meters.values()]}")
    
    async def async_update_data():
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(BASE_TIMEOUT + len(api.meters) * 2):
                await hass.async_add_executor_job(api.refresh_status)

        except asyncio.TimeoutError as err:
            raise UpdateFailed(f"Command executed timed out when regularly fetching data.")

        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
        
        #_LOGGER.debug(
        #    f"Latest data: {[(name, value.status) for name, value in hass.data[DOMAIN][UPDATED_DATA].items()]}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name=DOMAIN,
        update_method=async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=DATA_UPDATE_INTERVAL,
    )

    await coordinator.async_refresh()

    hass.data[DOMAIN][COORDINATOR] = coordinator
    
    # Start Taipower components
    if hass.data[DOMAIN][API]:
        _LOGGER.debug("Starting Taipower components.")
        for platform in PLATFORMS:
            discovery.load_platform(hass, platform, DOMAIN, {}, config)

    # Return boolean to indicate that initialization was successful.
    return True

async def async_setup_entry(hass, config_entry):
    """Set up from a config entry."""

    config = config_entry.data[DOMAIN]
    _LOGGER.debug(
        {
            "CONF_ACCOUNT": config.get(CONF_ACCOUNT),
            "CONF_PASSWORD": '*' * len(config.get(CONF_PASSWORD)),
            "CONF_DEVICES": config.get(CONF_DEVICES),
            "CONF_AMI_PERIOD": config.get(CONF_AMI_PERIOD),
            "CONF_RETRY": config.get(CONF_RETRY),            
        }
    )

    if config.get(CONF_DEVICES) == []:
        config[CONF_DEVICES] = None

    api = TaipowerAPI(
        account=config.get(CONF_ACCOUNT),
        password=config.get(CONF_PASSWORD),
        electric_numbers=config.get(CONF_DEVICES),
        ami_period=config.get(CONF_AMI_PERIOD),
        max_retries=config.get(CONF_RETRY),
    )

    hass.data[DOMAIN] = {}
    hass.data[DOMAIN][API] = api
    hass.data[DOMAIN][AMI_KEY] = None
    hass.data[DOMAIN][MONTH_KEY] = None
    hass.data[DOMAIN][COORDINATOR] = None

    try:
        await hass.async_add_executor_job(api.login)
    except AssertionError as err:
        _LOGGER.error(f"Assertion check error: {err}")
        return False
    except RuntimeError as err:
        _LOGGER.error(f"Failed to login API: {err}")
        return False

    _LOGGER.debug(
        f"Electric meter info: {[meter for meter in api.meters.values()]}")
    
    async def _async_update_data():
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(BASE_TIMEOUT + len(api.meters) * 2):
                await hass.async_add_executor_job(api.refresh_status)

        except asyncio.TimeoutError as err:
            raise UpdateFailed(f"Command executed timed out when regularly fetching data.")

        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    def _async_forward_entry_setup():
        for platform in PLATFORMS:
            hass.async_create_task(
                hass.config_entries.async_forward_entry_setup(config_entry, platform)
            )

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name=DOMAIN,
        update_method=_async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=DATA_UPDATE_INTERVAL,
    )

    await coordinator.async_refresh()

    hass.data[DOMAIN][COORDINATOR] = coordinator
    
    # Start Taipower components
    if hass.data[DOMAIN][API]:
        _LOGGER.debug("Starting Taipower components.")
        _async_forward_entry_setup()
    
    # Return boolean to indicate that initialization was successful.
    return True


@dataclass
class UpdateData:
    status_name : str
    electric_number : str
    status_value : Optional[int] = field(default_factory=None)
    status_str_value : Optional[str] = field(default_factory=None)


class TaipowerEntity(CoordinatorEntity):
    def __init__(self, meter, coordinator):
        super().__init__(coordinator)
        self._meter = meter

    @property
    def device_info(self) -> dict:
        """Return device info of the entity."""
        return {
            "identifiers": {(DOMAIN, self._meter.number)},
            "name": f"{self._meter.name} {self._meter.number}",
            "manufacturer": "Taipower",
            "model": "Taipower AMI",
        }
    
    @property
    def available(self) -> bool:
        """Indicate whether the entity is available."""
        return True

    @property
    def name(self):
        """Return the mater's name."""
        return self._meter.name

    @property
    def unique_id(self):
        """Return the entity's unique id."""
        raise NotImplementedError
    
    def update(self):
        """Update latest status"""
        _LOGGER.debug(f"Manually writing new states to entities.")
        for update_callback in self.coordinator._listeners:
            update_callback()