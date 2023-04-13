#!/usr/bin/python3
import config
from FeneconClientSocket import FeneconClientSocket
from HassioMqttClient import HassioMqttClient

def main():
    # Connect to Hassio integrated MQTT
    mqtt = HassioMqttClient()

    # start connect to Fenecon websocket
    s = FeneconClientSocket(mqtt)

if __name__ == "__main__":
    main()