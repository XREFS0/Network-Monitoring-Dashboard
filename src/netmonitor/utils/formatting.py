def format_bytes(num_bytes: float) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num_bytes < 1024.0:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.2f} PB"

def format_speed(bytes_per_sec: float) -> str:
    for unit in ["B/s", "KB/s", "MB/s", "GB/s", "TB/s"]:
        if bytes_per_sec < 1024.0:
            return f"{bytes_per_sec:.2f} {unit}"
        bytes_per_sec /= 1024.0
    return f"{bytes_per_sec:.2f} PB/s"

def format_packets(num_packets: int) -> str:
    if num_packets < 1000:
        return str(num_packets)
    elif num_packets < 1000000:
        return f"{num_packets / 1000.0:.1f}K"
    else:
        return f"{num_packets / 1000000.0:.1f}M"
