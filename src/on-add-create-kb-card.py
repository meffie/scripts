#!/usr/bin/python3

import configparser
import json
import os
import ssl
import sys

try:
    import kanboard
except ImportError:
    print('kanboard module not found.')
    os.sys.exit(1)


# Monkey patch ssl module to work around our malformed cert.
# Fixes the error:
#     ssl.CertificateError: hostname 'kb.devlab.sinenomine.net' doesn't match u'debian-8-x64-02'
ssl.match_hostname = lambda cert, hostname: True
ssl._create_default_https_context = ssl._create_unverified_context


class Config(object):

    def __init__(self, filename='~/.kbrc'):
        self._filename = os.path.expanduser(filename)
        if not os.path.exists(self._filename):
            raise OSError(2, f'Config file not found: {self._filename}')
        self._config = configparser.ConfigParser()
        if len(self._config.read(self._filename)) != 1:
            raise OSError(2, f'Unable to read config file: {self._filename}')

    @property
    def host(self):
        return self._config.get('kanboard', 'host')

    @property
    def token(self):
        return self._config.get('kanboard', 'token')

    @property
    def url(self):
        return os.path.join(self.host, 'jsonrpc.php')

    @property
    def project_id(self):
        return int(self._config.get('sync', 'project'))

    @property
    def username(self):
        return self._config.get('sync', 'username')


def main():
    feedback = None
    config = Config()
    task = json.loads(sys.stdin.readline())

    # ticket and kb UDAs must be integers (?)
    if 'ticket' in task:
        task['ticket'] = int(task['ticket'])
    if 'kb' in task:
        task['kb'] = int(task['kb'])

    if 'kb' in task and task['kb'] == 0:
        kb = kanboard.Client(config.url, 'jsonrpc', config.token)

        # Check for existing card by title.
        title = task['description']
        tasks = kb.search_tasks(project_id=config.project_id, query=f'title:{title}')
        titles = set(map(lambda t: t['title'], tasks))
        if title in titles:
            raise ValueError(f'Card alread exists with the title "{title}".')

        user = kb.get_user_by_name(username=config.username)
        if not user:
            raise ValueError(f'Failed to get user id for username f{config.username}.')

        # Add a kanboard card.
        fields = {
           'title': title,
           'project_id': config.project_id,
           'owner_id': user['id'],
        }
        if 'ticket' in task:
            fields['reference'] = task['ticket']
        kb_id = kb.create_task(**fields)
        task['kb'] = int(kb_id)   # Add the generated id to the task.
        feedback = f'Added kanboard card {kb_id}.'

    print(json.dumps(task))
    if feedback:
        print(feedback)


if __name__ == '__main__':
    try:
        main()
        rc = 0
    except Exception as e:
        print(f'Hook failed: {e}')
        rc = 1
    sys.exit(rc)
