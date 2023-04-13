#!/usr/bin/python3
import config
import paho.mqtt.client as mqtt

class HassioMqttClient:
    flag_connected = 0

    def __init__(self):
        self.client = mqtt.Client("Fenecon2Hassio")
        self.client.username_pw_set(config.hassio['mqtt_broker_user'], config.hassio['mqtt_broker_passwd'])
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(config.hassio['mqtt_broker_host'], config.hassio['mqtt_broker_port'], config.hassio['mqtt_broker_keepalive'])
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("HassioMqttClient: on_connect")
        self.flag_connected = 1

    def on_disconnect(self, client, userdata, rc):
        print("HassioMqttClient: on_disconnect")
        self.flag_connected = 0

    def publish(self, *args, **kwargs):
        if self.flag_connected == 1:
            #print("HassioMqttClient: publish - connected")
            self.client.publish(*args, **kwargs)
        #else:
            # Wait to reconnect
        #    print("HassioMqttClient: publish - NOT connected")
