import random
import dash
from dash import html, dcc, ctx
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go
from collections import deque
import dash_bootstrap_components as dbc
import numpy as np
import yaml
# from pylsl import StreamInfo, StreamInlet, resolve_stream

# streams=resolve_stream('name','datagather')
# inlet=StreamInlet(streams[0])

X = deque(maxlen=20)
X2 = deque(maxlen=20)
Y = deque(maxlen=20)
X.append(0)
X2.append(0)
Y.append(0)

minmax = {1: "min", 2:"max"}

with open('ECG_config.yml', 'r') as file:    
    config = yaml.safe_load(file)


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
    dcc.Interval(id="graph-update", interval=500, disabled=True), 
])


@app.callback(Output('tabs-content', 'children'),
              Input('tabs-example', 'value'),
              State('graph-update','disabled'))
def render_content(tab,disabled):
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
                    dcc.Graph(id='live_Acq', animate=True),
                ], style={'padding':20, 'flex':1}), 

            ],style={'display':'flex', 'flex-direction':'row'}),
            html.Button(id='stop_button',className='btn btn-secondary',children='STOP',  #440 and 32
                        style={'width': '300px', 'height':'100px', 'margin-left':'597px', 'margin-top':'20px','border-radius':'10px'}),

            

            html.Button(id='start_button',className='btn btn-secondary',children='START', 
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
              Input('graph-update', 'n_intervals'), 
              State('graph-update', 'disabled'),
              State('dataGP', 'value'))   
def update_graph(n, disable, store):
    global X
    global X2
    global Y
    [parmMin, parmMax]= config['Optimization']['range'][0]
    [costMin, costMax]= config['Optimization']['range_cost']
    n_parm = config['Optimization']['n_parms']
        
    match n_parm:
        case 1:
            if disable == False:
                X.append(random.randint(parmMin, parmMax))
                Y.append(random.randint(costMin, costMax))
            layout = go.Layout(xaxis = dict(title='Parameter',range=[parmMin, parmMax]),
                yaxis=dict(title='Cost',range=[min(Y), max(Y)]),title='Gaussian Process')
            data = go.Scatter(x=list(X), y=list(Y), name='gp', mode="lines+markers")
            return {'data':[data], 'layout':layout}
        
        case 2:
            # X.append(X[-1]+1)
            if disable == False:
                X.append(random.randint(parmMin, parmMax))
                X2.append(random.randint(parmMin, parmMax))
                Y.append(Y[-1]+(10*random.uniform(-0.1,0.1)))
            data=go.Mesh3d(x=list(X), y=list(X2), z=list(Y), opacity=0.50)
            return {'data':[data]}
    # data = go.Scatter(x=list(X), y=list(Y), name='gp', mode="lines+markers")
    # return {'data':[data]}      
        

    # layout = go.Layout(xaxis = dict(title='Parameter',range=[parmMin, parmMax]),
    #                     yaxis=dict(title='Cost',range=[min(Y), max(Y)]),title='Gaussian Process')
    # data = go.Scatter(x=list(X), y=list(Y), name='gp', mode="lines+markers")
    # 
    #return {'data':[data]}   


@app.callback(
    Output('graph-update', 'disabled'),
    Input('start_button', 'n_clicks'),
    Input('stop_button', 'n_clicks'),
    State('graph-update', 'disabled'))
def start_opt(n_start, n_stop, state):
    if (None == n_start) and (None== n_stop):
        return state
    if "start_button" == ctx.triggered_id:
        return False
    elif "stop_button" == ctx.triggered_id:
        return True
    
    
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
    app.run_server(debug=True, port = 8080)   #, host='0.0.0.0'