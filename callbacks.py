import plotly.graph_objs as go
import math
import numpy as np
import requests
import ast


class HYP:
    def __init__(self):
        self.order =   {1: 'likelihood.noise_covar.raw_noise',
                        2: 'mean_module.raw_constant',
                        3: 'covar_module.raw_outputscale',
                        4: 'lengthscale parm1',
                        5: 'lengthscale parm2',
                        6: 'hyperparameter 6'}
hyp = HYP()

def download_data(obj, config):
    n_parm = config['Optimization']['n_parms']
    server_flag = requests.get(f'http://{obj.serverIP}:{obj.serverPort}/OptimizationData')
    if server_flag.status_code == 200:
        obj.flags['server'] = 'ON'
    else:
        obj.flags['server'] = 'OFF'
    data = server_flag.json()
    if data['data_plot']['y'] != []:
        obj.GPy = data['data_plot']['y']
        j = 0
        obj.parameters = {1:[],2:[],3:[],4:[],5:[],6:[]}  
        for block in data['data_plot']['x']:
            #print('BLOCK', block)
            for i in range(n_parm):
                #print('JEEYY',j)
                obj.parameters[i+1].append(data['data_plot']['x'][j][i])
            j+=1

    for coordinate in data['data_gp']:
        if coordinate == 'mean':
            gp_list = data['data_gp']['mean']
            if not(gp_list == []):
                if n_parm == 1 :
                    n = len(gp_list)
                    obj.GP_data_plot = [gp_list[i] for i in range(n)]
                else:
                    n = len(gp_list)
                    gp_size = int(math.sqrt(n))
                    obj.GP_data_plot = [gp_list[i:i+gp_size] for i in range(0, n, gp_size)]
        else:
            obj.data_gp_lin[coordinate] = data['data_gp'][coordinate] 
            
    acq_list = data['data_acq']
    if not(acq_list is None):
        if n_parm == 1:
            n = len(acq_list)
            obj.Acq_data_plot = [acq_list[i] for i in range(n)]
        else:
            n = len(acq_list)
            acq_size = int(math.sqrt(n))
            obj.Acq_data_plot = [acq_list[i:i+acq_size] for i in range(0, n, acq_size)]
            
    obj.flags['optimization'] = data['state']
    
    for hyp_name in data['data_hyp']:
        if data['data_hyp'] != []:
            obj.hyperparameters[hyp_name] = data['data_hyp'][hyp_name]
            
    if data['data_ecg'] != []:
        obj.ECGy = [item for sublist in data['data_ecg'] for item in sublist]
        
    obj.HRVy = data['data_hrv']
    #print(obj.hyperparameters)

def updateECG(obj):
    data = go.Scatter(y= obj.ECGy, name='ECG', mode="lines")
    layout = go.Layout(xaxis = dict(title='Time'),yaxis=dict(title='mV'),title='ECG')
    return {'data': [data], 'layout': layout}

def updateHRV(obj):
    data = go.Scatter(y= obj.HRVy, name='HRV', mode="lines")
    layout = go.Layout(xaxis = dict(title='Time'),yaxis=dict(title='mV'),title='HRV')
    return {'data': [data], 'layout': layout}

