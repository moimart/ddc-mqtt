from mqtt_client import MQTTClient
from timer import Timer
from timeit import default_timer as timer
import yaml
import os
import json

class Service:
    def __init__(self):
        try:
            with open("config.yaml","r") as config:
                config = yaml.safe_load(config)
        except Exception as e:
            with open("rename_to_config.yaml","r") as config:
                config = yaml.safe_load(config)
                
        if 'MQTT_HOST' in os.environ:
            self.mqtt = MQTTClient(os.environ['MQTT_USER'],
                                    os.environ['MQTT_PASSWORD'],
                                    os.environ['MQTT_HOST'],
                                    int(os.environ['MQTT_PORT']))
        else:
            self.mqtt = MQTTClient(config["mqtt"]["username"],
                                    config["mqtt"]["password"],
                                    config["mqtt"]["host"],
                                    config["mqtt"]["port"])