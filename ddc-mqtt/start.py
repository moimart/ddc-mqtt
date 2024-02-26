from mqtt_client import MQTTClient
from timer import Timer
from timeit import default_timer as timer
import yaml
import os
import json
from devices import display_device, display_input_entity, hass_display_sensor

class Service:
    def __init__(self):
        self.dt = 0
        
        try:
            with open("config.yaml","r") as config:
                config = yaml.safe_load(config)
        except Exception as e:
            with open("rename_to_config.yaml","r") as config:
                config = yaml.safe_load(config)
                
        self.mqtt = MQTTClient(config["mqtt"]["username"],
                                config["mqtt"]["password"],
                                config["mqtt"]["host"],
                                config["mqtt"]["port"])
        
        self.inputs = {}
        display_data = config['display']

        self.inputs[display_data['id']]['switches'] = []
        
        for input_name, input_code in display_data['inputs'].items():
            self.create_display_switch(display_data['id'],input_name,input_code)
            
        self.update_inputs_states()
        self.timer = Timer(120, self)
        
    def update_inputs_states(self):
        #check what input is on by getting the code from simpleddc
        #change the state of only that input
        pass
            
    def on_message(self, topic, payload):
        if payload =='OFF':
            return #do nothing
        
        if "command" in topic:
            self.activate_input_deactivate_rest(self.inputs[topic.split("/")[2]],topic.split("/")[3])
            
    def activate_input_deactivate_rest(display_id,display_name):
        #check if this input is already on. if so, return
        #if not, switch display to this input, set rest of inputs to off
        pass
    
    def on_timer(self, timer, elapsed):
        #check input states
        self.timer.reset()
        self.timer.active = True
    
    def step(self, dt):
        self.timer.step(dt)
        self.mqtt.step(dt)

    def create_display_switch(self, display_id, input_name, input_code):
        topic = display_input_entity["generic_switch"]
        topic = topic.replace("#", display_id)
        topic = topic.replace("?", input_name)

        config = display_input_entity["generic_switch_config"].copy()
        config["unique_id"] = "{}_{}_switch".format(display_id,input_name)
        config["object_id"] = "{}_{}_switch".format(display_id,input_name)
        config["name"] = input_name
        config["state_topic"] = config["state_topic"].replace("#", id)
        config["state_topic"] = config["state_topic"].replace("?", input_name)

        device = display_device.copy()
        device["name"] = device["name"].replace("#", input_name)
        device["model"] = "{}-{}".format(device["model"],id)
        config["device"] = device

        config["command_topic"] = config["command_topic"].replace("#", id)
        config["command_topic"] = config["command_topic"].replace("?", input_name)

        self.mqtt.client.publish(config["state_topic"], "off")
        self.mqtt.client.publish(topic, json.dumps(config), retain=True)

        self.mqtt.client.subscribe(config["command_topic"])

        self.inputs[display_id]["switches"].append({"id": input_name, "topic": topic, "config": config, "code": input_code})
        
    def start(self):
        while True:
            t0 = timer()
            self.step(self.dt)
            t1 = timer()
            self.dt = t1 - t0

            