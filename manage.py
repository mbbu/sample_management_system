import os
import subprocess

from flask_script import Manager
from flask_socketio import SocketIO

import client
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
socketio = SocketIO(app)


def _bash(cmd, **kwargs):
    """ Helper bash call"""
    print('>>> {}'.format(cmd))
    return subprocess.call(cmd, env=os.environ, shell=True, **kwargs)


def serve():
    """ Run Vue Development Server"""
    print('Starting the Vue development server... ')
    cmd = 'npm run serve'
    _bash(cmd, cwd=client)


def build():
    """ Build vue Application"""
    cmd = 'npm build'
    _bash(cmd, cwd=client)
    print('Build completed')


def lint():
    """ Lint Vue Application"""
    cmd = 'npm lint'
    _bash(cmd, cwd=client)
    print('Lint completed')


if __name__ == '__main__':
    manager.run()
