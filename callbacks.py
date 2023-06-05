import plotly.graph_objs as go
import math
import numpy as np
import requests


class HYP:
    def __init__(self):
        self.order =   {1: 'likelihood.noise_covar.raw_noise',
                        2: 'mean_module.raw_constant',
                        3: 'covar_module.raw_outputscale',
                        4: 'covar_module.base_kernel.raw_lengthscale',
                        5: 'hyperparameter 5',
                        6: 'hyperparameter 6'}
hyp = HYP()

def download_data(obj, config):
    n_parm = config['Optimization']['n_parms']
    server_flag = requests.get('http://127.0.0.1:5000/OptimizationData')
    if server_flag.status_code == 200:
        obj.flags['server'] = 'ON'
    else:
        obj.flags['server'] = 'OFF'
    data = server_flag.json()

    obj.GPy = data['data_plot']['y']
    j = 0
    obj.parameters = {1:[],2:[],3:[],4:[],5:[],6:[]}  
    for list in data['data_plot']['x']:
        for i in range(n_parm):
            obj.parameters[i+1].append(data['data_plot']['x'][j][i])
        j+=1
    
    for coordinate in data['data_gp']:
        if coordinate == 'mean':
            gp_list = data['data_gp']['mean']
            n = len(gp_list)
            gp_size = int(math.sqrt(n))
            obj.GP_data_plot2D = [gp_list[i:i+gp_size] for i in range(0, n, gp_size)]
        else:
            obj.data_gp_lin[coordinate] = data['data_gp'][coordinate] 

    acq_list = data['data_acq']
    n = len(acq_list)
    acq_size = int(math.sqrt(n))
    obj.Acq_data_plot = [acq_list[i:i+acq_size] for i in range(0, n, acq_size)]

    obj.flags['optimization'] = data['state']

    for hyp_name in data['data_hyp']:
        obj.hyperparameters[hyp_name] = data['data_hyp'][hyp_name]

    obj.ECGy = [item for sublist in data['data_ecg'] for item in sublist]
    obj.HRVy = data['data_hrv']

def updateECG(obj):
    data = go.Scatter(y= obj.ECGy, name='ECG', mode="lines")
    layout = go.Layout(xaxis = dict(title='Time'),yaxis=dict(title='mV'),title='ECG')
    return {'data': [data], 'layout': layout}

def updateHRV(obj):
    data = go.Scatter(y= obj.HRVy, name='HRV', mode="lines")
    layout = go.Layout(xaxis = dict(title='Time'),yaxis=dict(title='mV'),title='HRV')
    return {'data': [data], 'layout': layout}

def updateLiveGP(obj, config, x, y):
    [parmMin, parmMax]= config['Optimization']['range'][0]
    n_parm = config['Optimization']['n_parms']
    if n_parm == 1 or (n_parm>1 and x == y):
        layout = go.Layout(xaxis = dict(title='Parameter',range=[parmMin, parmMax]),
                                    yaxis=dict(title='Cost'))
            
    else:
        scale= {'x':1.4, 'y':1.4, 'z':0.5}
        layout=go.Layout(xaxis = dict(range=[parmMin, parmMax]),yaxis=dict(range=[parmMin, parmMax]),
                            scene=dict(xaxis_title=f'Parameter{x}', yaxis_title=f'Parameter{y}',
                            zaxis_title='Cost', aspectmode='manual', aspectratio=dict(x=scale['x'],
                            y=scale['y'], z=scale['z'])), margin=dict(r=10, b=40, l=10, t=0)) 

    if n_parm == 1:                   
        if obj.time_inlet is not None:
            data = go.Scatter(x=list(obj.parameters[1]), y=list(obj.GPy), name='cost_sample', mode="markers")
            obj.HistGP[1][1] = [data]
        if not(obj.GP_data_plot == []): 
            data_1 = go.Scatter(x=list(np.linspace(parmMin,parmMax,100)), y=obj.GP_data_plot1D, name='GP', mode="lines")
            obj.HistGP[1][1] = [data, data_1]
        return {'data':obj.HistGP[1][1], 'layout':layout}
    
        
    if n_parm >= 2:
        data=go.Scatter3d(x=list(obj.parameters[x]), y=list(obj.parameters[y]), z=list(obj.GPy), 
                        name='cost_samples', mode="markers")
        
        obj.HistGP = [data]
        if not(obj.GP_data_plot2D == []): 
        #     # nx,ny = (30,30)
        #     # nnx = np.linspace(0,85, nx)
        #     # nny= np.linspace(0,85, ny)
            data_surf = go.Surface(x=obj.data_gp_lin['x'], y=obj.data_gp_lin['y'],
                                z=obj.GP_data_plot2D, name='GP',opacity=0.50, showscale=False) 
            obj.HistGP = [data, data_surf]
        return {'data':obj.HistGP, 'layout':layout}
    

