from mqtt_presence.mqtt_client import MQTTClient
from mqtt_presence.config_handler import Config_Handler
from mqtt_presence.webui import WebUI
from mqtt_presence.consoleui import ConsoleUI
from mqtt_presence.appdata import Configuration
from mqtt_presence.utils import Tools

import time
import logging
logger = logging.getLogger(__name__)



# app_state_singleton.py
#class MQTTPresenceAppSingleton:
#    _instance = None
#
#    @classmethod
#    def init(cls, app_state):
#        cls._instance = app_state
#
#    @classmethod
#    def get(cls):
#        if cls._instance is None:
#            raise Exception("MQTTPresenceApp wurde noch nicht initialisiert!")
#        return cls._instance


class MQTTPresenceApp:
    def __init__(self, config_handler: Config_Handler):
        # set singleton!
        #AppStateSingleton.init(self)

        self.config_handler = config_handler
        self.should_run = True
        
        # load config
        self.loadConfig()

        self.mqttClient: MQTTClient = MQTTClient(self)
        self.consoleUI: ConsoleUI = ConsoleUI(self)
        self.webUI = WebUI(self)

    def loadConfig(self):
        self.config = self.config_handler.load_config()
        self.appConfig = self.config_handler.load_config_yaml()


    def updateNewConfig(self, config : Configuration):
        self.config_handler.save_config(config)
        self.restart()

    def runConsoleUI(self):
        # Start Console UI 
        self.consoleUI.runUI()

    def runWebUI(self):
        # start webui
        self.webUI.runUI(self.appConfig.app.webServer.host, self.appConfig.app.webServer.port)

    def start(self):
        #show platform
        Tools.logPlatform()        
        self.mqttClient.start()


    def restart(self):
        self.config = self.config_handler.load_config()
        self.mqttClient.start()

    def exitApp(self):
        self.should_run = False
        self.mqttClient.stop()
        #self.consoleUI.stop()
        self.webUI.stop()
        time.sleep(1)
        Tools.exitApplication()
        


    def shutdown(self):
        logger.info("🛑 Shutdown initiated...")
        if (not self.appConfig.app.disableShutdown):
            Tools.shutdown()
        else:
            logger.info("Shutdown disabled!")

    def reboot(self):
        logger.info("🔄 Reboot initiated...")
        if (not self.appConfig.app.disableShutdown):
            Tools.reboot()
        else:
            logger.info("Shutdown disabled!")                
