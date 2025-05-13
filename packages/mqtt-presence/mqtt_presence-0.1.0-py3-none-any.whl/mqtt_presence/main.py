from mqtt_presence.mqttpresenceapp import MQTTPresenceApp#, MQTTPresenceAppSingleton
from mqtt_presence.config_handler import Config_Handler
from mqtt_presence.appdata import ConfigFiles

import signal, sys
import logging

# setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Konsole
        #logging.FileHandler('log/mqtt_presence.log', mode='a', encoding='utf-8')  # Datei (append mode)
    ]
)
logger = logging.getLogger(__name__)



def main():
    def stop(signum, frame):
        logger.info("🚪 Stop signal recived, exiting...")
        if (mqttAPP is not None):
            mqttAPP.exitApp()

    logger.info("🚀 mqtt-presence startup")
    mqttAPP: MQTTPresenceApp = MQTTPresenceApp(Config_Handler(ConfigFiles()))
    #MQTTPresenceAppSingleton.init(appState)

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    mqttAPP.start()
    mqttAPP.runWebUI()



if __name__ == "__main__":
    main()
