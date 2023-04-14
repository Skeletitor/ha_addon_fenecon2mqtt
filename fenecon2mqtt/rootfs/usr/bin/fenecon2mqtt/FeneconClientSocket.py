#!/usr/bin/python3
import websocket
import config
import rel
import json
import uuid
import time
from jsonrpcclient import Ok, parse_json, request_json
from publish_hassio_discovery import publish_hassio_discovery

class FeneconClientSocket:
    version = ''
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
        self.mqtt = mqtt
        self.opened = False
        #ws://<<IP of Fenecon Home>>:8085/websocket
        # str(f"fems-{key}")
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
        #print("*** on message ***")
        msg_dict = json.loads(message)

        msg_id = msg_dict.get('id')
        msg_curent_data = None
        #msg_dict.get('params'],{}).get('payload', {}).get('method')

        try:
            msg_curent_data = msg_dict['params']['payload']['params']
        except KeyError:
            msg_curent_data = None

        if msg_dict.get('id') is None and msg_curent_data:
            #print(msg_curent_data)
            keys = list(msg_curent_data.keys())
            for key in keys:
                self.mqtt.publish(config.hassio['mqtt_broker_hassio_queue']+ "/" + str(f"fems-{key}").replace("/", "_"), str(msg_curent_data[key]))

        elif msg_id == self.uuid_str_auth:
            return
        elif msg_id == self.uuid_str_getEdge:
            self.version = msg_dict['result']['edge']['version']
            return
        elif msg_id == self.uuid_str_getEdgeConfig_request:
            print(" ** Edgeconfig -> trigger Hassio discovery ** ")
            publish_hassio_discovery(self.mqtt, msg_dict, self.version)
            return

    def on_error(self, ws, error):
        print("FeneconClientSocket: on_error")
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("FeneconClientSocket: on_close")
        rel.abort()
        self.ws.run_forever(dispatcher=rel)
        rel.signal(2, rel.abort)
        rel.dispatch()

    def on_open(self, ws):
        print("FeneconClientSocket: on_open")
        #time.sleep(1)
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