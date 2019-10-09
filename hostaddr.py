#!/usr/bin/python

import re
from sh import ip

addrs = []
devices = []
for route in ip('-oneline', 'route', 'list', _iter=True):
    m = re.search(r'^default .* dev\s([^\s]+)', route)
    if m:
        devices.append(m.group(1))
for device in devices:
    for address in ip('-oneline', '-4', 'address', 'show', 'dev', device, 'up', _iter=True):
        m = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', address)
        if m:
            addrs.append(m.group(1))
for addr in addrs:
    print(addr)
