import os
import subprocess
import shlex
from flask import Flask

# Function to start the web server
def start_server(port):
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    app.run(host='0.0.0.0', port=port)

# Set default port to 8080 or use SERVER_PORT or PORT environment variable
port = int(os.environ.get('SERVER_PORT', os.environ.get('PORT', 8080)))

# Define the command to be executed
cmd = "chmod +x ./start.sh && ./start.sh"

# Start the web server in a separate process group
web_server_command = ['python', __file__, '--start-server', str(port)]
subprocess.Popen(web_server_command, preexec_fn=os.setsid)

# Start the web server
start_server(port)
