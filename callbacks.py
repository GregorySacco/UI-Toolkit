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
    for i in range(1, n_parm+1):
        obj.parameters[i] = obj.data['data_plot']['x'][i]

    data_gp = obj.data['data_gp']
    data_hyp = obj.data['data_hyp']
    data_acq = obj.data['data_acq']
    data_ecg = obj.data['data_ecg']


    # if obj.time_inlet is not None and data_plot[0] and obj.time_inlet != obj.previous_data:
    #     obj.previous_data = obj.time_inlet
    #     obj.GPy.append(data_plot[0]) 
    #     for i in range(1,len(data_plot)):
    #         obj.parameters[i].append(data_plot[i])

    # if obj.time_inlet_gp is not None:
    #     gp_list = [i[0] for i in data_gp]
    #     obj.GP_data_plot1D = gp_list
    #     n = len(gp_list)
    #     gp_size = int(math.sqrt(n))
    #     obj.GP_data_plot2D = [gp_list[i:i+gp_size] for i in range(0, n, gp_size)]
    
    # if obj.time_inlet_hyp is not None and data_hyp[0] and obj.time_inlet_hyp != obj.previous_hyp:
    #     obj.previous_hyp = obj.time_inlet_hyp
    #     for i in range(1, len(data_hyp)+1):
    #         obj.hyperparameters[hyp_order[i]].append(data_hyp[i-1])

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
    
    #GP PLOT UPDATE 
        
    # if n_parm >= 2:
    #     for i in range(1,n_parm+1):
    #         for j in range(1,n_parm+1):
    #             if i == j:
    #                 if obj.parameters[i] is not None:
    #                     data = go.Scatter(x=list(obj.parameters[i]), y=list(obj.GPy), name='cost_sample', mode="markers")
    #                     obj.HistGP[i-1][j-1] = [data]
    #                 if not(obj.GP_data_plot1D == []): 
    #                     data_1D = go.Scatter(x=list(np.linspace(parmMin,parmMax,100)), y=obj.GP_data_plot1D, name='GP', mode="lines")
    #                     obj.HistGP[i-1][j-1] = [data, data_1D]
    #             else:
    #                 data=go.Scatter3d(x=list(obj.parameters[i]), y=list(obj.parameters[j]), z=list(obj.GPy), 
    #                                 name='cost_samples', mode="markers")
    #                 obj.HistGP[i-1][j-1] = [data]
    #                 if not(obj.GP_data_plot2D == []): 
    #                     nx,ny = (30,30)
    #                     nnx = np.linspace(0,85, nx)
    #                     nny= np.linspace(0,85, ny)
    #                     data_2D = go.Surface(x=nnx,y=nny,z=obj.GP_data_plot2D, name='GP',opacity=0.50, showscale=False) 
    #                     obj.HistGP[i-1][j-1] = [data, data_2D]
        # return {'data':obj.HistGP[x-1][y-1], 'layout':layout}
    

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
    # if obj.time_inlet is not None and obj.time_inlet != obj.previous_parm:
    #     obj.HistParm = []
    for i in range(1,(n_parm+1)):
        data = go.Scatter(y=obj.parameters[i], name=f'Parameter{i}', mode="lines")
        # obj.HistParm.append(data)
    return {'data': data}

def updateHyperParm(obj, hyp_name):
    # if obj.time_inlet_hyp is not None:
    #     obj.HistHyp[hyp_name] = []    
    data = go.Scatter(y=obj.hyperparameters[hyp_name], name=f'Hyper {hyp_name}', mode="lines")
        # obj.HistHyp[hyp_name].append(data)
    return {'data': data}


def reset(obj):
    obj.parameters = {1:[],2:[],3:[],4:[],5:[],6:[]}  
    obj.hyperparameters = {hyp.order[1]:[], hyp.order[2]:[],
                           hyp.order[3]:[], hyp.order[4]:[],
                           hyp.order[5]:[], hyp.order[6]:[]}
    obj.GPy = []
    obj.Acq_data_plot = None
    obj.GP_data_plot1D = []
    obj.GP_data_plot2D = []
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
        
        
    