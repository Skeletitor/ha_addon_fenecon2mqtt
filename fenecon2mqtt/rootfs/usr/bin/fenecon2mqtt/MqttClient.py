#!/usr/bin/python3
import logging
import time

import config
import paho.mqtt.client as mqtt


class MqttClient:
    flag_connected = 0

    def __init__(self):
        logger = logging.getLogger(__name__)
        first_connect_retry_counter = 0
        first_connect_retry_max = 10
        
        while self.flag_connected == 0 and first_connect_retry_counter < first_connect_retry_max:
            logger.info('Connect to MQTT broker')
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, f"Fenecon2Hassio_mqttClient_{first_connect_retry_counter}", clean_session=True)
            self.client.username_pw_set(config.hassio['mqtt_broker_user'], config.hassio['mqtt_broker_passwd'])
            self.client.on_connect = self.connect_callback
            self.client.on_disconnect = self.disconnect_callback
            self.client.on_log = self.log_callback
#            self.client.on_message = self.on_message
            try:
                self.client.connect(config.hassio['mqtt_broker_host'], config.hassio['mqtt_broker_port'], config.hassio['mqtt_broker_keepalive'])
                self.client.loop_start()
                time.sleep(1)
            except Exception:
                self.client.loop_stop()
                first_connect_retry_counter += 1
                logger.warning(f'Trying to connect ({first_connect_retry_counter}/{first_connect_retry_max}). Mqtt broker not reachable. Check availability and config.')
                logger.warning(f'  Broker IP    : {config.hassio["mqtt_broker_host"]}')
                logger.warning(f'  Broker Port  : {config.hassio["mqtt_broker_port"]}')
                logger.warning(f'  Broker User  : {config.hassio["mqtt_broker_user"]}')
                logger.warning('  Broker Passwd: look in configuration')
                logger.warning('wait 30 seconds')
                time.sleep(30)

        if first_connect_retry_max == first_connect_retry_counter:
            logger.error('Connect to MQTT broker not possible. Wait 5 seconds. Exit!')
            time.sleep(5)
            quit()

    def connect_callback(self, client, userdata, flags, reason_code, properties):
        logger = logging.getLogger(str(f"connect_callback-{__name__}"))
        if reason_code.is_failure:
            #print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
            logger.warning(f"Bad connection Returned code={mqtt.connack_string(reason_code)}")
            time.sleep(5)
        else:
            logger.info(f"connected OK Returned code={mqtt.connack_string(reason_code)}")
            # we should always subscribe from on_connect callback to be sure
            # our subscribed is persisted across reconnections.
            client.subscribe("$SYS/#")
            self.flag_connected = 1
    
    def disconnect_callback(self, client, userdata, disconnect_flags, reason_code, properties):
        logger = logging.getLogger(str(f"on_disconnect-{__name__}"))
        logger.info("MQTT disconnection") 
        if reason_code.is_failure:
            logger.warning(f"Unexpected MQTT disconnection code={mqtt.connack_string(reason_code)}. Will auto-reconnect in 5 seconds.")
            time.sleep(5)
        self.flag_connected = 0

    def publish(self, *args, **kwargs):
        logger = logging.getLogger(__name__)
        if self.flag_connected == 1:
            logger.debug("HassioMqttClient: publish - connected")
            self.client.publish(*args, **kwargs)
        #else:
            # Wait to reconnect

    def log_callback(self, client, userdata, level, buf):
        if str(config.log_level).upper() == 'DEBUG':
            logger = logging.getLogger(__name__)
            logger.info(f'MQTT logger - Level: {level} Message: {buf}') 

#    def on_message(self, client, userdata, message):
#        logger = logging.getLogger(__name__)
#        logger.debug("clear HA discovery topic")
#        if message.retain and str(message.topic).startswith(config.hassio['mqtt_broker_hassio_discovery_queue']):
#            # Only process retained messages form discovery topic
#            logger.debug(f'clear HA discovery topic: {message.topic}')
#            self.client.publish(message.topic, None, 0, True)

    def clear_ha_discovery_topic(self):
        # Just to clean up old retained messages in discovery topic
        logger = logging.getLogger(__name__)

        if self.flag_connected == 0:
            logger.warning("not connected")
            return
        logger.info('Purge old Homeassistant discovery topic')
        logger.debug('Subscribe to discovery topic')
        self.client.subscribe(f"{config.hassio['mqtt_broker_hassio_discovery_queue']}/#")
        time.sleep(1)
        self.client.publish(f"{config.hassio['mqtt_broker_hassio_discovery_queue']}", None, 0, True)
        logger.debug('Unsubscribe to discovery topic')
        self.client.unsubscribe(f"{config.hassio['mqtt_broker_hassio_discovery_queue']}/#")
        exit
        return