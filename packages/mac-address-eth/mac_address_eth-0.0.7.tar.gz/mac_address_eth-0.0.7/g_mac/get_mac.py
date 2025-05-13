import subprocess
import re
import psutil
import socket

MAC_ADDRESS_PATTERN = re.compile(r"GENERAL\.HWADDR:\s*((?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2})")
ETHERNET_SYMBOL = ['eth', 'enp', 'ens']

def get_network_interfaces_info():
    network_info = {}
    for interface, addrs in psutil.net_if_addrs().items():
        ip_addresses = []
        for addr in addrs:
            if addr.family == socket.AF_INET:  # IPv4 addresses
                ip_addresses.append(addr.address)
        if ip_addresses:
            network_info[interface] = ip_addresses
    return network_info

def get_interface_name(device_names, device_type):
    try:
        output = subprocess.check_output(
            ["nmcli", "-t", "-f", "DEVICE,TYPE", "device", "status"],
            universal_newlines=True
        )
        for line in output.strip().splitlines():
            parts = line.split(":")
            if len(parts) >= 2:
                device, dev_type = parts[0], parts[1]
                if dev_type.lower() == device_type and any([device.lower().startswith(n) for n in device_names]):
                    return device
    except Exception as e:
        print(f"get_interface_name - Error: {e}")
        return None

def get_ethernet_interface_name():
    return get_interface_name(device_names=ETHERNET_SYMBOL, device_type="ethernet")

def get_mac(interface_name):
    """Get the default mac address."""
    try:
        result = subprocess.run(
            ["nmcli", "device", "show", interface_name],
            capture_output=True,
            text=True)
        if result.returncode == 0:
            # lines = result.stdout.split('\n')
            r = MAC_ADDRESS_PATTERN.findall(result.stdout)
            if r:
                return r[0]
            else:
                return None
    except Exception as e:
        print(f"get_mac - Error: {e}")
        return None

def get_connection_type(interface):
    if any(prefix in interface.lower() for prefix in ETHERNET_SYMBOL):
        return "Ethernet"
    else:
        return None

def search_mac():
    try:
        for intf in get_network_interfaces_info().keys():
            conn_type = get_connection_type(intf)
            device_name = ""
            if conn_type == "Ethernet":
                device_name = get_ethernet_interface_name()
                if device_name:
                    if conn_type == 'Ethernet':
                        mac = get_mac(intf)
                        if mac:
                            return mac
        return ""
    except Exception as e:
        print(f"search_mac - Error: {e}")
        return None

if __name__ == "__main__":
    search_mac()
