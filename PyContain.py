import json
import os
import hashlib
import logging
import subprocess
import sys
import ctypes
import shutil
import psutil
from typing import Dict, List, Optional, Set

# Constants for file paths and logging
LOG_FILE = 'incident_monitor.log'
QUARANTINE_DIR = 'quarantine'

# Configure logging with function and module names included
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
)

def is_running_as_admin() -> bool:
    """
    Check if the script is running with elevated (administrator) privileges.

    Returns:
        bool: True if running with elevated privileges, False otherwise.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        logging.error(f"Error checking admin privileges: {e}")
        return False

def run_as_admin() -> None:
    """
    Restart the script with administrative privileges if not already running as admin.

    Side Effects:
        Prints a message to the user indicating that administrative privileges are required.
        Uses subprocess to restart the script with elevated permissions.
        Terminates the script if unable to restart with elevated permissions.
    """
    if not is_running_as_admin():
        script_path = os.path.abspath(sys.argv[0])
        logging.info("The script requires administrative privileges. Attempting to restart with elevated permissions...")

        try:
            # Use subprocess to restart the script with elevated permissions
            subprocess.run(
                ["powershell", "-Command", "Start-Process", sys.executable, f'"{script_path}"', "-Verb", "runAs"],
                check=True
            )
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to restart script with administrative privileges: {e}")
            print("Failed to restart script with administrative privileges. Please run the script manually as an administrator.")
            sys.exit(0)

def load_json_file(json_file_path: str) -> Optional[Dict]:
    """
    Load a JSON file from the given file path and return its data as a Python dictionary.

    Args:
        json_file_path (str): The file path of the JSON file to be loaded.

    Returns:
        dict: A dictionary containing the data from the JSON file, or None if an error occurred.

    Raises:
        FileNotFoundError: If the JSON file is not found at the specified path.
        json.JSONDecodeError: If the JSON file cannot be parsed.
    """
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading JSON file: {e}")
        return None

def get_active_network_connections() -> List[psutil._common.sconn]:
    """
    Retrieve a list of active network connections on the system.

    Returns:
        list: A list of active network connections represented as psutil.Connection objects.

    Raises:
        Exception: If unable to retrieve network connections.
    """
    try:
        connections = psutil.net_connections(kind='inet')
        # Filter connections to only keep established connections
        established_connections = [conn for conn in connections if conn.status == 'ESTABLISHED']
        return established_connections
    except Exception as e:
        logging.error(f"Error getting active network connections: {e}")
        return []

def check_malicious_ips(active_connections: List[psutil._common.sconn], malicious_ips: Set[str]) -> None:
    """
    Check active network connections against a set of malicious IP addresses.

    Args:
        active_connections (list): A list of active network connections.
        malicious_ips (set): A set of malicious IP addresses.

    Side Effects:
        Logs a warning message if an active connection to a malicious IP address is found.
        Blocks outbound traffic to the malicious IP address using a firewall rule.
    """
    checked_ips = set()
    for conn in active_connections:
        remote_ip = conn.raddr.ip

        # Skip already checked IPs
        if remote_ip in checked_ips:
            continue

        # Check if the remote IP is in the set of malicious IPs
        if remote_ip in malicious_ips:
            logging.warning(f"Active connection to malicious IP address: {remote_ip}")
            block_malicious_ip(remote_ip)

        checked_ips.add(remote_ip)

def block_malicious_ip(ip_address: str) -> None:
    """
    Block outbound traffic to the given malicious IP address using a firewall rule.

    Args:
        ip_address (str): The IP address to block.

    Side Effects:
        Logs a message indicating the IP address has been blocked.
        If the script is not running with administrative privileges, logs a warning message.
    """
    if is_running_as_admin():
        try:
            subprocess.run(
                f'netsh advfirewall firewall add rule name="Block Malicious IP" '
                f'dir=out action=block remoteip={ip_address}',
                shell=True,
                check=True
            )
            logging.info(f"Blocked malicious IP address: {ip_address}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error blocking malicious IP {ip_address}: {e}")
    else:
        logging.warning(f"Cannot block IP {ip_address} due to lack of administrative privileges.")

def get_running_processes() -> List[Dict]:
    """
    Retrieve a list of currently running processes on the system.

    Returns:
        list: A list of dictionaries, each containing information about a running process (PID and name).

    Raises:
        Exception: If unable to retrieve running processes.
    """
    try:
        return [proc.info for proc in psutil.process_iter(['pid', 'name', 'exe']) if proc.info]
    except Exception as e:
        logging.error(f"Error getting running processes: {e}")
        return []

def check_suspicious_programs(running_processes: List[Dict], suspicious_programs: List[Dict]) -> None:
    """
    Check running processes against a list of suspicious programs.

    Args:
        running_processes (list): A list of dictionaries, each containing information about a running process.
        suspicious_programs (list): A list of dictionaries, each containing a suspicious program's name and hash.

    Side Effects:
        Logs a warning message if a suspicious program is detected.
        Terminates the suspicious process and quarantines the executable file.
    """
    # Convert suspicious programs from list to dict (name -> hash)
    suspicious_programs_dict = {sp['name']: sp['tlsh'] for sp in suspicious_programs}

    # Initialize set to keep track of checked processes
    checked_process_names = set()

    for process in running_processes:
        process_name = process.get('name')
        process_pid = process.get('pid')
        file_path = process.get('exe')

        # Skip already checked processes
        if process_name in checked_process_names:
            continue

        if process_name in suspicious_programs_dict:
            # Compute file hash using SHA-256 instead of MD5
            file_hash = compute_file_hash(file_path, hash_type='sha256')

            # Compare computed hash with known suspicious hash
            if file_hash == suspicious_programs_dict[process_name]:
                logging.warning(f"Suspicious program detected: {process_name} with hash: {file_hash}")

                # Handle suspicious process and quarantine file
                handle_suspicious_process(process_pid, file_path)

        # Add process name to checked set
        checked_process_names.add(process_name)

def compute_file_hash(file_path: str, hash_type: str = 'sha256') -> str:
    """
    Compute the hash of a file using the specified hash algorithm.

    Args:
        file_path (str): The file path of the file to hash.
        hash_type (str): The type of hash to compute (default is 'sha256').

    Returns:
        str: The computed hash of the file.

    Raises:
        Exception: If an error occurs while computing the file hash.
    """
    try:
        hash_obj = hashlib.new(hash_type)
        with open(file_path, 'rb') as file:
            while chunk := file.read(4096):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        logging.error(f"Error computing file hash: {e}")
        return ""

def handle_suspicious_process(process_pid: int, file_path: str) -> None:
    """
    Handle suspicious processes by terminating them and quarantining the executable.

    Args:
        process_pid (int): The PID of the suspicious process.
        file_path (str): The file path of the executable associated with the suspicious process.

    Side Effects:
        Terminates the suspicious process.
        Moves the executable file to the quarantine directory.
    """
    try:
        # Terminate the suspicious process
        process = psutil.Process(process_pid)
        process.terminate()
        process.wait(timeout=10)  # Allow process time to terminate gracefully

        # Create quarantine directory if not already present
        quarantine_path = os.path.join(os.path.dirname(file_path), QUARANTINE_DIR)
        os.makedirs(quarantine_path, exist_ok=True)

        # Move the file to quarantine directory
        quarantine_file_path = os.path.join(quarantine_path, os.path.basename(file_path))
        shutil.move(file_path, quarantine_file_path)

        logging.info(f"Suspicious process {process_pid} terminated and file moved to quarantine: {quarantine_file_path}")
    except psutil.NoSuchProcess:
        logging.warning(f"No such process with PID: {process_pid}")
    except Exception as e:
        logging.error(f"Error handling suspicious process: {e}")

def main() -> None:
    """
    Main function to coordinate the monitoring and handling of incidents on the Windows machine.

    The function performs the following tasks:
    1. Ensures the script is running with administrative privileges.
    2. Loads data from a JSON file containing malicious IPs and suspicious programs.
    3. Checks active network connections for connections to malicious IPs.
    4. Checks running processes for suspicious programs.
    """
    run_as_admin()

    # Load JSON file containing malicious IPs and suspicious programs
    json_file_path = 'incident_data.json'
    data = load_json_file(json_file_path)
    if data is None:
        print("Failed to load incident data. Please check the JSON file path and format.")
        return

    # Extract malicious IPs and suspicious programs from the data
    malicious_ips = set(data.get('malicious_ips', []))
    suspicious_programs = data.get('suspicious_programs', {})

    # Check active network connections
    active_connections = get_active_network_connections()
    check_malicious_ips(active_connections, malicious_ips)

    # Check running processes
    running_processes = get_running_processes()
    check_suspicious_programs(running_processes, suspicious_programs)

if __name__ == "__main__":
    main()
