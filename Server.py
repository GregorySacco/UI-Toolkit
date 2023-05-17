from flask import Flask
import numpy as np
from pylsl import StreamInlet, resolve_stream, resolve_streams


class Store:
   def __init__(self):
      self.plot = None
      self.time_inlet = None
      self.gp = None
      self.time_inlet_gp = None
      self.ecg = None

saved=Store()

app = Flask(__name__)

streams = resolve_streams()
for info in streams:
    print(info.name())
    # if info.name() == 'Change_parm':
    #     # print(info.name())
    #     id = print(info.source_id())
    #     print(info.channel_count())

streams=resolve_stream('name','Change_parm')  
inlet=StreamInlet(streams[0])
streams=resolve_stream('name','plot_data_GP')
inlet_gp=StreamInlet(streams[0])
# streams=resolve_stream('name','plot_data_acq')
# inlet_acq=StreamInlet(streams[0])
streams=resolve_stream('name','polar ECG')
inlet_ecg=StreamInlet(streams[0])
        

@app.get('/OptimizationData')
def list_OptimizationData():
   data_plot, time_inlet = inlet.pull_sample(timeout=0.1)
   if data_plot is not None:         
      saved.plot=data_plot
      saved.time_inlet = time_inlet

   data_gp, time_inlet_gp = inlet_gp.pull_chunk(timeout=0.1)
   if not(data_gp == []):
      saved.gp=data_gp
      saved.time_inlet_gp = time_inlet_gp

   in_memory_datastore = {
      "Change_parm" : {"data_plot": saved.plot, "time_inlet": saved.time_inlet},
      "plot_data_GP" : {"data_gp": saved.gp, "time_inlet_gp": saved.time_inlet_gp},
   }
   return in_memory_datastore

@app.get('/polarECG')
def list_ECGData():
   data_ecg, time_inlet_ecg = inlet_ecg.pull_chunk(timeout=0.2)
   if not(data_ecg == []):
      saved.ecg=data_ecg

   in_memory_datastore = {
      "polar ECG" : {"data_ecg": saved.ecg},
   }
   return in_memory_datastore

if __name__ == '__main__':
   app.run()

   # while True:
   #    print('here')
   #    data_plot, time_inlet = inlet.pull_sample(timeout=0.0)
   #    if data_plot is not None:
   #       saved.plot = data_plot
   #       saved.time_inlet = time_inlet

   #    data_gp, time_inlet_gp = inlet_gp.pull_chunk(timeout=0.0)
   #    if data_gp is not None:
   #       saved.gp = data_gp
   #       saved.time_inlet_gp = time_inlet_gp

   #    data_ecg, time_inlet_ecg = inlet_ecg.pull_chunk(timeout=0.0)
   #    if data_ecg is not None:
   #       saved.ecg = data_ecg
   
      
        