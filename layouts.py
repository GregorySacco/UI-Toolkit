from dash import html, dcc, ctx
import plotly.graph_objs as go

layout_main = html.Div([
            html.H1('RRL: Human in the Loop optimization',style={'margin-left': '5px'}),
            html.Div([
                dcc.Tabs(id='tabs-example', value='opt', children=[
                    dcc.Tab(label='Initialization', value='init'),
                    dcc.Tab(label='Optimization', value='opt'),
                    dcc.Tab(label='Signals', value='sig'),
                    dcc.Tab(label='Hyperparameters', value='hyp')
                ]),
                html.Div(id='tabs-content'),
            ]),
            dcc.Interval(id="graph-update", interval=2500, disabled=False), 
            dcc.Interval(id="server_timer", interval=500), 
            dcc.Interval(id="ECG_timer", interval=2000), 
            html.Div(id="hidden-div", children= None, style={"display":"none"}),
        ])


layout_init = html.Div([
                    html.Br(),
                    html.Div([
                        html.Br(),
                        html.H3('Select the feedback signal:',style={'margin-left': '5%'}), 
                        dcc.Dropdown(['ECG','Metabolic','COP'], 'ECG', id='sensor-dropdown',
                                            style={'margin-left': '3%', 'width': '80%'}, persistence=True),
                        html.Br(),
                        html.H3('Select type of Gaussian process:',style={'margin-left': '5%'}),
                        dcc.Dropdown(['Regular','RGPE'], 'Regular', id='GP-dropdown',
                                            style={'margin-left': '3%','width': '80%'}, persistence=True),
                        html.Br(),     
                        
                        html.H3('Select type of Acquisition function:',style={'margin-left': '5%'}),
                        dcc.Dropdown(['qei', 'b', 'c'], 'qei', id='Acq-dropdown',
                                            style={'margin-left': '3%','width': '80%'}, persistence=True),
            
                        html.Br(),
                        html.H3('Number of parameters:',style={'margin-left': '5%'}),   
                        html.Br(),
                        html.Div([
                            dcc.Slider(1,6,step=1,value=1,id='parm_slider',persistence=True), 
                        ], style = {'margin-left': '3%', 'width': '80%'}),
                        
                        html.Br(),
                        
                        html.Button(id='submit_button',className='btn btn-secondary',children='SUBMIT', 
                                style={'width': '200px', 'height':'100px', 'margin-left':'150px', 
                                    'margin-top':'5%','border-radius':'10px',}),
                        ],style={'width':'50%', 'display':'inline-block', 'vertical-align': 'top'}),        

                    
                    html.Div([      
                        html.Br(),  
                        html.Div(id='parmBox', style={'width': '400px', 'height':'100px', 'margin-left':'150px'}),    
                        ],style={'width':'50%', 'display':'inline-block',})                                 
                ], style={'width':'100%'})


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

                    # html.Div([
                    #     dcc.Dropdown(['1','2','3','4','5','6'], '1', id='GPx-dropdown',
                    #                         style={'margin-left': '2%', 'margin-top':'2%', 'width': '30%'}, persistence=True),
                    #     dcc.Dropdown(['1','2','3','4','5','6'], '1', id='GPy-dropdown',
                    #                         style={'margin-left': '2%', 'margin-top':'20px', 'width': '30%'}, persistence=True),
                    # ]),
                    html.Div([
                        html.H5("Select parameters for axis x and y", style={'margin-left':'2%', 'margin-top':'2%'}),
                        dcc.Input(id='x-input', type='number', placeholder='x-axis', persistence=True, persistence_type='memory',
                                  style={'width': '10%', 'margin-left':'2%', 'margin-top':'0%'}),
                        dcc.Input(id='y-input', type='number', placeholder='y-axis', persistence=True, persistence_type='memory',
                                  style={'width': '10%', 'margin-left':'2%', 'margin-top':'0%'}),
                    ]), 

                    html.Button(id='clear_button',className='btn btn-secondary',children='CLEAR', 
                                style={'width': '15%', 'height':'80px', 'margin-left':'48%', 'margin-top':'-4%','border-radius':'10px'}), 

                    html.Button(id='pause_button',className='btn btn-secondary',children='PAUSE', 
                                style={'width': '15%', 'height':'80px', 'margin-left':'32px', 'margin-top':'-4%','border-radius':'10px'}), 

                    html.Button(id='resume_button',className='btn btn-secondary',children='RESUME', 
                                style={'width': '15%','height':'80px', 'margin-left':'32px', 'margin-top':'-4%','border-radius':'10px'}),
                ],style={"width": "100 %"})

layout_sig=html.Div([
                html.Br(),
                html.Div([
                    html.Br(),
                    html.H3('Biofeedback signal'),
                    html.Br(),
                    dcc.Graph(id='live_ECG', figure={'layout': go.Layout(xaxis = dict(title='Time'),yaxis=dict(title='mV'),title='ECG')})
                ], style={'padding':20, 'flex':1}),
    
                html.Div([
                    html.Br(),
                    html.H3('Parameter/iterations'),
                    html.Br(),
                    dcc.Graph(id='live_parm', figure = {'layout': go.Layout(xaxis = dict(title='Iterations'),
                                                                            yaxis=dict(title='Parameter value'),title='Parameters')}),
                ], style={'padding':20, 'flex':1}), 
            ],style={'display':'flex', 'flex-direction':'row'})

layout_hyp = html.Div([
                html.Br(),
                html.Div([
                    html.Br(),
                    dcc.Graph(id='live_hyp1', style={"height": "37vh"}, figure={
                        'layout' : {'title': 'Likelihood noise covariance','margin': {'l': 40, 'r': 30, 't': 40, 'b': 30},}}),  
                    html.Br(),
                    dcc.Graph(id='live_hyp4', style={"height": "37vh"}, figure={
                        'layout' : {'title': 'Covariance module lengthscale','margin': {'l': 40, 'r': 30, 't': 40, 'b': 30},}}),  
                ], style={'padding':1, 'flex':1}),
    
                html.Div([
                    html.Br(),
                    dcc.Graph(id='live_hyp2', style={"height": "37vh"}, figure={
                        'layout' : {'title': 'Mean module','margin': {'l': 40, 'r': 30, 't': 40, 'b': 30},}}),
                    html.Br(),
                    dcc.Graph(id='live_hyp5', style={"height": "37vh"}, figure={
                        'layout' : {'title': 'Hyperparameter 5','margin': {'l': 40, 'r': 30, 't': 40, 'b': 30},}})
                ], style={'padding':1, 'flex':1}), 

                html.Div([
                    html.Br(),
                    dcc.Graph(id='live_hyp3', style={"height": "37vh"}, figure={
                        'layout' : {'title': 'Covariance module outputscale','margin': {'l': 40, 'r': 30, 't': 40, 'b': 30},}}),  
                    html.Br(),
                    dcc.Graph(id='live_hyp6', style={"height": "37vh"}, figure={
                        'layout' : {'title': 'Hyperparameter 6','margin': {'l': 40, 'r': 30, 't': 40, 'b': 30},}})
                ], style={'padding':1, 'flex':1}), 

            ],style={'display':'flex', 'flex-direction':'row', "width": "100 %"}),
