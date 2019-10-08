#!/usr/bin/python

from __future__ import print_function
import os
import sys
import ConfigParser
import rtkit.tracker
import rtkit.authenticators
from pprint import pprint as pp

names = ['api', 'cf', 'creator', 'date', 'delta', 'id', 'owner', 'priority', 'requestors', 'status', 'subject', 'tracker']

rc = {}
with open(os.path.expanduser('~/.rtrc')) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        name, value = line.split(' ', 1)
        rc[name] = value

url = '%s/REST/1.0/' % rc['server']
rt = rtkit.tracker.Tracker(url, rc['user'], rc['passwd'], rtkit.authenticators.CookieAuthenticator)

queue = 'msdw-afs'
tickets = rt.search_tickets("Queue='%s' AND (Status='open' OR Status='new' OR Status='stalled')" % (queue))
for t in tickets:
    print('%s\t%s\t%s' % (t.id, t.status, t.subject))
