import dash
from dash import html, dcc, ctx
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go
import numpy as np
import yaml
import math
import requests
from layouts import * 



class UI:
    def __init__(self):
        self.reset()

        minmax = {1: "min", 2:"max"}
        with open('ECG_config.yml', 'r') as file: config = yaml.safe_load(file)

        self.app = dash.Dash(__name__, suppress_callback_exceptions=True, 
                             external_stylesheets=[{'href': '/assets/bootstrap.min.css'}],
                meta_tags=[{'name':'viewport',
                            'content':'width=device-width, initial-scale=0.7, maximum-scale=3, minimum-scale=0.5'}])
        self.app.layout = layout_main


        @self.app.callback(Output('tabs-content', 'children'),
              Input('tabs-example', 'value'))
        def render_content(tab):
            if tab == 'init':
                return layout_init
            
            elif tab == 'opt':
                return layout_opt
                    
            elif tab == 'sig':
                return layout_sig
 
            elif tab == 'hyp':
                return layout_hyp

        @self.app.callback(Output("hidden-div", 'children', allow_duplicate=True),
                    Input('server_timer', 'n_intervals'),
                    prevent_initial_call=True)
        def download_server(n):
            if n is not None:
                self.data = requests.get('http://127.0.0.1:5000/OptimizationData').json()
        
        @self.app.callback(Output("hidden-div", 'children', allow_duplicate=True),
                    Input('ECG_timer', 'n_intervals'),
                    prevent_initial_call=True)
        def download_ECG(n):
            if n is not None:
                self.dataECG = requests.get('http://127.0.0.1:5000/polarECG').json()


        @self.app.callback(Output('parmBox','children'),
                    Input('parm_slider','value'),)
        def update_parmBox(n):
            return html.Div(
                    [html.Div([
                        html.Br(),
                        html.H5(f'Parameter {i+1}'),
                        html.Div([dcc.Input(id=f'input{i}{j}', type='number', placeholder=minmax[j+1],
                                            persistence=True, persistence_type='memory') for j in range(2)])]) for i in range(n)]) 
            

        @self.app.callback(Output(component_id="live_GP", component_property="figure"), 
                    Input('graph-update', 'n_intervals'))   
        def update_graphGP(n):
            [parmMin, parmMax]= config['Optimization']['range'][0]
            n_parm = config['Optimization']['n_parms']

            data_plot = self.data['Change_parm']['data_plot']
            time_inlet = self.data['Change_parm']['time_inlet']
            data_gp = self.data['plot_data_GP']['data_gp']
            time_inlet_gp = self.data['plot_data_GP']['time_inlet_gp']
    
            match n_parm:
                case 1:                   
                    if time_inlet is not None:
                        self.parameter1.append(data_plot[1])
                        self.GPy.append(data_plot[0])
                        data = go.Scatter(x=list(self.parameter1), y=list(self.GPy), name='cost_sample', mode="markers")
                        self.HistGP = [data]

                    if time_inlet_gp is not None:
                        gp_list = [i[0] for i in data_gp]
                        self.GP_data_plot = gp_list
                    if not(self.GP_data_plot == []): 
                        data_1 = go.Scatter(x=list(np.linspace(0,85,100)), y=self.GP_data_plot, name='GP', mode="lines")
                        self.HistGP = [data, data_1]
                    
                    layout = go.Layout(xaxis = dict(title='Parameter',range=[parmMin, parmMax]),
                                            yaxis=dict(title='Cost'))
                    return {'data':self.HistGP, 'layout':layout}
                
                case 2:
                    if len(time_inlet_gp):
                        gp_list = [i[0] for i in data_gp]
                        n = len(gp_list)
                        gp_size = int(math.sqrt(n))
                        self.GP_data_plot = [gp_list[i:i+gp_size] for i in range(0, n, gp_size)]

                    if time_inlet is not None:
                        if data_plot[0]:
                            self.parameter1.append(data_plot[1])
                            self.parameter2.append(data_plot[2])
                            self.GPy.append(data_plot[0])   

                    x_scale = 1.4
                    y_scale = 1.4  
                    z_scale = 0.5
                    layout=go.Layout(xaxis = dict(range=[parmMin, parmMax]),yaxis=dict(range=[parmMin, parmMax]),
                                    scene=dict(xaxis_title='Parameter 1', yaxis_title='Parameter 2',
                                    zaxis_title='Cost', aspectmode='manual', aspectratio=dict(x=x_scale,
                                    y=y_scale, z=z_scale)), width=700, margin=dict(r=10, b=40, l=10, t=0))                  
                                     
                    data=go.Scatter3d(x=list(self.parameter1), y=list(self.parameter2), z=list(self.GPy), 
                                    name='cost_samples', mode="markers")
                    self.HistGP = [data]

                    ###################################
                    if self.GP_data_plot is not None:
                        nx,ny = (30,30)
                        x = np.linspace(0,85, nx)
                        y= np.linspace(0,85, ny)
                        data_1 = go.Surface(x=x,y=y,z=self.GP_data_plot, name='GP',opacity=0.50) 
                        self.HistGP = [data, data_1]
                    
                    return {'data':self.HistGP, 'layout':layout} 
                

        # @app.callback(Output(component_id="live_Acq", component_property="figure"), 
        #               Input('graph-update', 'n_intervals'))   
        # def update_graphACQ(n):

        #     [parmMin, parmMax]= config['Optimization']['range'][0]
        #     [costMin, costMax]= config['Optimization']['range_cost']
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
                    

        @self.app.callback(Output(component_id="live_ECG", component_property="figure"), 
                    Input('graph-update', 'n_intervals'))   
        def update_graphECG(n):
            data_ecg = self.dataECG['polar ECG']['data_ecg']
            if data_ecg is not None:
                self.ECGy = np.array(data_ecg).flatten()
            data = go.Scatter(y=self.ECGy, name='ECG', mode="lines")
            return {'data':[data]}


        @self.app.callback(Output(component_id="live_parm", component_property="figure"), 
                    Input('graph-update', 'n_intervals'))   
        def update_graphPARM(n):
            n_parm = config['Optimization']['n_parms']
            time_inlet = self.data['Change_parm']['time_inlet']
            data_plot = self.data['Change_parm']['data_plot']
            if time_inlet is not None and not(time_inlet == self.previous_parm):
                self.previous_parm = time_inlet
                if n_parm>=1: 
                    self.parameter1.append(data_plot[1])
                    data1 = go.Scatter(y=self.parameter1, name='Parameter1', mode="lines")
                    self.HistParm = [data1]
                    if n_parm>=2:
                            self.parameter2.append(data_plot[2])
                            data2 = go.Scatter(y=self.parameter2, name='Parameter2', mode="lines")  
                            self.HistParm = [data1, data2]   
                            if n_parm>=3:
                                self.parameter3.append(data_plot[3])
                                data3 = go.Scatter(y=self.parameter3, name='Parameter3', mode="lines")  
                                self.HistParm = [data1, data2, data3] 
                                if n_parm>=4:
                                    self.parameter4.append(data_plot[4])
                                    data4 = go.Scatter(y=self.parameter4, name='Parameter4', mode="lines")  
                                    self.HistParm = [data1, data2, data3, data4]
                                    if n_parm>=5:
                                        self.parameter5.append(data_plot[5])
                                        data5 = go.Scatter(y=self.parameter5, name='Parameter5', mode="lines")  
                                        self.HistParm = [data1, data2, data3, data4, data5]
                                        if n_parm==6:
                                            self.parameter6.append(data_plot[6])
                                            data6 = go.Scatter(y=self.parameter6, name='Parameter6', mode="lines")  
                                            self.HistParm = [data1, data2, data3, data4, data5, data6]
                
            return {'data':self.HistParm}


        # @app.callback(
        #     Output('graph-update', 'disabled'),
        #     Input('resume_button', 'n_clicks'),
        #     Input('pause_button', 'n_clicks'))
        # def resume_opt(n_resume, n_pause, state):
        #     if (None == n_resume) and (None== n_pause):
        #         return True #state
        #     if "resume_button" == ctx.triggered_id:
        #         return True #False
        #     elif "pause_button" == ctx.triggered_id:
        #         return True
            
            
        @self.app.callback(
            Output('submit_button', 'children'),
            Input('submit_button', 'n_clicks'),
            State('parm_slider', 'value'),
            State('GP-dropdown', 'value'),
            State('Acq-dropdown', 'value'),
            State('parmBox','children'),
            State('inputCost-0', 'value'),
            State('inputCost-1', 'value'),prevent_initial_call=True)
        def submit(n_submit, n_parm, GP, Acq, parmRanges, costMin, costMax): 
            if "submit_button" == ctx.triggered_id:
                boxcouples = [[]for i in range(n_parm)]
                for i in range(n_parm):
                        boxcouples[i]=[parmRanges['props']['children'][i]['props']['children'][2]
                                    ['props']['children'][j]['props']['value'] for j in range(2)]
                    
                config['Optimization']['n_parms'] = n_parm
                config['Optimization']['GP'] = GP
                config['Optimization']['acquisition'] = Acq
                config['Optimization']['range'] = boxcouples
                config['Optimization']['range_cost'] = [costMin, costMax]

                config_list = [n_parm, GP, Acq, parmRanges, costMin, costMax]
                if not(None in config_list):
                    with open('ECG_config.yml', 'w') as file:
                        yaml.dump(config, file)
                    return 'SUBMITTED'
                else:
                    return 'SUBMIT'
                

        @self.app.callback(Output("hidden-div", 'children', allow_duplicate=True),
                           Input('clear_button', 'n_clicks'),
                           prevent_initial_call=True)
        def clear_UIstack(n):
            if n is not None and "clear_button" == ctx.triggered_id:
                self.reset()
        
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
                

        
