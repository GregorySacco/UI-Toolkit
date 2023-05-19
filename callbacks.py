import plotly.graph_objs as go
import math
import numpy as np

def updateLiveGP(obj, config):
    [parmMin, parmMax]= config['Optimization']['range'][0]
    n_parm = config['Optimization']['n_parms']

    data_plot = obj.data['Change_parm']['data_plot']
    time_inlet = obj.data['Change_parm']['time_inlet']
    data_gp = obj.data['plot_data_GP']['data_gp']
    time_inlet_gp = obj.data['plot_data_GP']['time_inlet_gp']
    match n_parm:
                case 1:                   
                    if time_inlet is not None:
                        obj.parameter1.append(data_plot[1])
                        obj.GPy.append(data_plot[0])
                        data = go.Scatter(x=list(obj.parameter1), y=list(obj.GPy), name='cost_sample', mode="markers")
                        obj.HistGP = [data]

                    if time_inlet_gp is not None:
                        gp_list = [i[0] for i in data_gp]
                        obj.GP_data_plot = gp_list
                    if not(obj.GP_data_plot == []): 
                        data_1 = go.Scatter(x=list(np.linspace(0,85,100)), y=obj.GP_data_plot, name='GP', mode="lines")
                        obj.HistGP = [data, data_1]
                    
                    layout = go.Layout(xaxis = dict(title='Parameter',range=[parmMin, parmMax]),
                                            yaxis=dict(title='Cost'))
                    return {'data':obj.HistGP, 'layout':layout}
                
                case 2:
                    if len(time_inlet_gp):
                        gp_list = [i[0] for i in data_gp]
                        n = len(gp_list)
                        gp_size = int(math.sqrt(n))
                        obj.GP_data_plot = [gp_list[i:i+gp_size] for i in range(0, n, gp_size)]

                    if time_inlet is not None:
                        if data_plot[0]:
                            obj.parameter1.append(data_plot[1])
                            obj.parameter2.append(data_plot[2])
                            obj.GPy.append(data_plot[0])   

                    x_scale = 1.4
                    y_scale = 1.4  
                    z_scale = 0.5
                    layout=go.Layout(xaxis = dict(range=[parmMin, parmMax]),yaxis=dict(range=[parmMin, parmMax]),
                                    scene=dict(xaxis_title='Parameter 1', yaxis_title='Parameter 2',
                                    zaxis_title='Cost', aspectmode='manual', aspectratio=dict(x=x_scale,
                                    y=y_scale, z=z_scale)), width=700, margin=dict(r=10, b=40, l=10, t=0))                  
                                     
                    data=go.Scatter3d(x=list(obj.parameter1), y=list(obj.parameter2), z=list(obj.GPy), 
                                    name='cost_samples', mode="markers")
                    obj.HistGP = [data]

                    ###################################
                    if obj.GP_data_plot is not None:
                        nx,ny = (30,30)
                        x = np.linspace(0,85, nx)
                        y= np.linspace(0,85, ny)
                        data_1 = go.Surface(x=x,y=y,z=obj.GP_data_plot, name='GP',opacity=0.50) 
                        obj.HistGP = [data, data_1]
                    
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

def updateParmIterationGraph(obj, config):
    n_parm = config['Optimization']['n_parms']
    time_inlet = obj.data['Change_parm']['time_inlet']
    data_plot = obj.data['Change_parm']['data_plot']
    if time_inlet is not None and not(time_inlet == obj.previous_parm):
        obj.previous_parm = time_inlet
        if n_parm>=1: 
            obj.parameter1.append(data_plot[1])
            data1 = go.Scatter(y=obj.parameter1, name='Parameter1', mode="lines")
            obj.HistParm = [data1]
            if n_parm>=2:
                    obj.parameter2.append(data_plot[2])
                    data2 = go.Scatter(y=obj.parameter2, name='Parameter2', mode="lines")  
                    obj.HistParm = [data1, data2]   
                    if n_parm>=3:
                        obj.parameter3.append(data_plot[3])
                        data3 = go.Scatter(y=obj.parameter3, name='Parameter3', mode="lines")  
                        obj.HistParm = [data1, data2, data3] 
                        if n_parm>=4:
                            obj.parameter4.append(data_plot[4])
                            data4 = go.Scatter(y=obj.parameter4, name='Parameter4', mode="lines")  
                            obj.HistParm = [data1, data2, data3, data4]
                            if n_parm>=5:
                                obj.parameter5.append(data_plot[5])
                                data5 = go.Scatter(y=obj.parameter5, name='Parameter5', mode="lines")  
                                obj.HistParm = [data1, data2, data3, data4, data5]
                                if n_parm==6:
                                    obj.parameter6.append(data_plot[6])
                                    data6 = go.Scatter(y=obj.parameter6, name='Parameter6', mode="lines")  
                                    obj.HistParm = [data1, data2, data3, data4, data5, data6]
                
    return {'data':obj.HistParm}


def reset(obj):
        obj.parameter1 = []  
        obj.parameter2 = []  
        obj.parameter3 = []  
        obj.parameter4 = []  
        obj.parameter5 = []  
        obj.parameter6 = [] 
        obj.GPy = []
        obj.Acq_data_plot = None
        obj.GP_data_plot = []
        obj.ECGy =[]
        obj.HistParm=[]
        obj.HistGP = []
        obj.previous_parm = 0
        obj.data = {}
        obj.dataECG = {}