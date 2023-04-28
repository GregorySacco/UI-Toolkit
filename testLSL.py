from pylsl import StreamInfo, StreamInlet, resolve_stream
import time

streams=resolve_stream('name','Change_parm')
inlet=StreamInlet(streams[0])


while True:
    print(inlet.pull_sample(timeout=0.5))
    time.sleep(0.5)