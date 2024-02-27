device = {
    "identifiers": ["Kikkei Labs Display KVM"],
    "name": "Display KVM #?",
    "model": "Kikkei-display-kvm-0",
    "manufacturer": "Kikkei Labs",
}


display_device = {
    "identifiers": ["Input"],
    "name": "Display Input KVM #?",
    "model": "Kikkei-display-kvm",
    "manufacturer": "Kikkei Labs",
}

display_input_entity = {
    "generic_switch": 'homeassistant/switch/display-kvm-#/?-switch/config',
    "generic_switch_config": {
        "availability_topic": "kikkei/display-kvm/availability",
        "state_topic": "kikkei/display-kvm/#/?/state",
        "name": "",
        "unique_id": "",
        "object_id": "",
        "payload_available": "online",
        "payload_not_available": "offline",
        #"json_attributes_topic": "kikkei/household/#/%/attributes",
        "state_on": "true",
        "state_off": "false",
        "command_topic": "kikkei/display-kvm/#/?/command",
        "device": display_device
    }
}
