#!/usr/bin/python3
import config
import paho.mqtt.client as mqtt
import logging
import time

class HassioMqttClient:
    flag_connected = 0

    def __init__(self):
        logger = logging.getLogger(__name__)
        first_connect_retry_counter = 0
        first_connect_retry_max = 10
        while self.flag_connected == 0 and first_connect_retry_counter < first_connect_retry_max:
            self.client = mqtt.Client("Fenecon2Hassio", clean_session=False)
            self.client.username_pw_set(config.hassio['mqtt_broker_user'], config.hassio['mqtt_broker_passwd'])
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_message = self.on_message
            
            logger.info('Connect to MQTT broker')
            try:
                self.client.connect(config.hassio['mqtt_broker_host'], config.hassio['mqtt_broker_port'], config.hassio['mqtt_broker_keepalive'])
                self.client.loop_start()
                time.sleep(1)
            except Exception:
                first_connect_retry_counter += 1
                logger.warning(f'Trying to connect ({first_connect_retry_counter}/{first_connect_retry_max}). Mqtt broker not reachable. Check availability and config.')
                logger.warning(f'  Broker IP    : {config.hassio["mqtt_broker_host"]}')
                logger.warning(f'  Broker Port  : {config.hassio["mqtt_broker_port"]}')
                logger.warning(f'  Broker User  : {config.hassio["mqtt_broker_user"]}')
                logger.warning('  Broker Passwd: look in configuration')
                logger.warning('wait 30 seconds')
                time.sleep(30)
        if first_connect_retry_max == first_connect_retry_counter:
            logger.error('Connect to MQTT broker not possible. Exit!')
            quit()

    def on_connect(self, client, userdata, flags, rc):
        logger = logging.getLogger(str(f"on_connect-{__name__}"))
        if rc==0:
            logger.info(f"connected OK Returned code={rc}")
            self.flag_connected = 1
        else:
            logger.warning(f"Bad connection Returned code={rc}")


    def on_disconnect(self, client, userdata, rc):
        logger = logging.getLogger(str(f"on_disconnect-{__name__}"))
        if rc != 0:
            logger.warning("Unexpected MQTT disconnection. Will auto-reconnect")
        self.flag_connected = 0

    def publish(self, *args, **kwargs):
        logger = logging.getLogger(__name__)
        if self.flag_connected == 1:
            logger.debug("HassioMqttClient: publish - connected")
            self.client.publish(*args, **kwargs)
        #else:
            # Wait to reconnect

    def on_message(self, client, userdata, message):
        logger = logging.getLogger(__name__)
        logger.debug("clear HA discovery topic")
        if message.retain and str(message.topic).startswith(config.hassio['mqtt_broker_hassio_discovery_queue']):
            # Only process retained messages form dircovery topic
            logger.debug(f'clear HA discovery topic: {message.topic}')
            self.client.publish(message.topic, None, 0, True)

    def clear_ha_discovery_topic(self):
        logger = logging.getLogger(__name__)

        if self.flag_connected == 0:
            logger.warning("not connected")
            return
        
        logger.info('Subscribe to discovery topic')
        self.client.subscribe(f"{config.hassio['mqtt_broker_hassio_discovery_queue']}/#")
        time.sleep(1)
        logger.info('Unsubscribe to discovery topic')
        self.client.unsubscribe(f"{config.hassio['mqtt_broker_hassio_discovery_queue']}/#")
        return