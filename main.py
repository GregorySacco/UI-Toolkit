from UI import UI
from pylsl import StreamInfo, StreamInlet, resolve_stream
import subprocess

UI = UI()

if __name__ == '__main__':
    # subprocess.Popen(['python', 'Server.py'])
    UI.app.run_server(debug=True, port = 8080) # host='0.0.0.0')