import time
from src.netmonitor.monitoring.samplers import NetworkSampler
from src.netmonitor.core.models import InterfaceStats

def test_sampler_empty_overview():
    sampler = NetworkSampler()
    interfaces = {}
    overview = sampler.get_network_overview(interfaces, None)
    
    assert overview.bytes_sent_speed == 0.0
    assert overview.bytes_recv_speed == 0.0
    assert overview.active_interface is None
    assert overview.connection_status == "Disconnected"

def test_sampler_overview_fallback():
    sampler = NetworkSampler()
    interfaces = {
        "eth0": InterfaceStats(
            name="eth0",
            is_up=True,
            ipv4_address="192.168.1.5",
            ipv6_address=None,
            mac_address="00:11:22:33:44:55",
            speed=1000,
            mtu=1500,
            bytes_sent=1000,
            bytes_recv=2000,
            packets_sent=10,
            packets_recv=20,
            errin=0,
            errout=0,
            dropin=0,
            dropout=0,
            bytes_sent_speed=100.0,
            bytes_recv_speed=200.0
        ),
        "lo": InterfaceStats(
            name="lo",
            is_up=True,
            ipv4_address="127.0.0.1",
            ipv6_address=None,
            mac_address=None,
            speed=10,
            mtu=65536,
            bytes_sent=5000,
            bytes_recv=5000,
            packets_sent=50,
            packets_recv=50,
            errin=0,
            errout=0,
            dropin=0,
            dropout=0,
            bytes_sent_speed=50.0,
            bytes_recv_speed=50.0
        )
    }
    overview = sampler.get_network_overview(interfaces, None)
    assert overview.active_interface == "eth0"
    assert overview.bytes_recv_speed == 200.0
    assert overview.bytes_sent_speed == 100.0
    assert overview.connection_status == "Connected"
