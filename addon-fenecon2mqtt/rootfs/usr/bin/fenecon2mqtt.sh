#!/usr/bin/with-contenv bashio
# shellcheck shell=bash
set -e
#TEST=$(bashio::config 'option1')
#echo "All done, new Version deployed!$TEST" > /share/example_addon_output.txt
#cp /data/options.json /share/options.json
#python3 --version > /share/python_version.txt
#pip3 --version > /share/pip_version.txt
python3 /usr/bin/fenecon2mqtt/Fenecon2Mqtt.py