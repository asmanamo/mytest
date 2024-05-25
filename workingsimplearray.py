def combine_arrays(config_file, port_mappings):
    """
    Combine the two arrays `config_file` and `port_mappings` into a single output array.

    Args:
        config_file (list): A list of strings representing configuration data.
        port_mappings (list): A list of strings representing port mapping data.

    Returns:
        list: A list of strings representing the combined output.
    """
    output = []
    #if len(config_file) != len(port_mappings):
     #   return ["invalid_arguments_given"]

    for i in range(len(config_file)):
        if config_file[i].startswith("__") and config_file[i].endswith("__"):
            # This is a header, add it to the output
            output.append(config_file[i])
        elif ":" in config_file[i] and i < len(port_mappings) and ":" in port_mappings[i]:
            # This is a key-value pair, split it and combine with the port mapping
            config_key, config_value = config_file[i].split(":")
            port_mapping_key, port_mapping_value = port_mappings[i].split(":")
            new_key = f"{port_mapping_value.strip()}: {config_key.strip()}"
            new_value = config_value.strip()
            output.append(f"{new_key}={new_value}")
        else:
            # Skip this element, as it doesn't follow the expected format
            continue

    return output

config_file = [
            "__10.1.1.1|10.2.2.2__",
            "portA:enabledetrue",
            "portB: vlan=10",
            "portC:vian=200",
            "__10.3.3.3__",
            "portA:poe=false",
            "portA: speed=100mbps",
            "portB:vlan=15"
        ]

port_mappings = [
            "__10.1.1.1|10.2.2.2__ ",
            "portA:member1_port3",
            "portB:member2_port27",
            "portC:member2_port14",
            "__10.3.3.3__",
            "portA:port4",
            "portB:port15"
        ]

print("config_file:", config_file)
print("port_mappings:", port_mappings)
output = combine_arrays(config_file, port_mappings)
print("ouput is ##################################",output)