def updateLiveGP(obj, config):
    n_parm = config['Optimization']['n_parms']
    if n_parm == 1:
        parmRange = config['Optimization']['range'][0]
        layout = go.Layout(xaxis = dict(title='Parameter',range=parmRange),
                                    yaxis=dict(title='Cost'))
            
    else:
        scale= {'x':1.4, 'y':1.4, 'z':0.5}
        ranges = config['Optimization']['range']
        parmRange1= [int(num) for num in ranges[0]]
        parmRange2= [int(num) for num in ranges[1]]
        layout=go.Layout(xaxis = dict(range=parmRange1),yaxis=dict(range=parmRange2),
                            scene=dict(xaxis_title=f'Parameter1', yaxis_title=f'Parameter2',
                            zaxis_title='Cost', aspectmode='manual', aspectratio=dict(x=scale['x'],
                            y=scale['y'], z=scale['z'])), margin=dict(r=10, b=40, l=10, t=0)) 

    if n_parm == 1:                   
        data = go.Scatter(x=list(obj.parameters[1]), y=list(obj.GPy), name='cost_sample', mode="markers")
        obj.HistGP = [data]
        if not(obj.GP_data_plot == []): 
            data_1 = go.Scatter(x=list(np.linspace(parmRange[0],parmRange[1],100)), y=obj.GP_data_plot, name='GP', mode="lines")
            obj.HistGP = [data, data_1]
        return {'data':obj.HistGP, 'layout':layout}
    
        
    if n_parm >= 2:
        data=go.Scatter3d(x=list(obj.parameters[1]), y=list(obj.parameters[2]), z=list(obj.GPy), 
                        name='cost_samples', mode="markers")
        
        obj.HistGP = [data]
        if not(obj.GP_data_plot == []): 
            data_surf = go.Surface(x=obj.data_gp_lin['x'], y=obj.data_gp_lin['y'],
                                z=obj.GP_data_plot, name='GP',opacity=0.50, showscale=False) 
            obj.HistGP = [data, data_surf]
        return {'data':obj.HistGP, 'layout':layout}
    

def updateAcqGraph(obj, config):
    n_parm = config['Optimization']['n_parms']
    if n_parm == 1:
        parmRange = config['Optimization']['range'][0]
        layout = go.Layout(xaxis = dict(title='Parameter',range=parmRange),
                                    yaxis=dict(title='Acquisition function'))
            
    else:
        scale= {'x':1.4, 'y':1.4, 'z':0.5}
        #print(config['Optimization']['range'])
        ranges = config['Optimization']['range']
        
        #print(config['Optimization']['range'])
        
        parmRange1= [int(num) for num in ranges[0]]
        parmRange2= [int(num) for num in ranges[1]]
        layout=go.Layout(xaxis = dict(range=parmRange1),yaxis=dict(range=parmRange2),
                            scene=dict(xaxis_title='Parameter1', yaxis_title='Parameter2',
                            zaxis_title='Cost', aspectmode='manual', aspectratio=dict(x=scale['x'],
                            y=scale['y'], z=scale['z'])), margin=dict(r=10, b=40, l=10, t=0)) 

    if n_parm == 1:                   
        if not(obj.Acq_data_plot == []): 
        # 
            data = go.Scatter(x=list(np.linspace(parmRange[0],parmRange[1],100)), y=obj.Acq_data_plot, name='Acq', mode="lines")
            obj.HistAcq = [data]
        return {'data':obj.HistAcq, 'layout':layout}
    
        
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
    layout = go.Layout(xaxis = dict(title='Iteration'),yaxis=dict(title='Parameter value'),title='Parameters')
    return {'data': obj.HistParm, 'layout': layout}

def updateHyperParm(obj, hyp_name):   
    data = go.Scatter(y=obj.hyperparameters[hyp_name], name=f'{hyp_name}', mode="lines")
    return {'data': [data]}


def reset(obj):
    obj.parameters = {1:[],2:[],3:[],4:[],5:[],6:[]}  
    obj.hyperparameters = {hyp.order[1]:[], hyp.order[2]:[],
                           hyp.order[3]:[], hyp.order[4]:[],
                           hyp.order[5]:[], hyp.order[6]:[]}
    obj.GPy = []
    obj.Acq_data_plot = None
    obj.GP_data_plot = []
    obj.data_gp_lin = {'x':[], 'y':[]}
    obj.ECGy =[]
    obj.HRVy =[]
    obj.HistParm = []
    obj.HistGP = []
    obj.HistAcq = []
    obj.data = {}
    obj.flags = {'server': 'OFF', 'optimization': 'OFF'}
    obj.serverIP = '127.0.0.1'
    obj.serverPort = '5000'
        
        
    
