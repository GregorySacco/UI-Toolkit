#!/usr/bin/env python3.10
from UI import UI
import subprocess

UI = UI()


if __name__ == '__main__':
    UI.app.run_server(debug=False, port = 8080, host='192.168.1.7')
