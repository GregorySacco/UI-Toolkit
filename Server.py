from flask import Flask
import numpy as np
from pylsl import StreamInlet, resolve_stream


class Store:
   def __init__(self):
      self.plot = None
      self.gp = None
      self.ecg = None

saved=Store()

app = Flask(__name__)

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
   data_plot, time_inlet = inlet.pull_sample(timeout=0.2)
   if data_plot is None and saved.plot is not None:      
         data_plot = saved.plot
   else: 
      saved.plot=data_plot

   data_gp, time_inlet_gp = inlet_gp.pull_chunk(timeout=0.2)
   if data_gp == [] and saved.gp is not None:     
         data_gp = saved.gp
   else:
      saved.gp=data_gp

   data_ecg, time_inlet_ecg = inlet_ecg.pull_chunk(timeout=0.2)
   if data_ecg == [] and saved.ecg is not None:      
      data_ecg = saved.ecg
   else: 
      saved.ecg=data_ecg
   
   in_memory_datastore = {
    #   "Change_parm" : {"data_plot": data_plot, "time_inlet": time_inlet},
    #   "plot_data_GP" : {"data_gp": data_gp, "time_inlet_gp": time_inlet_gp},
      "polar ECG" : {"data_ecg": data_ecg},
   }
   return in_memory_datastore

if __name__ == '__main__':
   app.run()