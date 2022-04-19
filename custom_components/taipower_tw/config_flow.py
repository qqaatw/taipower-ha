"""Taipower integration."""
import logging

from homeassistant import config_entries

from .const import (CONF_ACCOUNT, CONF_ADD_ANOTHER_METER, CONF_AMI_PERIOD,
                    CONF_DEVICES, CONF_PASSWORD, CONF_RETRY,
                    CONFIG_FLOW_ADD_METER_SCHEMA, CONFIG_FLOW_SCHEMA, DOMAIN)

_LOGGER = logging.getLogger(__name__)

from Taipower.api import TaipowerAPI


async def validate_auth(hass, account, password, electric_numbers, ami_period, max_retries) -> None:
    """Validates Taipower account and meters."""

    api = TaipowerAPI(
        account=account,
        password=password,
        electric_numbers=electric_numbers,
        ami_period=ami_period,
        max_retries=max_retries,
    )
    await hass.async_add_executor_job(api.login)


class TaipowerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Taipower config flow."""
    
    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self.data = None
    
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            self.data = user_input
            if isinstance(user_input[CONF_DEVICES], str):
                if user_input[CONF_DEVICES] == "":
                    self.data[CONF_DEVICES] = []
                else:
                    self.data[CONF_DEVICES] = [user_input[CONF_DEVICES]]
            
            if user_input[CONF_ADD_ANOTHER_METER]:
                return await self.async_step_add_meter()

            # translate correct words to typos, thanks to Taipower ^U^.
            if user_input[CONF_AMI_PERIOD] == "hourly":
                user_input[CONF_AMI_PERIOD] = "hour"
            elif user_input[CONF_AMI_PERIOD] == "quarter":
                user_input[CONF_AMI_PERIOD] = "quater"

            try:
                await validate_auth(
                    self.hass,
                    user_input[CONF_ACCOUNT],
                    user_input[CONF_PASSWORD],
                    user_input[CONF_DEVICES],
                    user_input[CONF_AMI_PERIOD],
                    user_input[CONF_RETRY],
                )
            except AssertionError as err:
                _LOGGER.error(f"Assertion check error: {err}")
                errors['base'] = "assertion_check_error"
            except RuntimeError as err:
                _LOGGER.error(f"Failed to login API: {err}")
                errors['base'] = "login_error"
            except Exception as err:
                _LOGGER.error(f"Failed to login API: {err}")
                errors['base'] = "unknown_error"

            if not errors:
                return self.async_create_entry(
                    title="Taipower TW",
                    data={
                        DOMAIN: user_input
                    }
                )
        return self.async_show_form(
            step_id="user", data_schema=CONFIG_FLOW_SCHEMA, errors=errors
        )
    
    async def async_step_ami_menu(self, user_input=None):
        if user_input is not None:
            return user_input
        
        return self.async_show_menu(
            step_id="ami_menu",
            menu_options={
                "hour": "Hourly",
                "daily": "Daily",
                "monthly": "Monthly",
                "quater": "Quarter",
            },
        )

    async def async_step_add_meter(self, user_input=None):
        errors = {}
        if user_input is not None:
            if user_input[CONF_DEVICES] != "":
                self.data[CONF_DEVICES].append(user_input[CONF_DEVICES])
            if user_input[CONF_ADD_ANOTHER_METER]:
                return await self.async_step_add_meter()
            else:
                self.data[CONF_ADD_ANOTHER_METER] = False
                return await self.async_step_user(self.data)

        return self.async_show_form(
            step_id="add_meter", data_schema=CONFIG_FLOW_ADD_METER_SCHEMA, errors=errors
        )