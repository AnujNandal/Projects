# Import necessary libraries
from datetime import datetime
import scapy.all as scapy
from scapy.arch import get_windows_if_list
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import Counter
import time
import ipaddress
import platform

def sniff_packets(interface, count, timeout=None):
    """
    Capture network packets using Scapy.

    Args:
    interface (str): Network interface to sniff on.
    count (int): Number of packets to capture.
    timeout (float, optional): Time limit for packet capture in seconds.

    Returns:
    list: Captured packets.
    """
    return scapy.sniff(iface=interface, count=count, timeout=timeout)

def categorize_ip(ip):
    """
    Categorize an IP address as Private, Public, Multicast, or Other.

    Args:
    ip (str): IP address to categorize.

    Returns:
    str: Category of the IP address.
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private:
            return "Private"
        elif ip_obj.is_global:
            return "Public"
        elif ip_obj.is_multicast:
            return "Multicast"
        else:
            return "Other"
    except ValueError:
        return "Invalid"

def analyze_packets(packets):
    """
    Analyze captured packets and extract relevant information.

    Args:
    packets (list): List of captured packets.

    Returns:
    dict: Analysis results including source IPs, destination IPs,
          protocols, packet sizes, timestamps, and IP categories.
    """
    analysis = {
        'src_ips': Counter(),
        'dst_ips': Counter(),
        'protocols': Counter(),
        'packet_sizes': [],
        'timestamps': [],
        'ip_categories': Counter(),
        'ports': Counter()
    }

    for packet in packets:
        if scapy.IP in packet:
            src_ip = packet[scapy.IP].src
            dst_ip = packet[scapy.IP].dst
            protocol = packet[scapy.IP].proto
            packet_size = len(packet)
            timestamp = packet.time

            # Count occurrences of source and destination IPs
            analysis['src_ips'][src_ip] += 1
            analysis['dst_ips'][dst_ip] += 1

            # Count occurrences of protocols
            analysis['protocols'][protocol] += 1

            # Record packet sizes and timestamps
            analysis['packet_sizes'].append(packet_size)
            analysis['timestamps'].append(timestamp)

            # Categorize source IP addresses
            src_category = categorize_ip(src_ip)
            analysis['ip_categories'][src_category] += 1

            if scapy.TCP in packet:
                tcp_layer = packet[scapy.TCP]
                analysis['ports'][f"TCP {tcp_layer.sport}"] += 1
                analysis['ports'][f"TCP {tcp_layer.dport}"] += 1
            elif scapy.UDP in packet:
                udp_layer = packet[scapy.UDP]
                analysis['ports'][f"UDP {udp_layer.sport}"] += 1
                analysis['ports'][f"UDP {udp_layer.dport}"] += 1

    return analysis

def visualize_traffic(analysis):
    """
    Create visualizations of the network traffic analysis.

    Args:
    analysis (dict): Analysis results from analyze_packets function.
    """
    fig = plt.figure(figsize=(15, 7.5))
    fig.suptitle("Network Traffic Analysis", fontsize=20)

    # 1. Source IP bar chart
    ax1 = fig.add_subplot(231)
    top_ips = dict(analysis['src_ips'].most_common(10))
    ax1.bar(top_ips.keys(), top_ips.values(), align='center')
    ax1.set_xticks(range(len(top_ips)))
    ax1.set_xticklabels(top_ips.keys(), rotation=45, ha='right')
    ax1.set_title("Top 10 Source IPs")
    ax1.set_xlabel("Source IP")
    ax1.set_ylabel("Packet Count")

    # 2. Protocol pie chart
    ax2 = fig.add_subplot(232)
    protocol_names = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
    protocol_data = {protocol_names.get(k, f'Other ({k})'): v for k, v in analysis['protocols'].items()}
    ax2.pie(protocol_data.values(), labels=protocol_data.keys(), autopct='%1.1f%%', startangle=90)
    ax2.set_title("Protocol Distribution")

    # 3. Packet size histogram
    ax3 = fig.add_subplot(233)
    ax3.hist(analysis['packet_sizes'], bins=50, edgecolor='black')
    ax3.set_title("Packet Size Distribution")
    ax3.set_xlabel("Packet Size (bytes)")
    ax3.set_ylabel("Frequency")

    # 4. Time series plot
    ax4 = fig.add_subplot(234)
    timestamps = [datetime.fromtimestamp(ts) for ts in analysis['timestamps']]
    ax4.plot(timestamps, range(1, len(timestamps) + 1))
    ax4.set_title("Cumulative Packets Over Time")
    ax4.set_xlabel("Time")
    ax4.set_ylabel("Cumulative Packet Count")
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax4.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # 5. IP category pie chart
    ax5 = fig.add_subplot(235)
    ax5.pie(analysis['ip_categories'].values(), labels=analysis['ip_categories'].keys(), autopct='%1.1f%%', startangle=90)
    ax5.set_title("IP Address Categories")

    # 6. Top ports bar chart
    ax6 = fig.add_subplot(236)
    top_ports = dict(analysis['ports'].most_common(10))
    ax6.bar(top_ports.keys(), top_ports.values(), align='center')
    ax6.set_xticks(range(len(top_ports)))
    ax6.set_xticklabels(top_ports.keys(), rotation=45, ha='right')
    ax6.set_title("Top 10 Ports")
    ax6.set_xlabel("Port")
    ax6.set_ylabel("Packet Count")

    # Adjust layout and display the plot
    plt.tight_layout()
    plt.subplots_adjust(top=0.90)
    plt.show()

def get_connected_interfaces():
    """
    Get a list of connected network interfaces with IP addresses.

    Returns:
    list: A list of tuples containing (interface_name, interface_id).
    """
    connected_interfaces = []

    if platform.system() == "Windows":
        for iface in get_windows_if_list():
            name = iface.get('name', '')
            description = iface.get('description', '')
            ip_addresses = iface.get('ips', [])

            valid_ips = [ip for ip in ip_addresses if ip != '0.0.0.0' and not ipaddress.ip_address(ip).is_link_local]

            if valid_ips:
                display_name = f"{description} ({name})" if description else name
                connected_interfaces.append((f"{display_name} - {valid_ips[0]}", name))
    else:
        for iface in scapy.get_if_list():
            try:
                ip = scapy.get_if_addr(iface)
                if ip and ip != '0.0.0.0' and not ipaddress.ip_address(ip).is_link_local:
                    connected_interfaces.append((f"{iface} - {ip}", iface))
            except:
                continue  # Skip interfaces that cause errors

    return connected_interfaces

def main():
    print("Network Traffic Analysis Tool")
    print("-----------------------------")

    # Get and display connected interfaces
    connected_interfaces = get_connected_interfaces()

    if not connected_interfaces:
        print("No connected network interfaces found. Please check your network connections.")
        return

    print("\nConnected network interfaces:")
    for i, (name, _) in enumerate(connected_interfaces, 1):
        print(f"{i}. {name}")

    # Ask user to select an interface
    while True:
        try:
            choice = int(input("\nEnter the number of the interface you want to use: "))
            if 1 <= choice <= len(connected_interfaces):
                _, interface = connected_interfaces[choice - 1]
                break
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Ask user for packet count
    while True:
        try:
            packet_count = int(input("Enter the number of packets to capture: "))
            if packet_count > 0:
                break
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    # Ask user for timeout
    while True:
        timeout_input = input("Enter the timeout in seconds (or press Enter for no timeout): ").strip()
        if timeout_input == "":
            timeout = None
            break
        try:
            timeout = float(timeout_input)
            if timeout > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a positive number or press Enter for no timeout.")

    print(f"\nStarting Network Traffic Analysis Tool...")
    print(f"Selected Interface: {interface}")
    print(f"Packet Count: {packet_count}")
    print(f"Timeout: {timeout if timeout is not None else 'No timeout'}")

    start_time = time.time()

    # Capture packets
    captured_packets = sniff_packets(interface, packet_count, timeout)
    print(f"\nCaptured {len(captured_packets)} packets in {time.time() - start_time:.2f} seconds")

    # Analyze captured packets
    analysis_results = analyze_packets(captured_packets)
    print("Packet analysis completed")

    # Generate and display visualizations
    print("Generating traffic visualizations...")
    visualize_traffic(analysis_results)
    print("Visualizations completed.")

if __name__ == "__main__":
    main()