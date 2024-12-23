import re

def parse_interface(output):
    parsed_data = []

    # Split the output by hosts
    host_blocks = re.split(r"ok: \[([^\]]+)\]", output)
    
    # Host blocks alternate: empty string, hostname, data
    for i in range(1, len(host_blocks), 2):
        hostname = host_blocks[i].strip()
        data = host_blocks[i + 1]

        # Extract lines with interface details
        lines = re.findall(r"^\s*([^\s]+)\s+([^\s]+)\s+YES\s+[^\s]+\s+(.+?)\s{2,}", data, re.MULTILINE)
        interface_list = []
        for line in lines:
            interface, ip_address, status = line
            interface = interface.strip('"')
            # Handle "administratively down"
            if "administratively down" in status:
                status = "administratively down"
            interface_list.append({
                "interface": interface,
                "detail": {
                    "ip_address": ip_address,
                    "status": status.strip()
                }
            })
        
        # Add the hostname with its interfaces
        parsed_data.append({
            "hostname": hostname,
            "interfaces": interface_list
        })
    
    return parsed_data