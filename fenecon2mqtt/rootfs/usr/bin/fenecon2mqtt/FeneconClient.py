#!/usr/bin/python3
import json
import logging
import os
import time
import uuid
import threading
import queue

import config
import websocket
from jsonrpcclient import request_json
from publish_hassio_discovery import publish_hassio_discovery


class FeneconClient:
    def __init__(self, mqtt):
        self.logger = logging.getLogger(__name__)
        self.logger.info('Init')
        self.mqtt = mqtt
        self.queue = queue.Queue()
        self.version = None

        # IDs
        self.uuid_str_auth = str(uuid.uuid4())
        self.uuid_str_getEdge = str(uuid.uuid4())
        self.uuid_str_getEdgeConfig_payload = str(uuid.uuid4())
        self.uuid_str_getEdgeConfig_request = str(uuid.uuid4())
        self.uuid_str_subscribe_payload = str(uuid.uuid4())
        self.uuid_str_subscribe_request = str(uuid.uuid4())

        # JSON-RPCs
        self.json_auth_passwd = request_json("authenticateWithPassword",
            params={"password": config.fenecon['fems_password']}, id=self.uuid_str_auth)
        self.json_get_edge = request_json("getEdge",
            params={"edgeId": "0"}, id=self.uuid_str_getEdge)
        self.json_get_edgeconfig_payload = request_json("getEdgeConfig",
            params={" ": " "}, id=self.uuid_str_getEdgeConfig_payload)
        self.json_get_edgeconfig_req = request_json("edgeRpc",
            params={"edgeId": "0", "payload": json.loads(self.json_get_edgeconfig_payload)},
            id=self.uuid_str_getEdgeConfig_request)
        self.json_subscribe_payload = request_json("subscribeChannels",
            params={"count": "0", "channels": config.channels2subscribe},
            id=self.uuid_str_subscribe_payload)
        self.json_subscribe_req = request_json("edgeRpc",
            params={"edgeId": "0", "payload": json.loads(self.json_subscribe_payload)},
            id=self.uuid_str_subscribe_request)

        threading.Thread(target=self.process_messages, daemon=True).start()
        threading.Thread(target=self.connect_websocket, daemon=True).start()

        # Keep the addon alive
        while True:
            time.sleep(60)

    def is_docker(self):
        return os.path.exists('/.dockerenv')

    def connect_websocket(self):
        self.logger.info('Connect to Fenecons websocket')
        ws_uri = f"ws://{config.fenecon['fems_ip']}:8085/websocket"
        self.ws = websocket.WebSocketApp(
            ws_uri,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.run_forever()

    def on_open(self, ws):
        logger = self.logger
        logger.debug('WebSocket opened')
        ws.send(self.json_auth_passwd)
        time.sleep(0.5)
        ws.send(self.json_get_edge)
        time.sleep(0.5)
        ws.send(self.json_get_edgeconfig_req)
        time.sleep(0.5)
        ws.send(self.json_subscribe_req)

    def on_message(self, ws, message):
        self.queue.put(message)

    def process_messages(self):
        while True:
            try:
                message = self.queue.get()
                msg_dict = json.loads(message)
                msg_id = msg_dict.get('id')

                try:
                    msg_data = msg_dict['params']['payload']['params']
                except KeyError:
                    msg_data = None

                if msg_id is None and msg_data:
                    for key, value in msg_data.items():
                        hassio_uid = f"{config.hassio['sensor_uid_prefix']}{key}".replace("/", "-")
                        self.mqtt.publish(f"{config.hassio['mqtt_broker_hassio_queue']}/{hassio_uid}".lower(), str(value))

                elif msg_id == self.uuid_str_auth:
                    if msg_dict.get('error') is None:
                        self.logger.info("FEMS Authentication successfull")
                    else:
                        error_code = msg_dict['error']['code']
                        error_msg = msg_dict['error']['message']
                        self.logger.error(f"FEMS Authentication failed ({error_code}): {error_msg}")
                        time.sleep(5)
                        quit()

                elif msg_id == self.uuid_str_getEdge:
                    try:
                        self.version = msg_dict['result']['edge']['version']
                    except Exception:
                        self.version = "N/A"

                elif msg_id == self.uuid_str_getEdgeConfig_request:
                    self.mqtt.clear_ha_discovery_topic()
                    publish_hassio_discovery(self.mqtt, msg_dict, self.version)

                    if self.is_docker():
                        try:
                            with open('/share/fenecon/fenecon_config.json', 'w') as fp:
                                json.dump(msg_dict, fp)
                        except Exception:
                            self.logger.error("Could not dump Fenecon config to disk")

                self.queue.task_done()
            except Exception as e:
                self.logger.error(f"Exception in message handling: {e}")
            time.sleep(0.01)

    def on_error(self, ws, error):
        self.logger.error(f"WebSocket error: {error}")
        time.sleep(5)
        quit()

    def on_close(self, ws, code, msg):
        self.logger.warning(f"WebSocket closed: Code={code} Message={msg}")
        time.sleep(5)
        quit()
