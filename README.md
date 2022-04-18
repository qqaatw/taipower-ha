# Taipower Home Assistant Integration

## Feature
A home assistant integration for retrieving Taipower data, using [libtaipower](https://github.com/qqaatw/libtaipower) backend.

## Installation

### Configuring via UI

1. Create `config/custom_components` folder if not existing.
2. Copy `taipower_tw` into `custom_components` folder.
3. Click `Configuration` button on the left side of Home Assistant panel, and then click `Integrations` tab.
4. Click `ADD INTEGRATION` button at the bottom right corner and follow the UI.

### Configuring via `configuration.yaml`

1. Create `config/custom_components` folder if not existing.
2. Copy `taipower_tw` into `custom_components` folder.
3. Configure your account (phone number), password, and electric numbers registered in the Taipower app, in `config/configuration.yaml`. If electric numbers are not provided, they will be fetched from the API automatically. (not recommended.)
4. Restart Home Assistant.

*An example of `configuration.yaml` can be found [here](configuration.yaml).*

## Supported devices

- Taipower AMI electric meter 臺電 AMI 電錶
  - AMI info AMI 資訊
  - Bill records 帳單紀錄

## Tested devices


## Known issues

Currently none.

## License

Apache License 2.0
