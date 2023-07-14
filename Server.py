#!/usr/bin/env python3.10
import asyncio
import zmq
import zmq.asyncio
from flask import Flask, request
import requests

ctx = zmq.asyncio.Context()
#ctx = zmq.Context()

class Store:
    def __init__(self):
        self.IP = "tcp://192.168.1.7"  # IP of computer where we run opt code
        self.port = "45"
        self.reset_data()

    def reset_data(self):
        self.plot = {'x': [], 'y':[]}
        self.gp = {'mean': [], 'x': [], 'y':[]}
        self.ecg = []
        self.acq = None
        self.hyp = {'likelihood.noise_covar.raw_noise': [],
                    'mean_module.raw_constant': [],
                    'covar_module.raw_outputscale': [],
                    'lengthscale parm1': [],
                    'lengthscale parm2': [],
                    } 
        self.state = "OFF"        #state of the optimization process 
        self.hrv = None
        self.opt_comand = 'RESUME'    #command from UI for optimization 

    def share_data(self):
        in_memory_datastore = {
            "data_plot": self.plot,
            "data_gp": self.gp,
            "data_acq": self.acq,
            "data_hyp": self.hyp,
            "data_ecg": self.ecg,
            "data_hrv": self.hrv,
            "state": self.state}
        return in_memory_datastore

saved = Store()

async def data_plot():
    sock = ctx.socket(zmq.SUB)
    sock.subscribe("")
    sock.connect(f"{saved.IP}:{saved.port}01")
    while True:
        try:
            msg = await sock.recv_json(flags=zmq.NOBLOCK) # waits for msg to be ready
        except zmq.ZMQError:
            msg = None
        if msg is None and saved.plot is None:
            saved.plot = {'x': [], 'y':[]}
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
        if msg is None and saved.gp is None:
            saved.gp = {'mean': [], 'x': [], 'y':[]}
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
        if msg is not None and msg != saved.state:
            saved.state = msg
        await asyncio.sleep(0.1)


#async def opt_comand():
#    sock = ctx.socket(zmq.PUB)
#    sock.bind(f"tcp://192.168.1.7:{saved.port}08")   #IP of sender (the computer where we run server)
#    while True:
#        print(saved.opt_comand)
#        sock.send_json(saved.opt_comand)
#        await asyncio.sleep(0.1)

app = Flask(__name__)

@app.get('/OptimizationData')
def list_OptimizationData():
    return saved.share_data()
    
@app.get('/OptCommand')
def sendOptcommand():
    return saved.opt_comand

@app.post('/OptimizationData')
def reset_OptimizationData():
    saved.reset_data()
    return 'data reset'

@app.post('/OptResume')
def resume_opt():
    saved.opt_comand = "1"
    print('resume called')
    return 'comand received'
    
@app.post('/OptPause')
def pause_opt():
    saved.opt_comand = "0"
    print('pause called')
    return 'comand received'
    


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [data_plot(), 
            data_ecg(),
            data_hrv(),
            data_hyp(),
            data_gp(),
            data_acq(),
            opt_state(),
           # opt_comand(),
            loop.run_in_executor(None, app.run)]
    loop.run_until_complete(asyncio.gather(*tasks))
    
    
