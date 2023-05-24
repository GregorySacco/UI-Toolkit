import plotly.graph_objs as go
import math
import numpy as np
import requests

global hyp_order  
hyp_order = {1: 'likelihood.noise_covar.raw_noise',
                2: 'mean_module.raw_constant',
                3: 'covar_module.raw_outputscale',
                4: 'covar_module.base_kernel.raw_lengthscale',
                5: 'hyperparameter 5',
                6: 'hyperparameter 6'}

def download_data(obj, config):
    n_parm = config['Optimization']['n_parms']
    obj.data = requests.get('http://127.0.0.1:5000/OptimizationData').json()
    data_plot = obj.data['Change_parm']['data_plot']
    obj.time_inlet = obj.data['Change_parm']['time_inlet']
    data_gp = obj.data['plot_data_GP']['data_gp']
    obj.time_inlet_gp = obj.data['plot_data_GP']['time_inlet_gp']
    data_hyp = obj.data['Hyp_parm']['data_hyp']
    obj.time_inlet_hyp = obj.data['Hyp_parm']['time_inlet_hyp']

    if obj.time_inlet is not None and data_plot[0] and obj.time_inlet != obj.previous_data:
        obj.previous_data = obj.time_inlet
        obj.GPy.append(data_plot[0]) 
        for i in range(1,len(data_plot)):
            obj.parameters[i].append(data_plot[i])

    match n_parm: 
        case 1: 
            if obj.time_inlet_gp is not None:
                gp_list = [i[0] for i in data_gp]
                obj.GP_data_plot = gp_list
        case 2:
            if obj.time_inlet_gp is not None:
                gp_list = [i[0] for i in data_gp]
                n = len(gp_list)
                gp_size = int(math.sqrt(n))
                obj.GP_data_plot = [gp_list[i:i+gp_size] for i in range(0, n, gp_size)]
    
    if obj.time_inlet_hyp is not None and data_hyp[0] and obj.time_inlet_hyp != obj.previous_hyp:
        obj.previous_hyp = obj.time_inlet_hyp
        for i in range(1, len(data_hyp)+1):
            obj.hyperparameters[hyp_order[i]].append(data_hyp[i-1])

def updateLiveGP(obj, config):
    [parmMin, parmMax]= config['Optimization']['range'][0]
    n_parm = config['Optimization']['n_parms']
    if n_parm == 1:
        layout = go.Layout(xaxis = dict(title='Parameter',range=[parmMin, parmMax]),
                                    yaxis=dict(title='Cost'))
    else :
        scale= {'x':1.4, 'y':1.4, 'z':0.5}
        layout=go.Layout(xaxis = dict(range=[parmMin, parmMax]),yaxis=dict(range=[parmMin, parmMax]),
                            scene=dict(xaxis_title='Parameter 1', yaxis_title='Parameter 2',
                            zaxis_title='Cost', aspectmode='manual', aspectratio=dict(x=scale['x'],
                            y=scale['y'], z=scale['z'])), margin=dict(r=10, b=40, l=10, t=0)) 

    match n_parm:
        case 1:                   
            if obj.time_inlet is not None:
                data = go.Scatter(x=list(obj.parameters[1]), y=list(obj.GPy), name='cost_sample', mode="markers")
                obj.HistGP = [data]
            if not(obj.GP_data_plot == []): 
                data_1 = go.Scatter(x=list(np.linspace(parmMin,parmMax,100)), y=obj.GP_data_plot, name='GP', mode="lines")
                obj.HistGP = [data, data_1]
            return {'data':obj.HistGP, 'layout':layout}
        
        case 2:
            data=go.Scatter3d(x=list(obj.parameters[1]), y=list(obj.parameters[2]), z=list(obj.GPy), 
                            name='cost_samples', mode="markers")
            obj.HistGP = [data]
            if not(obj.GP_data_plot == []): 
                nx,ny = (30,30)
                x = np.linspace(0,85, nx)
                y= np.linspace(0,85, ny)
                data_1 = go.Surface(x=x,y=y,z=obj.GP_data_plot, name='GP',opacity=0.50, showscale=False) 
                obj.HistGP = [data, data_1]
            return {'data':obj.HistGP, 'layout':layout} 
        
        case 3:               
            samples=from3To6parm(obj, config)
            obj.HistGP = list(samples)
            return {'data':obj.HistGP, 'layout':layout} 
        
        case 4:               
            samples=from3To6parm(obj, config)
            obj.HistGP = list(samples)
            return {'data':obj.HistGP, 'layout':layout} 
        
        case 5:               
            samples=from3To6parm(obj, config)
            obj.HistGP = list(samples)
            return {'data':obj.HistGP, 'layout':layout} 
        
        case 6:               
            samples=from3To6parm(obj, config)
            obj.HistGP = list(samples)
            return {'data':obj.HistGP, 'layout':layout} 

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
    if obj.time_inlet is not None and obj.time_inlet != obj.previous_parm:
        obj.HistParm = []
        for i in range(1,(n_parm+1)):
            data = go.Scatter(y=obj.parameters[i], name=f'Parameter{i}', mode="lines")
            obj.HistParm.append(data)
    return {'data': obj.HistParm}

