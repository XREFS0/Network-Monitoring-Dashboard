from src.netmonitor.utils.formatting import format_bytes, format_speed, format_packets

def test_format_bytes():
    assert format_bytes(500) == "500.00 B"
    assert format_bytes(1024) == "1.00 KB"
    assert format_bytes(1024 * 1024) == "1.00 MB"
    assert format_bytes(1024 * 1024 * 1024) == "1.00 GB"

def test_format_speed():
    assert format_speed(500) == "500.00 B/s"
    assert format_speed(2048) == "2.00 KB/s"
    assert format_speed(1.5 * 1024 * 1024) == "1.50 MB/s"

def test_format_packets():
    assert format_packets(500) == "500"
    assert format_packets(1500) == "1.5K"
    assert format_packets(2500000) == "2.5M"
