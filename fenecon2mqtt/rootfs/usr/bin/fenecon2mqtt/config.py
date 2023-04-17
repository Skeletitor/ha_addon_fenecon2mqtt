#!/usr/bin/python3
import json
import os

data = None

try:
    with open('/data/options.json') as file:
        data = json.load(file)
except Exception:
    script_dir = os.path.dirname(__file__)
    rel_path = "./config.json"
    with open(os.path.join(script_dir, rel_path)) as file:
        data = json.load(file)

fenecon = data['fenecon']
hassio = data['hassio']
log_level = data['log_level']
