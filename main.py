#!/usr/bin/env python3.10
from UI import UI

UI = UI()

if __name__ == '__main__':
    UI.app.run_server(debug=True, port = 8080) # host='0.0.0.0')