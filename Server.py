#!/usr/bin/env python3.10
import asyncio
import zmq
import zmq.asyncio
from flask import Flask

ctx = zmq.asyncio.Context()

class Store:
    def __init__(self):
        self.plot = None
        self.gp = None
        self.ecg = None
        self.hyp = None 
        self.state = None
        self.IP = "tcp://127.0.0.1"

saved = Store()

async def async_process(msg, person):
    print(msg, person)


async def data_plot():
    sock = ctx.socket(zmq.SUB)
    sock.subscribe("")
    sock.connect(f"{saved.IP}:4501")
    while True:
        msg, msg_time = await sock.recv_pyobj() # waits for msg to be ready
        reply = await async_process(msg, 'data_plot')
        if msg is not None and msg != saved.plot:
            saved.plot = msg
        await asyncio.sleep(0.1)

async def data_gp():
    sock = ctx.socket(zmq.SUB)
    sock.subscribe("")
    sock.connect(f"{saved.IP}:4502")
    while True:
        msg, msg_time = await sock.recv_pyobj() # waits for msg to be ready
        reply = await async_process(msg, 'data_gp')
        if msg is not None and msg != saved.gp:
            saved.gp = msg
        await asyncio.sleep(0.1)

async def data_ecg():
    sock = ctx.socket(zmq.SUB)
    sock.subscribe("")
    sock.connect(f"{saved.IP}:4503")
    while True:
        msg = await sock.recv_pyobj() # waits for msg to be ready
        reply = await async_process(msg, 'data_ecg')
        if msg is not None and msg != saved.ecg:
            saved.ecg = msg
        await asyncio.sleep(0.1)

async def data_hyp():
    sock = ctx.socket(zmq.SUB)
    sock.subscribe("")
    sock.connect(f"{saved.IP}:4504")
    while True:
        msg = await sock.recv_pyobj() # waits for msg to be ready
        reply = await async_process(msg, 'data_hyp')
        if msg is not None and msg != saved.hyp:
            saved.hyp = msg
            # saved.time_inlet = msg_time
        await asyncio.sleep(0.1)


# async def data_acq():
#     sock = ctx.socket(zmq.PULL)
#     sock.connect("tcp://127.0.0.1:4504")
#     while True:
#         msg = await sock.recv_pyobj() # waits for msg to be ready
#         reply = await async_process(msg, 'data_acq')
#         if msg is not None and msg != saved.acq:
#             saved.acq = msg
#             # saved.time_inlet = msg_time
#         await asyncio.sleep(0.1)

# async def data_rmssd():
#     sock = ctx.socket(zmq.PULL)
#     sock.connect("tcp://127.0.0.1:4505")
#     while True:
#         msg = await sock.recv_pyobj() # waits for msg to be ready
#         reply = await async_process(msg, 'data_rmssd')
#         if msg is not None and msg != saved.rmssd:
#             saved.rmssd = msg
#             # saved.time_inlet = msg_time
#         await asyncio.sleep(0.1)

async def state():
    sock = ctx.socket(zmq.SUB)
    sock.subscribe("")
    sock.connect(f"{saved.IP}:4507")
    while True:
        msg = await sock.recv_pyobj() # waits for msg to be ready
        reply = await async_process(msg, 'flags')
        if msg is not None and msg != saved.state:
            saved.state = msg
        await asyncio.sleep(0.1)


async def send_to_API():
    app = Flask(__name__)
    @app.get('/OptimizationData')
    def list_OptimizationData():
        in_memory_datastore = {
            "data_plot": saved.plot,
            "data_gp": saved.gp,
            "data_hyp": saved.hyp,
            "data_ecg": saved.ecg,
            "state": saved.state}
        return in_memory_datastore


async def main_loop():
    L = await asyncio.gather(
        data_plot(),
        data_ecg(),
        data_hyp(),
        # data_acq(),
        # data_rmssd(),
        send_to_API()
    )

if __name__ == '__main__':
    asyncio.run(main_loop())




# from flask import Flask
# from pylsl import StreamInlet, resolve_stream, resolve_streams
# import asyncio

# app = Flask(__name__)

# class Store:
#     def __init__(self):
#         self.plot = None
#         self.time_inlet = None
#         self.gp = None
#         self.time_inlet_gp = None
#         self.ecg = None
#         self.hyp = None 
#         self.time_inlet_hyp = None

# saved = Store()

# # streams = resolve_streams()
# # for info in streams:
# #     print(info.name())
# streams = resolve_stream('name', 'Change_parm')
# inlet = StreamInlet(streams[0])
# streams = resolve_stream('name', 'plot_data_GP')
# inlet_gp = StreamInlet(streams[0])
# streams = resolve_stream('name', 'polar ECG')
# inlet_ecg = StreamInlet(streams[0])
# streams = resolve_stream('name', 'Hyp_parm')
# inlet_hyp = StreamInlet(streams[0])


# @app.get('/OptimizationData')
# def list_OptimizationData():
#     in_memory_datastore = {
#         "Change_parm": {"data_plot": saved.plot, "time_inlet": saved.time_inlet},
#         "plot_data_GP": {"data_gp": saved.gp, "time_inlet_gp": saved.time_inlet_gp},
#         "Hyp_parm": {"data_hyp": saved.hyp, "time_inlet_hyp": saved.time_inlet_hyp},
#     }
#     return in_memory_datastore

# @app.get('/polarECG')
# def list_ECGData():
#     data_ecg, time_inlet_ecg = inlet_ecg.pull_chunk(timeout=0.2)
#     if not (data_ecg == []):
#         saved.ecg = data_ecg
#     in_memory_datastore = {
#         "polar ECG": {"data_ecg": saved.ecg},
#     }
#     return in_memory_datastore


# async def run_code():
#     while True:
#         data_plot, time_inlet = inlet.pull_sample(timeout=0.1)
#         if data_plot is not None and data_plot != saved.plot:
#             saved.plot = data_plot
#             saved.time_inlet = time_inlet

#         data_gp, time_inlet_gp = inlet_gp.pull_chunk(timeout=0.1)
#         if not (data_gp == []):
#             saved.gp = data_gp
#             saved.time_inlet_gp = time_inlet_gp

#         data_hyp, time_inlet_hyp = inlet_hyp.pull_sample(timeout=0.1)
#         if data_hyp is not None and data_hyp != saved.hyp:
#             saved.hyp = data_hyp
#             saved.time_inlet_hyp = time_inlet_hyp

# if __name__ == '__main__':
#    loop = asyncio.get_event_loop()
#    tasks = [run_code(), loop.run_in_executor(None, app.run)]
#    loop.run_until_complete(asyncio.gather(*tasks))
   
      
        