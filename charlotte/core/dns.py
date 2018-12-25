"""
this file implement some dns utils

todo optimize this by async dns query
"""

import socket


def fetch_dns(hostname) -> str:
    """
    blocking method for dns query
    :param hostname: domain that need queried
    :return: ip string
    """
    return socket.gethostbyname(hostname)


_dns_cache = {}


def get_cached_dns(hostname) -> str:
    """
    same function with fetch_dns, but with a cache
    """
    if hostname in _dns_cache:
        return _dns_cache.get(hostname)
    else:
        address = fetch_dns(hostname)
        _dns_cache.setdefault(hostname, address)
        return address
