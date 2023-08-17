from dash import html, dcc, ctx
import plotly.graph_objs as go
import dash_bootstrap_components as dbc


layout_main = html.Div([
            html.Div([
                html.Div([
                    html.H1('RRL: Human in the Loop optimization',style={'margin-left': '5px'}),
                ]),
    
                html.Div([
                    dbc.Badge(children="Server", id= "server_flag", color="secondary", className="me-1",),
                ], style={'width':'5%', 'margin-left':'10%', 'margin-top':'1%'}), 

                html.Div([
                    dbc.Badge(children="Optimization", id="opt_flag", color="secondary", className="me-1", ),
                ], style={'width':'5%', 'margin-left':'1%', 'margin-top':'1%'}), 
            ],style={'display':'flex', 'flex-direction':'row', "width": "100 %"}),

            html.Div([
                dcc.Tabs(id='tabs-example', value='init', children=[
                    dcc.Tab(label='Initialization', value='init'),
                    dcc.Tab(label='Optimization', value='opt'),
                    dcc.Tab(label='Signals', value='sig'),
                    dcc.Tab(label='Hyperparameters', value='hyp')
                ]),
                html.Div(id='tabs-content'),
            ]),
            dcc.Interval(id="graph-updateOPT", interval=3000),
            dcc.Interval(id="graph-updateHyp123", interval=2500),
            dcc.Interval(id="graph-updateHyp456", interval=2500),
            dcc.Interval(id="graph-updateSig", interval=1000),
            dcc.Interval(id="server_timer", interval=500), 
            html.Div(id="hidden-div", children= None, style={"display":"none"}),
        ])


layout_init = html.Div([
                html.Div([
                    html.Br(),
                    html.Br(),
                    #html.H4('Select the feedback signal:'), 
                    #dcc.Dropdown(['ECG','Metabolic','COP'], 'ECG', id='sensor-dropdown',
                    #                         style={'width': '80%'}, persistence=True),
                    #html.Br(),
                    html.H4('Number of parameters:'),   
                    html.Br(),
                    html.Div([ 
                    dcc.Slider(1,6,step=1,value=1,id='parm_slider',persistence=True), 
                    ], style = {'width': '80%'}), 
                    html.Br(),
                    html.Br(),
                    html.H4('Insert number of steps for optimization'),
                    dcc.Input(id='opt_steps', type='number', placeholder = 'n_steps',
                              style={'width': '40%', 'height': '25px'}, persistence=True, persistence_type='memory'),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.H4('Insert time for each step'),
                    dcc.Input(id='opt_time', type='number', placeholder = 'seconds',
                              style={'width': '40%', 'height': '25px'}, persistence=True, persistence_type='memory') 
                ], style={'padding':1, 'flex':1,'margin-left': '3%'}),
    
                html.Div([
                    html.Br(), 
                    html.Div(id='parmBox', style={'width': '92%', 'height':'20%', 'margin-left':'5%'})
                ], style={'padding':1, 'flex':1}), 

                html.Div([
                    html.Br(),
                    html.Br(),
                    html.H4('Select type of Gaussian process:',),
                    dcc.Dropdown(['Regular','RGPE'], 'Regular', id='GP-dropdown', style={'width': '80%'}, persistence=True),
                    html.Br(),
                    html.H4('Select type of Acquisition function:',),
                    dcc.Dropdown(['ei', 'pi'], 'ei', id='Acq-dropdown',
                                style={'width': '80%'}, persistence=True),
                    html.Br(),
                    html.Div([
                        html.Button(id='submit_button',className='btn btn-secondary',children='SUBMIT', 
                            style={'width': '40%', 'height':'100px', 'margin-left':'20%','margin-top':'5%','border-radius':'10px',}),
                    ])
                
                ], style={'padding':1, 'flex':1, 'margin-left': '1%'}), 
            ],style={'display':'flex', 'flex-direction':'row', "width": "100 %"}),


