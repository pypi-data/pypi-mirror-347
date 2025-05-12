from scapy.all import ARP, Ether, srp

def arp_scan(target_ip):
    arp_request = ARP(pdst=target_ip)
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_packet = ether_frame / arp_request

    result = srp(arp_request_packet, timeout=3, verbose=False)[0]
    devices_list = []

    for sent, received in result:
        devices_list.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices_list

def print_scan_results(devices_list):
    print("IP Address\t\tMAC Address")
    print("-------------------------------------------")
    for device in devices_list:
        print(f"{device['ip']}\t\t{device['mac']}")

def main(target_ip):
    print(f"Scanning {target_ip}...")
    devices_list = arp_scan(target_ip)
    print_scan_results(devices_list)

if __name__ == '__main__':
    target_ip = input("Enter the target IP range ")
    main(target_ip)
