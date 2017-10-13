import subprocess


def is_user_in_network(mac_address, timeout=5000):
    arp_scan = subprocess.check_output([
        'arp-scan',
        '-l',
        '--timeout={}'.format(timeout)
    ])
    return mac_address in arp_scan