layout_opt=html.Div([
                    html.Div([
                        html.Br(),
                        html.Div([
                            html.H3('Gaussian Process'),
                            dcc.Graph(id='live_GP'),    
                        ], style={'padding':10, 'flex':1}),
            
                        html.Div([
                            html.H3('Acquisition function'),
                            dcc.Graph(id='live_Acq'),
                        ], style={'padding':10, 'flex':1}), 

                    ],style={'display':'flex', 'flex-direction':'row'}),

                    html.Button(id='clear_button',className='btn btn-secondary',children='CLEAR', 
                                style={'width': '15%', 'height':'80px', 'margin-left':'24.5%', 'margin-top':'2%','border-radius':'10px'}), 

                    html.Button(id='pause_button',className='btn btn-secondary',children='PAUSE', 
                                style={'width': '15%', 'height':'80px', 'margin-left':'3%', 'margin-top':'2%','border-radius':'10px'}), 

                    html.Button(id='resume_button',className='btn btn-secondary',children='RESUME', 
                                style={'width': '15%','height':'80px', 'margin-left':'3%', 'margin-top':'2%','border-radius':'10px'}),
                ],style={"width": "100 %"})


layout_sig=html.Div([
                html.Br(),
                html.Div([
                    html.H4('Biofeedback signal'),
                    dcc.Graph(id='live_ECG', style={"height": "37vh"}, figure={'layout': 
                                    go.Layout(xaxis = dict(title='Time'),yaxis=dict(title='mV'),title='ECG')}),  
                    dcc.Graph(id='live_HRV', style={"height": "37vh"}, figure={'layout': 
                                    go.Layout(xaxis = dict(title='Time'),yaxis=dict(title='mV'),title='RMSSD')}),  
                ], style={'padding':1, 'flex':1}),
    
                html.Div([
                    html.H4('Parameters and Cost'),
                    dcc.Graph(id='live_parm', style={"height": "37vh"}, figure={'layout': 
                                    go.Layout(xaxis = dict(title='Iteration'),title='Parameters')}),
                    dcc.Graph(id='live_cost', style={"height": "37vh"}, figure={'layout': 
                                    go.Layout(xaxis = dict(title='Iteration'),yaxis=dict(title=''),title='Cost')})
                ], style={'padding':1, 'flex':1}), 

            ],style={'display':'flex', 'flex-direction':'row', "width": "100 %"}),


layout_hyp = html.Div([
                html.Br(),
                html.Div([
                    html.Br(),
                    dcc.Graph(id='live_hyp1', style={"height": "37vh"}, figure={
                        'layout' : {'title': 'Hyperparameter 1','margin': {'l': 40, 'r': 30, 't': 40, 'b': 30},}}),  
                    html.Br(),
                    dcc.Graph(id='live_hyp4', style={"height": "37vh"}, figure={
                        'layout' : {'title': 'Hyperparameter 4','margin': {'l': 40, 'r': 30, 't': 40, 'b': 30},}}),  
                ], style={'padding':1, 'flex':1}),
    
                html.Div([
                    html.Br(),
                    dcc.Graph(id='live_hyp2', style={"height": "37vh"}, figure={
                        'layout' : {'title': 'Hyperparameter 2','margin': {'l': 40, 'r': 30, 't': 40, 'b': 30},}}),
                    html.Br(),
                    dcc.Graph(id='live_hyp5', style={"height": "37vh"}, figure={
                        'layout' : {'title': 'Hyperparameter 5','margin': {'l': 40, 'r': 30, 't': 40, 'b': 30},}})
                ], style={'padding':1, 'flex':1}), 

                html.Div([
                    html.Br(),
                    dcc.Graph(id='live_hyp3', style={"height": "37vh"}, figure={
                        'layout' : {'title': 'Hyperparameter 3','margin': {'l': 40, 'r': 30, 't': 40, 'b': 30},}}),  
                    html.Br(),
                    dcc.Graph(id='live_hyp6', style={"height": "37vh"}, figure={
                        'layout' : {'title': 'Hyperparameter 6','margin': {'l': 40, 'r': 30, 't': 40, 'b': 30},}})
                ], style={'padding':1, 'flex':1}), 

            ],style={'display':'flex', 'flex-direction':'row', "width": "100 %"})
            
            
            
            
            
