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
        self.acq = None
        self.hyp = None 
        self.state = None
        self.hrv = None
        self.IP = "tcp://192.168.1.43"
        self.port = "45"

saved = Store()
print('hellooooo')

async def async_process(msg, person):
    # print(msg, person)
    pass


async def data_plot():
    sock = ctx.socket(zmq.SUB)
    sock.subscribe("")
    sock.connect(f"{saved.IP}:{saved.port}01")
    while True:
        try:
            msg = await sock.recv_json(flags=zmq.NOBLOCK) # waits for msg to be ready
        except zmq.ZMQError:
            msg = None
        await async_process(msg, 'data_plot')
        if msg is not None and msg != saved.plot:
            saved.plot = msg
        await asyncio.sleep(0.1)

async def data_gp():
    sock = ctx.socket(zmq.SUB)
    sock.subscribe("")
    sock.connect(f"{saved.IP}:{saved.port}02")
    while True:
        try:
            msg = await sock.recv_json(flags=zmq.NOBLOCK) # waits for msg to be ready
        except zmq.ZMQError:
            msg = None
        # reply = await async_process(msg, 'data_gp')
        if msg is not None and msg != saved.gp:
            saved.gp = msg
        await asyncio.sleep(0.1)

async def data_acq():
    sock = ctx.socket(zmq.SUB)
    sock.subscribe("")
    sock.connect(f"{saved.IP}:{saved.port}03")
    while True:
        try:
            msg = await sock.recv_json(flags=zmq.NOBLOCK) # waits for msg to be ready
        except zmq.ZMQError:
            msg = None
        reply = await async_process(msg, 'data_acq')
        if msg is not None and msg != saved.acq:
            saved.acq = msg
        await asyncio.sleep(0.1)

async def data_ecg():
    sock = ctx.socket(zmq.SUB)
    sock.subscribe("")
    sock.connect(f"{saved.IP}:{saved.port}09")
    while True:
        try:
            msg = await sock.recv_json(flags=zmq.NOBLOCK) # waits for msg to be ready
        except zmq.ZMQError:
            msg = None
        reply = await async_process(msg, 'data_ecg')
        if msg is not None:
            saved.ecg = msg
            
        await asyncio.sleep(0.1)

async def data_hrv():
    sock = ctx.socket(zmq.SUB)
    sock.subscribe("")
    sock.connect(f"{saved.IP}:{saved.port}10")
    while True:
        try:
            msg = await sock.recv_json(flags=zmq.NOBLOCK) # waits for msg to be ready
        except zmq.ZMQError:
            msg = None
        reply = await async_process(msg, 'data_hrv')
        if msg is not None and msg != saved.hrv:
            saved.hrv = msg
        await asyncio.sleep(0.1)

async def data_hyp():
    sock = ctx.socket(zmq.SUB)
    sock.subscribe("")
    sock.connect(f"{saved.IP}:{saved.port}04")
    while True:
        try:
            msg = await sock.recv_json(flags=zmq.NOBLOCK) # waits for msg to be ready
        except zmq.ZMQError:
            msg = None
        reply = await async_process(msg, 'data_hyp')
        if msg is not None and msg != saved.hyp:
            saved.hyp = msg
        await asyncio.sleep(0.1)


async def opt_state():
    sock = ctx.socket(zmq.SUB)
    sock.subscribe("")
    sock.connect(f"{saved.IP}:{saved.port}07")
    while True:
        try:
            msg = await sock.recv_json(flags=zmq.NOBLOCK) # waits for msg to be ready
        except zmq.ZMQError:
            msg = None
        reply = await async_process(msg, 'state')
        if msg is not None and msg != saved.state:
            saved.state = msg
        await asyncio.sleep(0.1)



app = Flask(__name__)

@app.get('/OptimizationData')
def list_OptimizationData():
    in_memory_datastore = {
        "data_plot": saved.plot,
        "data_gp": saved.gp,
        "data_acq": saved.acq,
        "data_hyp": saved.hyp,
        "data_ecg": saved.ecg,
        "data_hrv": saved.hrv,
        "state": saved.state}
    return in_memory_datastore


if __name__ == '__main__':
   loop = asyncio.get_event_loop()
   tasks = [data_plot(), 
            data_ecg(),
            data_hrv(),
            data_hyp(),
            data_gp(),
            data_acq(),
            opt_state(),
            loop.run_in_executor(None, app.run)]
   loop.run_until_complete(asyncio.gather(*tasks))

   
      
        