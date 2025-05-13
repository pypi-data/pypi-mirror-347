import unittest
import os
import json
from mqtt_presence.appdata import Configuration, Broker, Homeassistant, ConfigFiles
from mqtt_presence.config_handler import Config_Handler


class TestConfiguration(unittest.TestCase):
    def get_Config_Handler(self, configFile):
        configFiles = ConfigFiles()
        configFiles.configFile = configFile
        return Config_Handler(configFiles())

    def test_load_defaults_when_file_missing(self):
        config_handler: Config_Handler = self.get_Config_Handler("non_existing.json")
        config = config_handler.load_config()
       
        self.assertIsInstance(config.data.mqtt.broker, Broker)
        self.assertIsInstance(config.data.mqtt.homeassistant, Homeassistant)
        self.assertEqual(config.data.mqtt.broker.host, "localhost")

    def test_load_valid_json(self):
        sample_config = {
            'mqtt': {
                'broker': {
                    'host': 'testhost',
                    'port': 1884,
                    'username': 'user',
                    'encrypted_password': 'pass',
                    'client_id': 'test-client',
                    'keepalive': 60,
                    'prefix': 'topic-prefix'
                },
                'homeassistant': {
                    'enabled': True,
                    'discovery_prefix': 'testprefix',
                    'device_name': 'TestDevice'
                }
            }
        }

        with open("temp_config.json", "w") as f:
            json.dump(sample_config, f)

        config_handler: Config_Handler = self.get_Config_Handler("temp_config.json")
        config = config_handler.load_config()
        self.assertEqual(config.data.mqtt.broker.host, "testhost")
        self.assertEqual(config.data.mqtt.homeassistant.device_name, "TestDevice")

        os.remove("temp_config.json")
