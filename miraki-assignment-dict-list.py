def combine_arrays(config_file, port_mappings):
    result = []

    if not isinstance(config_file, list) or not isinstance(port_mappings, list):
        return ["invalid_arguments_given"]

    # Create a dictionary to store port mappings by header
    port_mappings_dict = {}
    current_header = None
    for item in port_mappings:
        if item.startswith("__"):
            current_header = item
            port_mappings_dict[current_header] = []
        elif current_header:
            port_mappings_dict[current_header].append(item)

    i = 0
    while i < len(config_file):
        config_line = config_file[i]
        if config_line.startswith("__"):
            # This is a header
            current_header = config_line
            i += 1

            # Find the corresponding port mappings for this header
            current_port_mappings = port_mappings_dict.get(current_header)
            if not current_port_mappings:
                return ["invalid_arguments_given"]  # Header not found in port mappings
            port_mapping_index = 0

        elif ":" in config_line and current_port_mappings and port_mapping_index < len(current_port_mappings):
            try:
                config_key, config_value = config_line.split(":")
                port_mapping_key, port_mapping_value = current_port_mappings[port_mapping_index].split(":")
            except ValueError:
                return ["invalid_arguments_given"]

            new_key = port_mapping_value.strip()
            new_value = config_value.strip()
            result.append(f"{new_key}:{new_value}")

            # Check if the next line also belongs to the same port mapping
            if i + 1 < len(config_file) and not config_file[i + 1].startswith("__"):
                next_config_key = config_file[i + 1].split(":")[0]
                if next_config_key == config_key:
                    i += 1
                    continue

            port_mapping_index += 1
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
    "__10.3.3.3__", # Order Changed
    "portA:port4",
    "portB:port15",
    "__device100__",
    "portA:member1_port3",
    "portB:member2_port27",
    "portC:member2_port14",
    "__Spine300__",
    "portA:port40",
    "portB:port5",
]

output = combine_arrays(config_file, port_mappings)
print('\n'.join(output))
