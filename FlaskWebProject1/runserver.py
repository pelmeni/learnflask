"""
This script runs the FlaskWebProject1 application using a development server.
"""

from os import environ
from FlaskWebProject1 import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(50479)
        #int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 50479
    app.run(HOST, PORT)
