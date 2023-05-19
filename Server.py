from flask import Flask
from pylsl import StreamInlet, resolve_stream, resolve_streams
import asyncio

app = Flask(__name__)

class Store:
    def __init__(self):
        self.plot = None
        self.time_inlet = None
        self.gp = None
        self.time_inlet_gp = None
        self.ecg = None

saved = Store()

streams = resolve_streams()
for info in streams:
    print(info.name())

streams = resolve_stream('name', 'Change_parm')
inlet = StreamInlet(streams[0])
streams = resolve_stream('name', 'plot_data_GP')
inlet_gp = StreamInlet(streams[0])
streams = resolve_stream('name', 'polar ECG')
inlet_ecg = StreamInlet(streams[0])


@app.get('/OptimizationData')
def list_OptimizationData():
    in_memory_datastore = {
        "Change_parm": {"data_plot": saved.plot, "time_inlet": saved.time_inlet},
        "plot_data_GP": {"data_gp": saved.gp, "time_inlet_gp": saved.time_inlet_gp},
    }
    return in_memory_datastore

@app.get('/polarECG')
def list_ECGData():
    data_ecg, time_inlet_ecg = inlet_ecg.pull_chunk(timeout=0.2)
    if not (data_ecg == []):
        saved.ecg = data_ecg
    in_memory_datastore = {
        "polar ECG": {"data_ecg": saved.ecg},
    }
    return in_memory_datastore


async def run_code():
   while True:
      
      data_plot, time_inlet = inlet.pull_sample(timeout=0.1)
      if data_plot is not None:
         saved.plot = data_plot
         saved.time_inlet = time_inlet

      data_gp, time_inlet_gp = inlet_gp.pull_chunk(timeout=0.1)
      if not (data_gp == []):
         saved.gp = data_gp
         saved.time_inlet_gp = time_inlet_gp

if __name__ == '__main__':
   loop = asyncio.get_event_loop()
   tasks = [run_code(), loop.run_in_executor(None, app.run)]
   loop.run_until_complete(asyncio.gather(*tasks))
   
      
        