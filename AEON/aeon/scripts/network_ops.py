
import socket
import subprocess
import platform
import struct
from typing import List, Optional, Tuple

def get_local_ip() -> str:
    """Returns local IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def ping_host(host: str, count: int = 4) -> str:
    """Pings a host."""
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, str(count), host]
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

def is_port_open(host: str, port: int, timeout: int = 1) -> bool:
    """Checks if a TCP port is open."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.close()
        return True
    except:
        return False

def scan_ports(host: str, ports: List[int]) -> List[int]:
    """Scans a list of ports."""
    open_ports = []
    for port in ports:
        if is_port_open(host, port):
            open_ports.append(port)
    return open_ports

def scan_common_ports(host: str) -> List[int]:
    """Scans common ports (20-1024)."""
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 8080, 3306, 5432, 27017]
    return scan_ports(host, common_ports)

def resolve_dns(hostname: str) -> str:
    """Resolves IP from hostname."""
    try:
        return socket.gethostbyname(hostname)
    except:
        return ""

def reverse_dns(ip: str) -> str:
    """Resolves hostname from IP."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return ""

def get_mac_address() -> str:
    """Returns MAC address."""
    from uuid import getnode
    mac = getnode()
    return ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))

def ip_to_int(ip: str) -> int:
    """Converts IP string to integer."""
    try:
        return struct.unpack("!I", socket.inet_aton(ip))[0]
    except:
        return 0

def int_to_ip(num: int) -> str:
    """Converts integer to IP string."""
    try:
        return socket.inet_ntoa(struct.pack("!I", num))
    except:
        return ""

def is_valid_ip(ip: str) -> bool:
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False

def check_ssl_cert(hostname: str) -> str:
    """Checks SSL cert expiration (rudimentary)."""
    import ssl
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.connect((hostname, 443))
            cert = s.getpeercert()
            return str(cert)
    except Exception as e:
        return str(e)
