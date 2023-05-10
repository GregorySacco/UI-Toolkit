import dash
from dash import html, dcc, ctx
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go
from collections import deque
import dash_bootstrap_components as dbc
import numpy as np
import yaml
import math

from pylsl import StreamInfo, StreamInlet, resolve_stream


class UI:
    def __init__(self):
        
        streams=resolve_stream('name','Change_parm')
        inlet=StreamInlet(streams[0])
        
        streams=resolve_stream('name','plot_data_GP')
        inlet_gp=StreamInlet(streams[0])
        
        # streams=resolve_stream('name','plot_data_acq')
        # inlet_acq=StreamInlet(streams[0])

        streams=resolve_stream('name','polar ECG')
        inlet_ecg=StreamInlet(streams[0])
        
        
        self.parameter1 = []  
        self.parameter2 = []  
        self.parameter3 = []  
        self.parameter4 = []  
        self.parameter5 = []  
        self.parameter6 = [] 
        self.GPy = []
        self.Acq_data_plot = None
        self.GP_data_plot = []
        self.ECGy =[]
        self.HistParm=[]
        self.HistGP = []

        minmax = {1: "min", 2:"max"}
        with open('ECG_config.yml', 'r') as file: config = yaml.safe_load(file)

        self.app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[{'href': '/assets/bootstrap.min.css'}],
                meta_tags=[{'name':'viewport',
                            'content':'width=device-width, initial-scale=0.7, maximum-scale=3, minimum-scale=0.5'}])
        self.app.layout = html.Div([
            html.H1('RRL: Human in the Loop optimization',style={'margin-left': '5px'}),
            html.Br(),
            html.Div([
                dcc.Tabs(id='tabs-example', value='init', children=[
                    dcc.Tab(label='Initialization', value='init'),
                    dcc.Tab(label='Optimization', value='opt'),
                    dcc.Tab(label='Others', value='oth')
                ]),
                html.Div(id='tabs-content'),
            ]),
            dcc.Interval(id="graph-update", interval=2500, disabled=False), 
        ])


        @self.app.callback(Output('tabs-content', 'children'),
              Input('tabs-example', 'value'))
        def render_content(tab):
            if tab == 'init':
                return html.Div([
                    html.Br(),
                    html.Div([
                        html.Br(),
                        html.H3('Select the sensor:',style={'margin-left': '5px'}), 
                        dcc.Dropdown(['ECG','Metabolic','COP'], 'ECG', id='sensor-dropdown',
                                            style={'margin-left': '10px', 'margin-right': '30px'}, persistence=True),
                        html.Br(),
                        html.Br(),
                        html.H3('Number of parameters:',style={'margin-left': '5px'}),   
                        html.Br(),
                        dcc.Slider(1,6,step=1,value=1,id='parm_slider',persistence=True),
                    ],style={'width':'32%', 'display':'inline-block', 'vertical-align': 'top'}),

                    html.Div(id='parmBox',
                            style={'width':'420px', 'display':'inline-block', 'vertical-align': 'top','margin-left':'50px', 'margin-right':'40px'}),  

                    html.Div([      
                        html.Br(),  
                        html.Div([
                                html.Div([
                                    html.H3('Select the type of Gaussian process:'),
                                    dcc.Dropdown(['Regular','RGPE'], 'Regular', id='GP-dropdown',
                                            style={'margin-left': '0px', 'margin-right': '0px', 'width': '200px'}, persistence=True)
                                    ], style={'margin-left': '0px'}),
                                html.Br(),     
                                html.Div([
                                    html.H3('Select the type of Acquisition function:'),
                                    dcc.Dropdown(['qei', 'b', 'c'], 'qei', id='Acq-dropdown',
                                            style={'margin-left': '0px', 'margin-right': '0px', 'width': '200px'}, persistence=True)
                                    ], style={'margin-left': '0px'}),
                                html.Br(),
                                html.H3('Cost', style={'margin-left': '0px'}),
                                html.Div([dcc.Input(id=f'inputCost-{j}',placeholder=minmax[j+1],type='number',
                                    style={'margin-left': '0px'}, persistence=True, persistence_type='memory') for j in range(2)]),

                                html.Button(id='submit_button',className='btn btn-secondary',children='SUBMIT', 
                                    style={'width': '200px', 'height':'100px', 'margin-left':'150px', 
                                        'margin-top':'100px','border-radius':'10px',}),    
                                ])          
                    ],style={'width':'32%', 'display':'inline-block',})                        
                ], style={'margin':'40px'})
            
            elif tab == 'opt':
                return html.Div([
                    html.Div([
                        html.Br(),
                        html.Div([
                            html.Br(),
                            html.H3('Gaussian Process'),
                            html.Br(),
                            dcc.Graph(id='live_GP'),  #, animate=True
                            dcc.Store(id='dataGP')   
                        ], style={'padding':20, 'flex':1}),
            
                        html.Div([
                            html.Br(),
                            html.H3('Acquisition function'),
                            html.Br(),
                            dcc.Graph(id='live_Acq'),
                        ], style={'padding':20, 'flex':1}), 

                    ],style={'display':'flex', 'flex-direction':'row'}),
                    html.Button(id='pause_button',className='btn btn-secondary',children='PAUSE',  #440 and 32
                                style={'width': '300px', 'height':'100px', 'margin-left':'597px', 'margin-top':'20px','border-radius':'10px'}),

                    

                    html.Button(id='resume_button',className='btn btn-secondary',children='RESUME', 
                                style={'width': '300px','height':'100px', 'margin-left':'32px', 'margin-top':'20px','border-radius':'10px'}),
                ])
                    
            
            elif tab == 'oth':
                return html.Div([
                        html.Br(),
                        html.Div([
                            html.Br(),
                            html.H3('Biofeedback signal'),
                            html.Br(),
                            dcc.Graph(id='live_ECG')
                        ], style={'padding':20, 'flex':1}),
            
                        html.Div([
                            html.Br(),
                            html.H3('Parameter/iterations'),
                            html.Br(),
                            dcc.Graph(id='live_parm'),
                        ], style={'padding':20, 'flex':1}), 
                    ],style={'display':'flex', 'flex-direction':'row'})


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
        def update_graph(n):
            [parmMin, parmMax]= config['Optimization']['range'][0]
            [costMin, costMax]= config['Optimization']['range_cost']
            n_parm = config['Optimization']['n_parms']

            data_plot, time_inlet = inlet.pull_sample(timeout=0.2)
            # print(data_plot, time_inlet)

            data_gp, time_inlet_gp = inlet_gp.pull_chunk(timeout=0.2)
            if len(time_inlet_gp):
                gp_list = [i[0] for i in data_gp]
                n = len(gp_list)
                gp_size = int(math.sqrt(n))
                self.GP_data_plot = [gp_list[i:i+gp_size] for i in range(0, n, gp_size)]
            
            match n_parm:
                case 1:
                    if time_inlet is not None:
                        self.parameter1.append(data_plot[1])
                        self.GPy.append(data_plot[0])
                    layout = go.Layout(xaxis = dict(title='Parameter',range=[parmMin, parmMax]),
                                            yaxis=dict(title='Cost'),title='Gaussian Process')
                    data = go.Scatter(x=list(self.parameter1), y=list(self.GPy), name='cost_sample', mode="markers")
                    if self.GP_data_plot is not None:
                        data_1 = go.Scatter(x=list(np.linspace(0,85, 100)), y=self.GP_data_plot, name='GP', mode="lines")
                    self.HistGP = [data, data_1]
                    return {'data':self.HistGP, 'layout':layout}
                
                case 2:
                    if time_inlet is not None:
                        if data_plot[0]:
                            self.parameter1.append(data_plot[1])
                            self.parameter2.append(data_plot[2])
                            self.GPy.append(data_plot[0])   

                    x_scale = 1.4
                    y_scale = 1.4  
                    z_scale = 0.5
                    layout=go.Layout(scene=dict(xaxis_title='Parameter 1', yaxis_title='Parameter 2',
                                zaxis_title='Cost', aspectmode='manual', aspectratio=dict(x=x_scale,
                                y=y_scale, z=z_scale)), width=800, margin=dict(r=10, b=40, l=10, t=0))                  
                                     
                    data=go.Scatter3d(x=list(self.parameter1), y=list(self.parameter2), z=list(self.GPy), 
                                    name='cost_samples', mode="markers")
                    self.HistGP= [data]

                    ###################################
                    if self.GP_data_plot is not None:
                        nx,ny = (30,30)
                        x = np.linspace(0,85, nx)
                        y= np.linspace(0,85, ny)
                        # xv, yv = np.meshgrid(x,y)
                        # data_1 = go.Mesh3d(x=xv.flatten(), y=yv.flatten(), z=list(self.GP_data_plot), name='GP',opacity=0.50) 
                        data_1 = go.Surface(x=x,y=y,z=self.GP_data_plot, name='GP',opacity=0.50) 
                        self.HistGP = [data, data_1]
                    
                    return {'data':self.HistGP, 'layout':layout} 
                

        # @app.callback(Output(component_id="live_Acq", component_property="figure"), 
        #               Input('graph-update', 'n_intervals'))   
        # def update_graph(n):

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
        def update_graph(n):
            
            data_plot, time_inlet = inlet_ecg.pull_chunk(timeout=0.2)
            if data_plot is not None:
                self.ECGy = np.array(data_plot).flatten()
            
            layout = go.Layout(xaxis = dict(title='Time'),yaxis=dict(title='mV'),title='ECG')
            data = go.Scatter(y=self.ECGy, name='ECG', mode="lines")
            return {'data':[data], 'layout':layout}

        @self.app.callback(Output(component_id="live_parm", component_property="figure"), 
                    Input('graph-update', 'n_intervals'))   
        def update_graph(n):
            n_parm = config['Optimization']['n_parms']
            data_plot, time_inlet = inlet.pull_sample(timeout=0.2)
            layout = go.Layout(xaxis = dict(title='Iterations'),yaxis=dict(title='Parameter value'),title='Parameters')
            if time_inlet is not None:
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
                                        if n_parm>=6:
                                            self.parameter6.append(data_plot[6])
                                            data6 = go.Scatter(y=self.parameter6, name='Parameter6', mode="lines")  
                                            self.HistParm = [data1, data2, data3, data4, data5, data6]
                
            return {'data':self.HistParm, 'layout':layout}


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
                

        