def updateAcqGraph(obj, config):
    [parmMin, parmMax]= config['Optimization']['range'][0]
    n_parm = config['Optimization']['n_parms']
    if n_parm == 1:
        layout = go.Layout(xaxis = dict(title='Parameter',range=[parmMin, parmMax]),
                                    yaxis=dict(title='Acquisition function'))
            
    else:
        scale= {'x':1.4, 'y':1.4, 'z':0.5}
        layout=go.Layout(xaxis = dict(range=[parmMin, parmMax]),yaxis=dict(range=[parmMin, parmMax]),
                            scene=dict(xaxis_title='Parameter1', yaxis_title='Parameter2',
                            zaxis_title='Cost', aspectmode='manual', aspectratio=dict(x=scale['x'],
                            y=scale['y'], z=scale['z'])), margin=dict(r=10, b=40, l=10, t=0)) 

    if n_parm == 1:                   
        if obj.time_inlet is not None:
            data = go.Scatter(x=list(obj.parameters[1]), y=list(obj.GPy), name='cost_sample', mode="markers")
            obj.HistGP[1][1] = [data]
        if not(obj.GP_data_plot == []): 
            data_1 = go.Scatter(x=list(np.linspace(parmMin,parmMax,100)), y=obj.GP_data_plot1D, name='GP', mode="lines")
            obj.HistGP[1][1] = [data, data_1]
        return {'data':obj.HistGP[1][1], 'layout':layout}
    
        
    if n_parm >= 2:
        if not(obj.Acq_data_plot == []):
            nx,ny = (30,30) 
            x = np.linspace(0,85, nx)
            y= np.linspace(0,85, ny)
            xv, yv = np.meshgrid(x,y)
            data = go.Surface(x=obj.data_gp_lin['x'], y=obj.data_gp_lin['y'],
                                z=obj.Acq_data_plot, name='GP',opacity=0.50, showscale=False) 
            obj.HistAcq = [data]
        return {'data':obj.HistAcq, 'layout':layout}
    

def updateParmIterationGraph(obj, n_parm):
    obj.HistParm = []
    for i in range(1,(n_parm+1)):
        data = go.Scatter(y=obj.parameters[i], name=f'Parameter{i}', mode="lines")
        obj.HistParm.append(data)
    return {'data': obj.HistParm}

def updateHyperParm(obj, hyp_name):   
    data = go.Scatter(y=obj.hyperparameters[hyp_name], name=f'Hyper {hyp_name}', mode="lines")
    return {'data': [data]}


def reset(obj):
    obj.parameters = {1:[],2:[],3:[],4:[],5:[],6:[]}  
    obj.hyperparameters = {hyp.order[1]:[], hyp.order[2]:[],
                           hyp.order[3]:[], hyp.order[4]:[],
                           hyp.order[5]:[], hyp.order[6]:[]}
    obj.GPy = []
    obj.Acq_data_plot = None
    obj.GP_data_plot1D = []
    obj.GP_data_plot2D = []
    obj.data_gp_lin = {'x':[], 'y':[]}
    obj.ECGy =[]
    obj.HRVy =[]
    obj.HistParm = []
    obj.HistGP = []
    obj.HistAcq = []
    obj.data = {}
    obj.flags = {'server': 'OFF', 'optimization': 'OFF'}
        
        
    