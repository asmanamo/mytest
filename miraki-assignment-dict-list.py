def combine_arrays(config_file, port_mappings):
    result = []

    if not isinstance(config_file, list) or not isinstance(port_mappings, list):
        return ["invalid_arguments_given"]

    # Create a dictionary to store port mappings by header and port
    port_mappings_dict = {}
    current_header = None
    for item in port_mappings:
        if item.startswith("__"):
            current_header = item
            port_mappings_dict[current_header] = {} 
        elif current_header:
            try:
                port_key, port_value = item.split(":")
                port_mappings_dict[current_header][port_key.strip()] = port_value.strip()
            except ValueError:
                return ["invalid_arguments_given"]

    i = 0
    while i < len(config_file):
        config_line = config_file[i]
        if config_line.startswith("__"):
            # This is a header, add it to the output
            current_header = config_line
            result.append(current_header)  # Add header to the result list
            i += 1
        elif ":" in config_line:
            try:
                config_key, config_value = config_line.split(":")
            except ValueError:
                return ["invalid_arguments_given"]

            # Find the corresponding port mapping for this header and port
            current_port_mappings = port_mappings_dict.get(current_header)
            if not current_port_mappings:
                return ["invalid_arguments_given"] 

            port_mapping_value = current_port_mappings.get(config_key.strip())
            if port_mapping_value is not None:
                new_key = port_mapping_value
                new_value = config_value.strip()
                result.append(f"{new_key}:{new_value}")

            i += 1
        else:
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
    "__10.3.3.3__", 
    "portB:port15",
    "portA:port4",
    "__Spine300__",
    "portA:port40",
    "portB:port5",
    "__device100__",
    "portA:member1_port3",
    "portB:member2_port27",
    "portC:member2_port14"
]

output = combine_arrays(config_file, port_mappings)
print('\n'.join(output))
