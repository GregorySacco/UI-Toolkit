from flask import Flask
import numpy as np
from pylsl import StreamInfo, StreamInlet, resolve_stream


class Server:
    def __init__(self):
        self.app = Flask(__name__)

        in_memory_datastore = {
        "COBOL" : {"name": "COBOL", "publication_year": np.array([1,2,3]).tolist(), "contribution": "record data"},
        "ALGOL" : {"name": "ALGOL", "publication_year": 1958, "contribution": "scoping and nested functions"},
        "APL" : {"name": "APL", "publication_year": 1962, "contribution": "array processing"},
        }

        @self.app.get('/programming_languages')
        def list_programming_languages():
            return in_memory_datastore
        
        if __name__ == '__main__':
            self.app.run()