#!/usr/bin/python3
import websocket
import config
import rel
import json
import uuid
import time
from jsonrpcclient import Ok, parse_json, request_json
from publish_hassio_discovery import publish_hassio_discovery
import logging
import os

class FeneconClientSocket:
    version = None
    # Static uuids for request
    uuid_str_auth = str(uuid.uuid4())
    uuid_str_getEdge = str(uuid.uuid4())
    uuid_str_getEdgeConfig_payload = str(uuid.uuid4())
    uuid_str_getEdgeConfig_request = str(uuid.uuid4())
    uuid_str_subscribe_payload = str(uuid.uuid4())
    uuid_str_subscribe_request = str(uuid.uuid4())

    # JSON request templates
    json_auth_passwd = request_json("authenticateWithPassword", params={"password":config.fenecon['fems_password']}, id=uuid_str_auth)
    json_get_edge = request_json("getEdge", params={"edgeId":"0"}, id=uuid_str_getEdge)
    json_get_edgeconfig_payload = request_json("getEdgeConfig", params={" ": " "}, id=uuid_str_getEdgeConfig_payload)
    json_get_edgeconfig_req = request_json("edgeRpc", params={"edgeId":"0", "payload":json.loads(json_get_edgeconfig_payload)}, id=uuid_str_getEdgeConfig_request)
    json_subscribe_payload = request_json("subscribeChannels", params={"count":"0", "channels":config.fenecon['fems_request_channels']}, id=uuid_str_subscribe_payload)
    json_subscribe_req = request_json("edgeRpc", params={"edgeId":"0", "payload":json.loads(json_subscribe_payload)}, id=uuid_str_subscribe_request)

    def __init__(self, mqtt):
        logger = logging.getLogger(__name__)
        self.mqtt = mqtt
        #self.opened = False
        self.connect_retry_counter = 0
        self.connect_retry_max = 10
        self.connect_websocket()

    def is_docker(self):
        path = '/proc/self/cgroup'
        return (
            os.path.exists('/.dockerenv') or
            os.path.isfile(path) and any('docker' in line for line in open(path))
        )

    def connect_websocket(self):
        #ws://<<IP of Fenecon Home>>:8085/websocket
        ws_uri = str(f"ws://{config.fenecon['fems_ip']}:8085/websocket")
        self.ws = websocket.WebSocketApp(ws_uri ,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.run_forever(dispatcher=rel)

        rel.signal(2, rel.abort)  # Keyboard Interrupt
        rel.dispatch()

    def on_message(self, ws, message):
        logger = logging.getLogger(__name__)
        logger.debug("on_message")
        msg_dict = json.loads(message)

        msg_id = msg_dict.get('id')
        msg_curent_data = None
        #msg_dict.get('params'],{}).get('payload', {}).get('method')

        try:
            msg_curent_data = msg_dict['params']['payload']['params']
        except KeyError:
            msg_curent_data = None

        if msg_dict.get('id') is None and msg_curent_data:
            # process subscribed data
            keys = list(msg_curent_data.keys())
            for key in keys:
                hassio_uid = str(f"{config.hassio['sensor_uid_prefix']}{key}").replace("/", "-")
                self.mqtt.publish(config.hassio['mqtt_broker_hassio_queue']+ "/" + hassio_uid, str(msg_curent_data[key]))

        elif msg_id == self.uuid_str_auth:
            # process authorization reqest
            return
        elif msg_id == self.uuid_str_getEdge:
            # process edge data
            self.version = msg_dict['result']['edge']['version']
            return
        elif msg_id == self.uuid_str_getEdgeConfig_request:
            # process edge configuration data
            logger.info("Edgeconfig -> trigger Hassio discovery")
            publish_hassio_discovery(self.mqtt, msg_dict, self.version)
            if self.is_docker():
                logger.info("Dump Fenecon configration to local docker filesystem")
                try:
                    with open('/share/fenecon/fenecon_config.json', 'w') as fp:
                        json.dump(msg_dict, fp)
                except Exception:
                    logger.error("Dump Fenecon configration to local docker filesystem failed")
            return

    def on_error(self, ws, error):
        logger = logging.getLogger(__name__)
        logger.error(f'Fenecon connection error: {error}')

    def on_close(self, ws, close_status_code, close_msg):
        logger = logging.getLogger(__name__)
        logger.warning(f'Fenecon sonnection closed. Code:    {close_status_code}')
        logger.warning(f'                           Message: {close_msg}')
        logger.warning('try again in 30 seconds')
        time.sleep(30)
        self.connect_retry_counter += 1
        if self.connect_retry_max >= self.connect_retry_counter:
            logger.warning(f'Trying to connect ({self.connect_retry_counter}/{self.connect_retry_max}). Fenecon not reachable. Check availability and config.')
            logger.warning(f'  Fenecon IP    : {config.fenecon["fems_ip"]}')
            self.connect_websocket()
        else:
            logger.error('Fenecon not reachable. Exit!')
            quit()
        #rel.abort()
        #self.ws.run_forever(dispatcher=rel)
        #rel.signal(2, rel.abort)
        #rel.dispatch()

    def on_open(self, ws):
        logger = logging.getLogger(__name__)
        logger.info('Fenecon open connection and subscribe')
        self.connect_retry_counter = 0
        # auth
        self.ws.send(self.json_auth_passwd)
        time.sleep(0.5)
        # get edge
        self.ws.send(self.json_get_edge)
        time.sleep(0.5)
        # get edgeConfig
        self.ws.send(self.json_get_edgeconfig_req)
        time.sleep(0.5)
        # Subscribe
        self.ws.send(self.json_subscribe_req)