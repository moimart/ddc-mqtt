from mqtt_client import MQTTClient
from timer import Timer
from timeit import default_timer as timer
import yaml
import os
import json
from devices import display_device, display_input_entity
import simpleddc

class Service:
    def __init__(self):
        self.dt = 0
        
        try:
            with open("config.yml","r") as config:
                config = yaml.safe_load(config)
        except Exception as e:
            with open("rename_to_config.yml","r") as config:
                config = yaml.safe_load(config)
                
        self.mqtt = MQTTClient(config["mqtt"]["username"],
                                config["mqtt"]["password"],
                                config["mqtt"]["host"],
                                config["mqtt"]["port"])
        
        poll_interval = 20 if "interval" not in config else config["interval"]
        
        self.mqtt.delegate = self
        
        self.inputs = {}
        display_data = config['display']
        
        print(display_data)

        self.inputs = {}
        
        for display in display_data:
            self.inputs[display['id']] = { "switches": [] }
            for input_name, input_code in display['inputs'].items():
                self.create_display_switch(display['id'],input_name,input_code)
            
        self.timer = Timer(poll_interval, self)
        self.update_inputs_states()
        
    def update_inputs_states(self):
        for display_id in self.inputs.keys():
            input_code = simpleddc.show_input(int(display_id))
        
            print(f"Input code is {input_code}")
            
            for entry in self.inputs[display_id]["switches"]:
                if entry["code"] == input_code:
                    self.mqtt.client.publish(entry["topic"], "true")
                    entry["state"] = True
                else:
                    self.mqtt.client.publish(entry["topic"], "false")
                    entry["state"] = False
            
    def on_message(self, topic, payload):
        if payload =='OFF':
            return #do nothing
        
        if "command" in topic:
            self.activate_input_deactivate_rest(int(topic.split("/")[2]),topic.split("/")[3])
            
    def activate_input_deactivate_rest(self, display_id,display_input):
        print(f"Display {display_id} name {display_input}")
        
        for entry in self.inputs[display_id]["switches"]:
            if entry["id"] == display_input:
                entry["state"] = True
                self.mqtt.client.publish(entry["topic"], "true")
                print(f'switching to {entry["code"]}')
                simpleddc.switch_to_input(display_id, int(entry["code"]))
                
            else:
                entry["state"] = False
                self.mqtt.client.publish(entry["topic"], "false")
            
    def on_timer(self, timer, elapsed):
        #check input states
        self.timer.reset()
        self.timer.active = True
        self.update_inputs_states()
    
    def step(self, dt):
        self.timer.step(dt)
        self.mqtt.step(dt)

    def create_display_switch(self, display_id, input_name, input_code):
        topic = display_input_entity["generic_switch"]
        topic = topic.replace("#", str(display_id))
        topic = topic.replace("?", input_name)

        config = display_input_entity["generic_switch_config"].copy()
        config["unique_id"] = "{}_{}_switch".format(display_id,input_name)
        config["object_id"] = "{}_{}_switch".format(display_id,input_name)
        config["name"] = input_name
        config["state_topic"] = config["state_topic"].replace("#", str(display_id))
        config["state_topic"] = config["state_topic"].replace("?", input_name)

        device = display_device.copy()
        device["name"] = device["name"].replace("?", input_name)
        device["model"] = "{}-{}".format(device["model"],display_id)
        config["device"] = device

        config["command_topic"] = config["command_topic"].replace("#", str(display_id))
        config["command_topic"] = config["command_topic"].replace("?", input_name)

        self.mqtt.client.publish(config["availability_topic"],"online", retain=True)
        self.mqtt.client.publish(config["state_topic"], "off")
        self.mqtt.client.publish(topic, json.dumps(config), retain=True)

        self.mqtt.client.subscribe(config["command_topic"])

        self.inputs[display_id]["switches"].append({"id": input_name, "topic": config["state_topic"], "config": config, "code": input_code, "state": False})
        
    def start(self):
        while True:
            t0 = timer()
            self.step(self.dt)
            t1 = timer()
            self.dt = t1 - t0

service = Service()
service.start()