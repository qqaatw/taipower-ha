"""Taipower integration."""
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import CONF_DEVICES, CONF_PASSWORD

DOMAIN = "taipower_tw"
API = "api"
COORDINATOR = "coordinator"
MONTH_KEY = "month_key"
AMI_KEY = "ami_key"

CONF_ACCOUNT = "account"
CONF_RETRY = "retry"
CONF_AMI_PERIOD = "ami_period"
CONF_ADD_ANOTHER_METER = "add_another_meter"
DEFAULT_RETRY = 5
DEFAULT_AMI_PERIOD = "daily"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_ACCOUNT): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
                vol.Optional(CONF_RETRY, default=DEFAULT_RETRY): cv.positive_int,
                vol.Optional(CONF_DEVICES, default=[]): vol.All(cv.ensure_list, list),
                vol.Optional(CONF_AMI_PERIOD, default=DEFAULT_AMI_PERIOD): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

CONFIG_FLOW_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ACCOUNT): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_RETRY, default=DEFAULT_RETRY): cv.positive_int,
        vol.Optional(CONF_DEVICES, default=""): cv.string,
        vol.Optional(CONF_AMI_PERIOD, default=DEFAULT_AMI_PERIOD): cv.string,
        vol.Optional(CONF_ADD_ANOTHER_METER, default=False): cv.boolean,
    }
)

CONFIG_FLOW_ADD_METER_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_DEVICES, default=""): cv.string,
        vol.Optional(CONF_ADD_ANOTHER_METER, default=False): cv.boolean,
    }
)