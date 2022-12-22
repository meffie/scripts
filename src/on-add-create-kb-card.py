#!/usr/bin/python3

import configparser
import json
import os
import ssl
import sys

try:
    import kanboard
except ImportError:
    sys.stderr.write('kanboard module not found.\n')
    os.sys.exit(1)

# Monkey patch ssl module to work around our malformed cert.
# Fixes the error:
#     ssl.CertificateError: hostname 'kb.devlab.sinenomine.net' doesn't match u'debian-8-x64-02'
ssl.match_hostname = lambda cert, hostname: True
ssl._create_default_https_context = ssl._create_unverified_context

def load_config():
    config = configparser.ConfigParser()
    filename = os.path.expanduser('~/.kbrc')
    if not os.path.exists(filename):
        raise OSError(2, f'kanboard config file not found: {filename}')
    if len(config.read(filename)) != 1:
        raise OSError(2, f'Unable to read config file: {filename}')
    return config


def connect(config):
    host = config.get('kanboard', 'host')
    token = config.get('kanboard', 'token')
    url = os.path.join(host, 'jsonrpc.php')
    return kanboard.Client(url, 'jsonrpc', token)


def main():
    task = json.loads(sys.stdin.readline())
    if 'ticket' in task:
        task['ticket'] = int(task['ticket'])
    tags = task.get('tags', [])
    if 'kb' in tags:
        config = load_config()
        kb = connect(config)
        username = config.get('sync', 'username')
        user = kb.get_user_by_name(username=username)
        if not user:
            sys.stderr.write(f'Failed to get user id for username f{username}.\n')
            return 1

        fields = {
            'title': task['description'],
            'project_id': int(config.get('sync', 'project')),
            'owner_id': user['id'],
        }
        if 'ticket' in task:
            fields['reference'] = task['ticket']

        card_id = kb.create_task(**fields)
        task['kb'] = int(card_id)   # Add the kb id to our new task.

    print(json.dumps(task))
    return 0


if __name__ == '__main__':
    sys.exit(main())
