def combine_arrays(config_file, port_mappings):
    result = []
    port_mapping_index = 0
    
    if not isinstance(config_file, list) or not isinstance(port_mappings, list):
        return ["invalid_arguments_given"]

    i = 0
    while i < len(config_file):
        config_line = config_file[i]
        if config_line.startswith("__"):
            # This is a header, add it to the output
            result.append(config_line)
            port_mapping_index += 1
            i += 1
        elif ":" in config_line and port_mapping_index < len(port_mappings) and ":" in port_mappings[port_mapping_index]:
            # This is a key-value pair, split it and combine with the port mapping
            #config_key, config_value = config_line.split(":")
            #port_mapping_key, port_mapping_value = port_mappings[port_mapping_index].split(":")
            try:
               config_key, config_value = config_line.split(":")
               port_mapping_key, port_mapping_value = port_mappings[port_mapping_index].split(":")
            except ValueError:
               return ["invalid_arguments_given"]    

            new_key = port_mapping_value.strip()
            new_value = config_value.strip()
            result.append(f"{new_key}:{new_value}")

            # Check if the next line also belongs to the same port mapping
            if i + 1 < len(config_file) and not config_file[i + 1].startswith("__"):
                next_config_key = config_file[i + 1].split(":")[0]
                if next_config_key == config_key:
                    # Use the same port mapping for the next configuration
                    i += 1
                    continue
            
            port_mapping_index += 1
            i += 1
        else:
            # Skip this element, as it doesn't follow the expected format
            return ["invalid_arguments_given"]

    return result

config_file = [
    "__device100__",
    "portA:enabledetrue",
    "portB: vlan=10",
    "portC:vian=200",
    "__10.3.3.3__",
    "portA:poe=false",
    "portA: speed=100mbps",
    "portB:vlan=15",
    "__Spine300__",
    "portA: poe=false",
    "portA: speed=100mbps",
    "portB:vlan=15"
]

port_mappings = [
    "__device100__",
    "portA:member1_port3",
    "portB:member2_port27",
    "portC:member2_port14",
    "__10.3.3.3__",
    "portA:port4",
    "portB:port15",
    "__Spine300__",
    "portA:port40",
    "portB:port5"
]

output = combine_arrays(config_file, port_mappings)
print('\n'.join(output))
