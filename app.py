import os
import subprocess
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

# Start the web server in a separate process
subprocess.Popen(['python', __file__, '--start-server', str(port)])

# Continue with the rest of your script...

# For example, your original code to run the "start.sh" script
cmd = "chmod +x ./start.sh && ./start.sh"
subprocess.call(cmd, shell=True)
