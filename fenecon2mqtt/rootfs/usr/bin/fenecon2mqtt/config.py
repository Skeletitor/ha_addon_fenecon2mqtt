#!/usr/bin/python3
import json

data = None

try:
    with open('/data/options.json') as file:
        data = json.load(file)
except e:
    with open('config.json') as file:
        data = json.load(file)

fenecon = data['fenecon']
hassio = data['hassio']
log_level = data['log_level']
