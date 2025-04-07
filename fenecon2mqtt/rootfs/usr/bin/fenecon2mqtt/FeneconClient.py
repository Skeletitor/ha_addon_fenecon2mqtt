#!/usr/bin/python3
import json
import logging
import os
import time
import uuid
from queue import Queue, Empty
from threading import Thread

import config
import websocket
from jsonrpcclient import request_json
from publish_hassio_discovery import publish_hassio_discovery


class FeneconClient:
    """
    A client for connecting to the Fenecon WebSocket and processing messages.
    """

    # Static UUIDs for requests
    uuid_str_auth = str(uuid.uuid4())
    uuid_str_getEdge = str(uuid.uuid4())
    uuid_str_getEdgeConfig_payload = str(uuid.uuid4())
    uuid_str_getEdgeConfig_request = str(uuid.uuid4())
    uuid_str_subscribe_payload = str(uuid.uuid4())
    uuid_str_subscribe_request = str(uuid.uuid4())

    # JSON request templates
    json_auth_passwd = request_json("authenticateWithPassword", params={"password": config.fenecon['fems_password']}, id=uuid_str_auth)
    json_get_edge = request_json("getEdge", params={"edgeId": "0"}, id=uuid_str_getEdge)
    json_get_edgeconfig_payload = request_json("getEdgeConfig", params={" ": " "}, id=uuid_str_getEdgeConfig_payload)
    json_get_edgeconfig_req = request_json("edgeRpc", params={"edgeId": "0", "payload": json.loads(json_get_edgeconfig_payload)}, id=uuid_str_getEdgeConfig_request)
    json_subscribe_payload = request_json("subscribeChannels", params={"count": "0", "channels": config.channels2subscribe}, id=uuid_str_subscribe_payload)
    json_subscribe_req = request_json("edgeRpc", params={"edgeId": "0", "payload": json.loads(json_subscribe_payload)}, id=uuid_str_subscribe_request)

    def __init__(self, mqtt):
        """
        Initialize the FeneconClient and connect to the WebSocket.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info('Initializing FeneconClient...')
        self.mqtt = mqtt
        self.message_queue = Queue()
        self.running = True

        # Start the message processing thread
        self.processing_thread = Thread(target=self.process_queue, daemon=True)
        self.processing_thread.start()

        # Connect to the WebSocket
        self.connect_websocket()

    def connect_websocket(self):
        """
        Connect to the Fenecon WebSocket with ping functionality in a dedicated thread.
        """
        self.logger.info('Connecting to Fenecon WebSocket...')
        ws_uri = f"ws://{config.fenecon['fems_ip']}:8085/websocket"

        def run_ws():
            try:
                ws = websocket.WebSocketApp(
                    ws_uri,
                    on_open=self.on_open,
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close
                )
                # Run the WebSocket with ping functionality
                ws.run_forever(ping_interval=30, ping_timeout=10)
            except Exception as e:
                self.logger.error(f"WebSocket connection failed: {e}")
                self.reconnect_websocket()

        # Start the WebSocket in a dedicated thread
        websocket_thread = Thread(target=run_ws, daemon=True)
        websocket_thread.start()

    def reconnect_websocket(self):
        """
        Attempt to reconnect to the WebSocket with a delay.
        """
        self.logger.info("Reconnecting to WebSocket in 5 seconds...")
        time.sleep(5)  # Wait before attempting to reconnect
        self.connect_websocket()

    def on_message(self, ws, message):
        """
        Callback for receiving messages from the WebSocket.
        """
        self.message_queue.put(message)

    def process_queue(self):
        """
        Process messages from the queue in batches.
        """
        while self.running:
            try:
                batch = []
                start_time = time.time()

                # Collect messages for up to 100ms or until the queue is empty
                while time.time() - start_time < 0.1:
                    try:
                        message = self.message_queue.get(timeout=0.05)
                        batch.append(message)
                    except Empty:
                        break

                # Process the batch
                for message in batch:
                    self._process_message(message)

                # Mark tasks as done
                for _ in batch:
                    self.message_queue.task_done()

                # Sleep briefly if the queue is empty
                if not batch:
                    time.sleep(0.05)
            except Exception as e:
                self.logger.error(f"Error processing message queue: {e}")

    def _process_message(self, message):
        """
        Process a single message from the WebSocket.
        """
        try:
            msg_dict = json.loads(message)
            msg_id = msg_dict.get('id')
            msg_current_data = msg_dict.get('params', {}).get('payload', {}).get('params')

            if msg_id is None and msg_current_data:
                # Process subscribed data
                for key, value in msg_current_data.items():
                    hassio_uid = f"{config.hassio['sensor_uid_prefix']}{key}".replace("/", "-")
                    self.mqtt.publish(f"{config.hassio['mqtt_broker_hassio_queue']}/{hassio_uid}".lower(), str(value))
            elif msg_id == self.uuid_str_auth:
                self._handle_auth_response(msg_dict)
            elif msg_id == self.uuid_str_getEdge:
                self._handle_get_edge_response(msg_dict)
            elif msg_id == self.uuid_str_getEdgeConfig_request:
                self._handle_edge_config_response(msg_dict)
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")

    def _handle_auth_response(self, msg_dict):
        """
        Handle the response to the authentication request.
        """
        if msg_dict.get('error') is None:
            self.logger.info("FEMS Authentication successful.")
        else:
            error_code = msg_dict['error']['code']
            error_msg = msg_dict['error']['message']
            self.logger.error(f"FEMS Authentication failed. Error ({error_code}): {error_msg}")
            self.shutdown()

    def _handle_get_edge_response(self, msg_dict):
        """
        Handle the response to the getEdge request.
        """
        self.logger.info("getEdge response received.")
        try:
            self.version = msg_dict['result']['edge']['version']
        except KeyError:
            self.version = "N/A"

    def _handle_edge_config_response(self, msg_dict):
        """
        Handle the response to the getEdgeConfig request.
        """
        self.logger.info("EdgeConfig response received. Clearing old Home Assistant discovery topics.")
        self.mqtt.clear_ha_discovery_topic()
        self.logger.info("Publishing new Home Assistant discovery topics.")
        publish_hassio_discovery(self.mqtt, msg_dict, self.version)

        if self.is_docker():
            self.logger.info("Dumping Fenecon configuration to local Docker filesystem.")
            try:
                with open('/share/fenecon/fenecon_config.json', 'w') as fp:
                    json.dump(msg_dict, fp)
            except Exception as e:
                self.logger.error(f"Failed to dump Fenecon configuration: {e}")

    def on_error(self, ws, error):
        """
        Callback for WebSocket errors.
        """
        self.logger.error(f"WebSocket error: {error}")
        self.logger.info("Attempting to reconnect...")
        self.reconnect_websocket()

    def on_close(self, ws, close_status_code, close_msg):
        """
        Callback for WebSocket closure.
        """
        self.logger.warning(f"WebSocket closed. Code: {close_status_code}, Message: {close_msg}")
        self.logger.info("Attempting to reconnect...")
        self.reconnect_websocket()

    def on_open(self, ws):
        """
        Callback for WebSocket opening.
        """
        self.logger.info("WebSocket connection opened. Sending authentication request.")
        ws.send(self.json_auth_passwd)
        time.sleep(0.5)
        ws.send(self.json_get_edge)
        time.sleep(0.5)
        ws.send(self.json_get_edgeconfig_req)
        time.sleep(0.5)
        ws.send(self.json_subscribe_req)

    def is_docker(self):
        """
        Check if the application is running in a Docker container.
        """
        return os.path.exists('/.dockerenv') or any('docker' in line for line in open('/proc/self/cgroup', 'r'))

    def shutdown(self):
        """
        Cleanly shut down the client.
        """
        self.logger.info("Shutting down FeneconClient...")
        self.running = False
        self.processing_thread.join(timeout=5)
        time.sleep(5)
        quit()