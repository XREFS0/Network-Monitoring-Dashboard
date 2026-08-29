from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass(frozen=True)
class InterfaceStats:
    name: str
    is_up: bool
    ipv4_address: Optional[str]
    ipv6_address: Optional[str]
    mac_address: Optional[str]
    speed: int
    mtu: int
    bytes_sent: int
    bytes_recv: int
    packets_sent: int
    packets_recv: int
    errin: int
    errout: int
    dropin: int
    dropout: int
    bytes_sent_speed: float = 0.0
    bytes_recv_speed: float = 0.0

@dataclass(frozen=True)
class ConnectionInfo:
    protocol: str
    local_address: str
    local_port: int
    remote_address: str
    remote_port: int
    status: str
    pid: Optional[int]
    process_name: Optional[str]

@dataclass(frozen=True)
class SystemStats:
    cpu_usage: float
    memory_usage: float
    hostname: str
    platform_name: str
    python_version: str

@dataclass(frozen=True)
class NetworkOverview:
    bytes_sent_speed: float
    bytes_recv_speed: float
    total_bytes_sent: int
    total_bytes_recv: int
    packets_sent: int
    packets_recv: int
    active_interface: Optional[str]
    interface_state: bool
    connection_status: str
    current_ip: Optional[str]
    mac_address: Optional[str]
