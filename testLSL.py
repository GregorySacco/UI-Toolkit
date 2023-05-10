from UI import UI
from pylsl import StreamInfo, StreamInlet, resolve_stream

app = UI()

if __name__ == '__main__':
            app.app.run_server(debug=True, port = 8080) # host='0.0.0.0')