def updateHyperParm(obj, hyp_name):
    if obj.time_inlet_hyp is not None:
        obj.HistHyp[hyp_name] = []
        data = go.Scatter(y=obj.hyperparameters[hyp_name], name=f'Hyper {hyp_name}', mode="lines")
        obj.HistHyp[hyp_name].append(data)
    return {'data': obj.HistHyp[hyp_name]}


def from3To6parm(obj, config):
    [parmMin, parmMax]= config['Optimization']['range'][0]
    n_parm = config['Optimization']['n_parms']
    samp_size = len(obj.parameters[1])
    dim = {3: np.array([1]), 4: np.array([7 for e in range(samp_size)]), 
            5:['blue' for e in range(samp_size)]}  #3 for parm3, 4 for parm4, 5 for color of parm5 and parm6
    
    for j in range(3, n_parm+1):
        if j == 3:
            dim[3] = np.interp(obj.parameters[3], (parmMin, parmMax), (0.2, 1.0)) #opacity for parm3
            hover_info = [[f'parm1: {x}<br>parm2: {y}<br>parm3: {fv}<br>cost: {z}']
                for x, y, fv, z in zip(obj.parameters[1], obj.parameters[2], obj.parameters[3], obj.GPy)]
        if j == 4:
            dim[4] = np.interp(obj.parameters[4], (parmMin, parmMax), (3, 12))  #size for parm4
            hover_info = [[f'parm1: {x}<br>parm2: {y}<br>parm3: {fv}<br>param4: {sv}<br>cost: {z}']
                for x, y, fv, sv, z in zip(obj.parameters[1], obj.parameters[2], obj.parameters[3], obj.parameters[4], obj.GPy)]
        if j == 5:
            normalized_blue = [(value - parmMin) / (parmMax - parmMin) for value in obj.parameters[5]]
            dim[5] = ['rgb({}, {}, {})'.format(0, 0, int(255 * (blue))) for blue in normalized_blue]   #color(different levels of blue) for parm5
            hover_info = [[f'parm1: {x}<br>parm2: {y}<br>parm3: {fv}<br>param4: {sv}<br>parm5: {tv}<br>cost: {z}']
                for x, y, fv, sv, tv, z in zip(obj.parameters[1], obj.parameters[2], obj.parameters[3], obj.parameters[4], obj.parameters[5], obj.GPy)]
        if j == 6:
            normalized_green = [(value - parmMin) / (parmMax - parmMin) for value in obj.parameters[6]] #color(b/w green and blue) for parm5 and parm6
            dim[5] = ['rgb({}, {}, {})'.format(0, int(255 * (green)), int(255 * (blue))) for green, blue in zip(normalized_green, normalized_blue)]
            hover_info = [[f'parm1: {x}<br>parm2: {y}<br>parm3: {fv}<br>param4: {sv}<br>parm5: {tv}<br>parm6: {uv}<br>cost: {z}']
                for x, y, fv, sv, tv, uv, z in zip(obj.parameters[1], obj.parameters[2], obj.parameters[3], obj.parameters[4], obj.parameters[5], obj.parameters[6], obj.GPy)]
            
    samples= []
    for i in range(samp_size):
        sample = go.Scatter3d(x=np.array(obj.parameters[1][i]),y=np.array(obj.parameters[2][i]),z=np.array(obj.GPy[i]),
            mode='markers',
            showlegend=False,
            marker=dict(color=dim[5][i],opacity=dim[3][i],size=dim[4][i]),
            hovertemplate='%{customdata}', 
            customdata=hover_info[i]
        )
        samples.append(sample)   
    return samples   

def reset(obj):
    obj.parameters = {1:[],2:[],3:[],4:[],5:[],6:[]}  
    obj.hyperparameters = {hyp_order[1]:[], hyp_order[2]:[],
                           hyp_order[3]:[], hyp_order[4]:[],
                           hyp_order[5]:[], hyp_order[6]:[]}
    obj.GPy = []
    obj.Acq_data_plot = None
    obj.GP_data_plot = []
    obj.ECGy =[]
    obj.HistParm = []
    obj.HistGP = []
    obj.HistHyp = {hyp_order[1]:[], hyp_order[2]:[],
                   hyp_order[3]:[], hyp_order[4]:[],
                   hyp_order[5]:[], hyp_order[6]:[]}
    obj.time_inlet = None
    obj.time_inlet_gp = None
    obj.time_inlet_hyp = None
    obj.previous_parm = None
    obj.previous_data = None
    obj.previous_hyp = None
    obj.data = {}
    obj.dataECG = {}
        
        
    