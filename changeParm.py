import numpy as np
from pylsl import StreamInlet, resolve_stream, resolve_streams
# streams=resolve_stream('name','Change_parm')
# inlet=StreamInlet(streams[0])

# while True:
#     data_plot, time_inlet = inlet.pull_sample(timeout=0.5)
#     print(data_plot)


streams = resolve_streams()
for info in streams:
    print(info.name())
    if info.name() == 'Change_parm':
        # print(info.name())
        id = print(info.source_id())
        print(info.channel_count())


streams =resolve_stream('source_id','1998')
inlet=StreamInlet(streams[0])

while True:
    data_plot, time_inlet = inlet.pull_sample(timeout=0.5)
    print(data_plot)

        