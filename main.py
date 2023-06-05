#!/usr/bin/env python3.10
from UI import UI
import subprocess

UI = UI()

# Start the server.py script as a subprocess
# subprocess.Popen(['python3.10', 'server.py'])

# async def async_process(msg, person):
#     subprocess.Popen(['python3.10', 'server.py'])

if __name__ == '__main__':
    UI.app.run_server(debug=True, port = 8080) # host='0.0.0.0')