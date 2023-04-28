import random
import dash
from dash import html, dcc, ctx
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go
from collections import deque
import dash_bootstrap_components as dbc
import numpy as np
import yaml
#from pylsl import StreamInfo, StreamInlet, resolve_stream

#streams=resolve_stream('name','datagather')
#inlet=StreamInlet(streams[0])

from pylsl import StreamInfo, StreamInlet, resolve_stream
import time

streams=resolve_stream('name','Change_parm')
inlet=StreamInlet(streams[0])

streams=resolve_stream('name','plot_data_GP')
inlet_gp=StreamInlet(streams[0])

streams=resolve_stream('name','plot_data_acq')
inlet_acq=StreamInlet(streams[0])


minmax = {1: "min", 2:"max"}

with open('ECG_config.yml', 'r') as file:    
    config = yaml.safe_load(file)

class MyClass:
    def __init__(self):
        self.parameter1 = []  
        self.parameter2 = []  
        self.parameter3 = [0]  
        self.parameter4 = [0]  
        self.parameter5 = [0]  
        self.parameter6 = [0]  
        self.GPy = []
        self.Acq_data_plot = None
        self.GP_data_plot = None
        
values = MyClass()

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SLATE],
                meta_tags=[{'name':'viewport',
                            'content':'width=device-width, initial-scale=0.7, maximum-scale=3, minimum-scale=0.5'}])

app.layout = html.Div([
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


@app.callback(Output('tabs-content', 'children'),
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
                    html.H3('Cost/iterations'),
                    html.Br(),
                    dcc.Graph(id='live_cost', animate=True),
                ], style={'padding':20, 'flex':1}),
    
                html.Div([
                    html.Br(),
                    html.H3('Parameter/iterations'),
                    html.Br(),
                    dcc.Graph(id='live_parm', animate=True),
                ], style={'padding':20, 'flex':1}), 
            ],style={'display':'flex', 'flex-direction':'row'})


@app.callback(Output('parmBox','children'),
              Input('parm_slider','value'),)
def update_parmBox(n):
    return html.Div(
            [html.Div([
                html.Br(),
                html.H5(f'Parameter {i+1}'),
                html.Div([dcc.Input(id=f'input{i}{j}', type='number', placeholder=minmax[j+1],
                                    persistence=True, persistence_type='memory') for j in range(2)])]) for i in range(n)]) 
     

@app.callback(Output(component_id="live_GP", component_property="figure"), 
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
        values.GP_data_plot = gp_list
    
    match n_parm:
        case 1:
            if time_inlet is not None:
                values.parameter1.append(data_plot[0])
                values.GPy.append(data_plot[1])
     
            layout = go.Layout(xaxis = dict(title='Parameter',range=[parmMin, parmMax]),
                yaxis=dict(title='Cost'),title='Gaussian Process')
            data = go.Scatter(x=list(values.parameter1), y=list(values.GPy), name='cost_samples', mode="markers")
            if values.GP_data_plot is not None:
                data_1 = go.Scatter(x=list(np.linspace(0,85, 100)), y=values.GP_data_plot, name='GP', mode="lines")
            return {'data':[data, data_1], 'layout':layout}
        
        case 2:
            if time_inlet is not None:
                if data_plot[0]:
                    values.parameter1.append(data_plot[1])
                    values.parameter2.append(data_plot[2])
                    values.GPy.append(data_plot[0])             
                
            layout = go.Layout(scene = dict(xaxis_title='Parameter 1',yaxis_title='Parameter 2',
                                zaxis_title='Cost'), width=600, margin=dict(r=10, b=10, l=10, t=10))
            data=go.Scatter3d(x=list(values.parameter1), y=list(values.parameter2), z=list(values.GPy), name='cost_samples', mode="markers", )
            if values.GP_data_plot is not None:
                nx,ny = (30,30)
                x = np.linspace(0,85, nx)
                y= np.linspace(0,85, ny)
                xv, yv = np.meshgrid(x,y)
                data_1 = go.Mesh3d(x=xv.flatten(), y=yv.flatten(), z=list(values.GP_data_plot), name='GP',opacity=0.50)
                 
                return {'data':[data, data_1], 'layout':layout} 
            return {'data':[data], 'layout':layout} 
        

@app.callback(Output(component_id="live_Acq", component_property="figure"), 
              Input('graph-update', 'n_intervals'))   
def update_graph(n):

    [parmMin, parmMax]= config['Optimization']['range'][0]
    [costMin, costMax]= config['Optimization']['range_cost']
    n_parm = config['Optimization']['n_parms']

    data_plot, time_inlet = inlet.pull_sample(timeout=0.2)
    data_acq, time_inlet_acq = inlet_acq.pull_chunk(timeout=0.2)
    if len(time_inlet_acq):
        acq_list = [i[0] for i in data_acq]
        values.Acq_data_plot = acq_list
    match n_parm:
        # case 1:
        #     if disable == False:
        #         values.parameter1.append(random.randint(parmMin, parmMax))
        #         values.Acqy.append(random.randint(costMin, costMax))
        #     layout = go.Layout(xaxis = dict(title='Parameter',range=[parmMin, parmMax]),
        #         yaxis=dict(title='Cost',range=[min(values.Acqy), max(values.Acqy)]))  #,title='Gaussian Process')
        #     data = go.Scatter(x=list(values.parameter1), y=list(values.Acqy), name='gp', mode="lines+markers")
        #     return {'data':[data], 'layout':layout}
        
        case 2:
            if time_inlet is not None:
                if data_plot[0]:
                    values.parameter1.append(data_plot[1])
                    values.parameter2.append(data_plot[2])

            layout = go.Layout(scene = dict(xaxis_title='Parameter 1', yaxis_title='Parameter 2',
                            zaxis_title='Cost'), width=600, margin=dict(r=10, b=10, l=10, t=10))
            if values.Acq_data_plot is not None:
                nx,ny = (30,30)
                x = np.linspace(0,85, nx)
                y= np.linspace(0,85, ny)
                xv, yv = np.meshgrid(x,y)
                data = go.Mesh3d(x=xv.flatten(), y=yv.flatten(), z=list(values.Acq_data_plot), name='Acq',opacity=0.50)
                return {'data':[data], 'layout':layout} 
            



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
    
    
@app.callback(
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
        

if __name__ == '__main__':
    app.run_server(debug=True, port = 8080) # host='0.0.0.0')