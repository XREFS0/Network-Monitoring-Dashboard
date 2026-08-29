import psutil
import time
import socket
import sys
import platform
from typing import Dict, List, Optional, Tuple
from ..core.models import InterfaceStats, ConnectionInfo, SystemStats, NetworkOverview

class NetworkSampler:
    def __init__(self):
        self.last_io: Dict[str, Tuple[int, int, int, int, float]] = {}

    def get_system_stats(self) -> SystemStats:
        try:
            cpu = psutil.cpu_percent(interval=None)
        except Exception:
            cpu = 0.0
        try:
            mem = psutil.virtual_memory().percent
        except Exception:
            mem = 0.0
        try:
            hostname = socket.gethostname()
        except Exception:
            hostname = "Unknown"

        return SystemStats(
            cpu_usage=cpu,
            memory_usage=mem,
            hostname=hostname,
            platform_name=f"{platform.system()} {platform.release()}",
            python_version=sys.version.split()[0]
        )

    def sample_interfaces(self) -> Dict[str, InterfaceStats]:
        current_time = time.time()
        try:
            addrs = psutil.net_if_addrs()
        except Exception:
            addrs = {}
        try:
            stats = psutil.net_if_stats()
        except Exception:
            stats = {}
        try:
            io = psutil.net_io_counters(pernic=True)
        except Exception:
            io = {}

        result = {}
        for name in io.keys() | addrs.keys() | stats.keys():
            if_addr = addrs.get(name, [])
            ipv4_addr = None
            ipv6_addr = None
            mac_addr = None
            for addr in if_addr:
                if addr.family == socket.AF_INET:
                    ipv4_addr = addr.address
                elif addr.family == socket.AF_INET6:
                    ipv6_addr = addr.address.split("%")[0]
                elif hasattr(psutil, "AF_LINK") and addr.family == psutil.AF_LINK:
                    mac_addr = addr.address
                elif hasattr(socket, "AF_LINK") and addr.family == socket.AF_LINK:
                    mac_addr = addr.address

            if_stat = stats.get(name)
            is_up = if_stat.isup if if_stat else False
            speed = if_stat.speed if if_stat else 0
            mtu = if_stat.mtu if if_stat else 0

            if_io = io.get(name)
            bytes_sent = if_io.bytes_sent if if_io else 0
            bytes_recv = if_io.bytes_recv if if_io else 0
            packets_sent = if_io.packets_sent if if_io else 0
            packets_recv = if_io.packets_recv if if_io else 0
            errin = if_io.errin if if_io else 0
            errout = if_io.errout if if_io else 0
            dropin = if_io.dropin if if_io else 0
            dropout = if_io.dropout if if_io else 0

            speed_sent = 0.0
            speed_recv = 0.0

            if name in self.last_io:
                last_sent, last_recv, last_pkts_sent, last_pkts_recv, last_time = self.last_io[name]
                dt = current_time - last_time
                if dt > 0:
                    if bytes_sent >= last_sent:
                        speed_sent = (bytes_sent - last_sent) / dt
                    if bytes_recv >= last_recv:
                        speed_recv = (bytes_recv - last_recv) / dt

            self.last_io[name] = (bytes_sent, bytes_recv, packets_sent, packets_recv, current_time)

            result[name] = InterfaceStats(
                name=name,
                is_up=is_up,
                ipv4_address=ipv4_addr,
                ipv6_address=ipv6_addr,
                mac_address=mac_addr,
                speed=speed,
                mtu=mtu,
                bytes_sent=bytes_sent,
                bytes_recv=bytes_recv,
                packets_sent=packets_sent,
                packets_recv=packets_recv,
                errin=errin,
                errout=errout,
                dropin=dropin,
                dropout=dropout,
                bytes_sent_speed=speed_sent,
                bytes_recv_speed=speed_recv
            )

        return result

    def sample_connections(self) -> List[ConnectionInfo]:
        conns = []
        try:
            connections = psutil.net_connections(kind="inet")
        except Exception:
            return []

        proc_cache = {}
        for conn in connections:
            proto = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
            laddr = f"{conn.laddr.ip}" if conn.laddr else "*"
            lport = conn.laddr.port if conn.laddr else 0
            raddr = f"{conn.raddr.ip}" if conn.raddr else "*"
            rport = conn.raddr.port if conn.raddr else 0
            status = conn.status

            proc_name = None
            if conn.pid:
                if conn.pid in proc_cache:
                    proc_name = proc_cache[conn.pid]
                else:
                    try:
                        p = psutil.Process(conn.pid)
                        proc_name = p.name()
                        proc_cache[conn.pid] = proc_name
                    except Exception:
                        proc_cache[conn.pid] = None

            conns.append(
                ConnectionInfo(
                    protocol=proto,
                    local_address=laddr,
                    local_port=lport,
                    remote_address=raddr,
                    remote_port=rport,
                    status=status,
                    pid=conn.pid,
                    process_name=proc_name
                )
            )
        return conns

    def get_network_overview(self, interfaces: Dict[str, InterfaceStats], selected_interface_name: Optional[str]) -> NetworkOverview:
        target_if = selected_interface_name
        if not target_if or target_if not in interfaces:
            active_candidate = None
            for name, stats in interfaces.items():
                if stats.is_up and stats.ipv4_address and name != "lo" and "loopback" not in name.lower():
                    active_candidate = name
                    break
            if not active_candidate:
                for name, stats in interfaces.items():
                    if stats.is_up:
                        active_candidate = name
                        break
            target_if = active_candidate

        if target_if and target_if in interfaces:
            stat = interfaces[target_if]
            return NetworkOverview(
                bytes_sent_speed=stat.bytes_sent_speed,
                bytes_recv_speed=stat.bytes_recv_speed,
                total_bytes_sent=stat.bytes_sent,
                total_bytes_recv=stat.bytes_recv,
                packets_sent=stat.packets_sent,
                packets_recv=stat.packets_recv,
                active_interface=target_if,
                interface_state=stat.is_up,
                connection_status="Connected" if stat.is_up else "Disconnected",
                current_ip=stat.ipv4_address,
                mac_address=stat.mac_address
            )

        total_sent = 0
        total_recv = 0
        total_packets_sent = 0
        total_packets_recv = 0
        total_speed_sent = 0.0
        total_speed_recv = 0.0

        for stats in interfaces.values():
            total_sent += stats.bytes_sent
            total_recv += stats.bytes_recv
            total_packets_sent += stats.packets_sent
            total_packets_recv += stats.packets_recv
            total_speed_sent += stats.bytes_sent_speed
            total_speed_recv += stats.bytes_recv_speed

        return NetworkOverview(
            bytes_sent_speed=total_speed_sent,
            bytes_recv_speed=total_speed_recv,
            total_bytes_sent=total_sent,
            total_bytes_recv=total_recv,
            packets_sent=total_packets_sent,
            packets_recv=total_packets_recv,
            active_interface=None,
            interface_state=False,
            connection_status="Disconnected",
            current_ip=None,
            mac_address=None
        )
