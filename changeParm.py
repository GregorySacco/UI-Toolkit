import numpy as np
from pylsl import StreamInlet, resolve_stream, resolve_streams
import time
# streams=resolve_stream('name','Change_parm')
# inlet=StreamInlet(streams[0])

# while True:
#     data_plot, time_inlet = inlet.pull_sample(timeout=0.5)
#     print(data_plot)


streams = resolve_streams()
for info in streams:
    print(info.name())
    # if info.name() == 'Change_parm':
    #     # print(info.name())
    #     id = print(info.source_id())
    #     print(info.channel_count())


stream =resolve_stream('name','Hyp_parm')
inlet=StreamInlet(stream[0])

while True:
    data_plot, time_inlet = inlet.pull_sample(timeout=0.5)
    print(data_plot)


# streams=resolve_stream('name','polar ECG')
# inlet=StreamInlet(streams[0])
# i=0
# t =0
# while True:
#     data_plot, time_inlet = inlet.pull_sample(timeout=0.2)
#     if data_plot is not None and i == 0:
#         i = 1
#         start= time.perf_counter()
#         print(data_plot)
#         t += 1
#         print('t = ', t )
#     elif data_plot is None and i == 1:
#         i = 0
#         stop= time.perf_counter()
#         elapsed_time = stop - start
#         print("Elapsed time: ", elapsed_time)
    

        