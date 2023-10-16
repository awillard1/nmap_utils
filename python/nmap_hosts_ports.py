import xml.etree.ElementTree as ET
import argparse

class HostPort:
    def __init__(self, address, ports):
        self.address = address
        self.ports = ports

def parse_nmap_xml(filepath):
    tree = ET.parse(filepath)
    hosts = tree.findall("host")
    host_ports = []
    for host in hosts:
        if host.find("status").attrib["state"] == "up":
            address = host.find("address").attrib["addr"]
            ports = [port.attrib["portid"] for port in host.findall("ports/port")]
            host_ports.append(HostPort(address, ports))
    return host_ports

def main():
    host_ports = parse_nmap_xml(filepath)
    for host_port in host_ports:
        for port in host_port.ports:
            print(f"{host_port.address}:{port}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", type=str, help="Path to XML file from nmap results")
    args = parser.parse_args()
    if (args.filepath):
        filepath = args.filepath
        main()
