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
    obj.data = requests.get('http://127.0.0.1:5000/OptimizationData').json()
    
    obj.GPy = obj.data['data_plot']['y']
    j = 0
    obj.parameters = {1:[],2:[],3:[],4:[],5:[],6:[]}  
    for list in obj.data['data_plot']['x']:
        for i in range(n_parm):
            obj.parameters[i+1].append(obj.data['data_plot']['x'][j][i])
        j+=1
    
    for _ in obj.data['data_gp']:
        if _ == 'mean':
            obj.GP_data_plot2D = obj.data['data_gp']['mean']
        else:
            obj.data_gp_lin[_] = obj.data['data_gp'][_] 

    # data_acq = obj.data['data_acq']
    data_ecg = obj.data['data_ecg']

    for hyp_name in obj.data['data_hyp']:
        obj.hyperparameters[hyp_name] = obj.data['data_hyp'][hyp_name]


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
        # obj.HistGP[i-1][j-1] = [data]
        # if not(obj.GP_data_plot2D == []): 
        #     # nx,ny = (30,30)
        #     # nnx = np.linspace(0,85, nx)
        #     # nny= np.linspace(0,85, ny)
        #     data_2D = go.Surface(x=obj.data_gp_lin['x'], y=obj.data_gp_lin['y'], z=obj.GP_data_plot2D, name='GP',opacity=0.50, showscale=False) 
            # obj.HistGP[i-1][j-1] = [data, data_2D]
        return {'data':[data], 'layout':layout}
    

# def updateAcqGraph(obj, config):
    #     [parmMin, parmMax]= config['Optimization']['range'][0]
    #     n_parm = config['Optimization']['n_parms']

    #     data_plot, time_inlet = inlet.pull_sample(timeout=0.2)
    #     data_acq, time_inlet_acq = inlet_acq.pull_chunk(timeout=0.2)
    #     if len(time_inlet_acq):
    #         acq_list = [i[0] for i in data_acq]
    #         self.Acq_data_plot = acq_list
    #     match n_parm:
    #         # case 1:
    #         #     if disable == False:
    #         #         self.parameter1.append(random.randint(parmMin, parmMax))
    #         #         self.Acqy.append(random.randint(costMin, costMax))
    #         #     layout = go.Layout(xaxis = dict(title='Parameter',range=[parmMin, parmMax]),
    #         #         yaxis=dict(title='Cost',range=[min(self.Acqy), max(self.Acqy)]))  #,title='Gaussian Process')
    #         #     data = go.Scatter(x=list(self.parameter1), y=list(self.Acqy), name='gp', mode="lines+markers")
    #         #     return {'data':[data], 'layout':layout}
            
    #         case 2:
    #             if time_inlet is not None:
    #                 if data_plot[0]:
    #                     self.parameter1.append(data_plot[1])
    #                     self.parameter2.append(data_plot[2])

    #             layout = go.Layout(scene = dict(xaxis_title='Parameter 1', yaxis_title='Parameter 2',
    #                             zaxis_title='Cost'), width=600, margin=dict(r=10, b=10, l=10, t=10))
    #             if self.Acq_data_plot is not None:
    #                 nx,ny = (30,30)
    #                 x = np.linspace(0,85, nx)
    #                 y= np.linspace(0,85, ny)
    #                 xv, yv = np.meshgrid(x,y)
    #                 data = go.Mesh3d(x=xv.flatten(), y=yv.flatten(), z=list(self.Acq_data_plot), name='Acq',opacity=0.50)
    #                 return {'data':[data], 'layout':layout} 

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
    obj.HistParm = []
    obj.HistGP = [[[] for _ in range(6)] for _ in range(6)]
    # obj.HistHyp = {hyp_order[1]:[], hyp_order[2]:[],
    #                hyp_order[3]:[], hyp_order[4]:[],
    #                hyp_order[5]:[], hyp_order[6]:[]}
    obj.time_inlet = None
    obj.time_inlet_gp = None
    obj.time_inlet_hyp = None
    obj.previous_parm = None
    obj.previous_data = None
    obj.previous_hyp = None
    obj.data = {}
    obj.dataECG = {}
    obj.flags = {'server': 1, 'optimization': 0}
        
        
    