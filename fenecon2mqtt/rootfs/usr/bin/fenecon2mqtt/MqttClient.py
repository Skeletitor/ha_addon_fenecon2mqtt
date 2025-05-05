#!/usr/bin/python3
import logging
import time
import threading
import os
import config
import paho.mqtt.client as mqtt


class MqttClient:
    def __init__(self):
        """
        Initialize the MQTT client and connect to the broker.
        """
        self.logger = logging.getLogger(__name__)
        self.flag_connected = threading.Event()  # Thread-safe connection flag
        self.client = None
        self._connect_to_broker()

    def _connect_to_broker(self):
        """
        Connect to the MQTT broker. Exit program on failure.
        """
        self.logger.info("Attempting to connect to MQTT broker")
        try:
            self.client = mqtt.Client(client_id="Fenecon2Hassio_mqttClient", clean_session=True)
            self.client.username_pw_set(config.hassio['mqtt_broker_user'], config.hassio['mqtt_broker_passwd'])
            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            self.client.on_log = self._on_log
            self.client.on_message = self._on_message

            self.client.connect(
                config.hassio['mqtt_broker_host'],
                config.hassio['mqtt_broker_port'],
                config.hassio['mqtt_broker_keepalive']
            )
            self.client.loop_start()
            time.sleep(1)  # Allow time for connection
        except Exception as e:
            self.logger.error(f"Failed to connect to MQTT broker: {e}")
            time.sleep(-1)  # Brief pause for logging
            os._exit(0)

    def _on_connect(self, client, userdata, flags, reason_code):
        """
        Callback for successful connection to the MQTT broker.
        """
        if reason_code == 0:
            self.logger.info("Successfully connected to MQTT broker.")
            self.flag_connected.set()
            client.subscribe("$SYS/#")  # Example subscription
        else:
            self.logger.error(f"Connection failed with reason code: {mqtt.connack_string(reason_code)}")
            time.sleep(1)  # Brief pause for logging
            os._exit(0)

    def _on_disconnect(self, client, userdata, reason_code):
        """
        Callback for disconnection from the MQTT broker. Exit program immediately.
        """
        self.logger.error(f"Disconnected from MQTT broker. Reason: {mqtt.connack_string(reason_code)}")
        self.flag_connected.clear()
        time.sleep(1)  # Brief pause for logging
        os._exit(0)

    def publish(self, topic, payload, qos=0, retain=False):
        """
        Publish a message to the MQTT broker.

        Args:
            topic (str): The topic to publish to.
            payload (str): The message payload.
            qos (int): The Quality of Service level.
            retain (bool): Whether the message should be retained.
        """
        if self.flag_connected.is_set():
            self.logger.debug(f"Publishing to topic '{topic}': {payload}")
            self.client.publish(topic, payload, qos, retain)
        else:
            self.logger.warning("Cannot publish message. MQTT client is not connected.")

    def _on_log(self, client, userdata, level, buf):
        """
        Callback for MQTT client logging.
        """
        self.logger.debug(f"MQTT Log - Level: {level}, Message: {buf}")

    def _on_message(self, client, userdata, message):
        """
        Callback for received MQTT messages.
        """
        self.logger.debug(f"Received message on topic '{message.topic}': {message.payload.decode()}")
        if message.retain and message.topic.startswith(config.hassio['mqtt_broker_hassio_discovery_queue']):
            if message.topic == "homeassistant/sensor/fenecon/config":
                return
            self.logger.debug(f"Clearing retained message on topic: {message.topic}")
            self.client.publish(message.topic, None, 0, True)

    def clear_ha_discovery_topic(self):
        """
        Clear retained messages in the Home Assistant discovery topic.
        """
        if not self.flag_connected.is_set():
            self.logger.warning("Cannot clear discovery topic. MQTT client is not connected.")
            return

        self.logger.info("Clearing old Home Assistant discovery topics.")
        self.client.subscribe(f"{config.hassio['mqtt_broker_hassio_discovery_queue']}/#")
        time.sleep(3)  # Allow time for messages to be received
        self.client.unsubscribe(f"{config.hassio['mqtt_broker_hassio_discovery_queue']}/#")
        self.logger.info("Discovery topics cleared.")

    def disconnect(self):
        """
        Disconnect the MQTT client and stop the loop.
        """
        if self.client:
            self.logger.info("Disconnecting MQTT client.")
            self.client.loop_stop()
            self.client.disconnect()