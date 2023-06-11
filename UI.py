import dash
from dash import html, dcc, ctx
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go
import numpy as np
import yaml
import requests
from layouts import * 
from callbacks import *
import subprocess


class UI:
    def __init__(self):
        reset(self)
        with open('ECG_config.yml', 'r') as file: config = yaml.safe_load(file)
        self.serverIP = '127.0.0.1'
        self.serverPort = '5000'
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
                download_data(self,config)
           
    
        @self.app.callback(Output('parmBox','children'),
                    Input('parm_slider','value'),)
        def update_parmBox(n):
            minmax = {1: "min", 2:"max"}
            return html.Div(
                    [html.Div([
                        html.Br(),
                        html.H5(f'Parameter {i+1}'),
                        html.Div([dcc.Input(id=f'input{i}{j}', type='number', placeholder=minmax[j+1], style={'width': '40%', 'height': '10%'},
                                            persistence=True, persistence_type='memory') for j in range(2)])]) for i in range(n)]) 
            
        
        @self.app.callback(Output(component_id="live_GP", component_property="figure"), 
                    Input('graph-updateOPT', 'n_intervals'))   
        def update_graphGP(n):
            figure_update = updateLiveGP(self, config)
            return figure_update
                

        @self.app.callback(Output(component_id="live_Acq", component_property="figure"), 
                      Input('graph-updateOPT', 'n_intervals'))   
        def update_graphACQ(n):
            updateAcq = updateAcqGraph(self, config)
            return updateAcq

    
        @self.app.callback(Output(component_id="live_ECG", component_property="figure"), 
                    Input('graph-update2', 'n_intervals'))   
        def update_graphECG(n):
            figure_update = updateECG(self)
            return figure_update
        
        @self.app.callback(Output(component_id="live_HRV", component_property="figure"), 
                    Input('graph-update2', 'n_intervals'))   
        def update_graphHRV(n):
            figure_update = updateHRV(self)
            return figure_update
            


        @self.app.callback(Output(component_id="live_parm", component_property="figure"), 
                    Input('graph-update2', 'n_intervals'))   
        def update_graphPARM(n):
            n_parm = config['Optimization']['n_parms']
            update_figureParmIter = updateParmIterationGraph(self, n_parm)
            return update_figureParmIter
        
        @self.app.callback(Output(component_id="live_hyp1", component_property="figure"), 
                    Input('graph-update', 'n_intervals'))   
        def update_graphHYP1(n):
            update_hyp = updateHyperParm(self, hyp.order[1])
            layout = {'title': 'Likelihood noise covariance','margin': {'l': 40, 'r': 30, 't': 40, 'b': 30}}
            update_hyp['layout'] = layout
            return update_hyp
                
        @self.app.callback(Output(component_id="live_hyp2", component_property="figure"), 
                    Input('graph-update', 'n_intervals'))   
        def update_graphHYP2(n):
            update_hyp = updateHyperParm(self, hyp.order[2])
            layout = {'title': 'Mean module','margin': {'l': 40, 'r': 30, 't': 40, 'b': 30}}
            update_hyp['layout'] = layout
            return update_hyp
        
        @self.app.callback(Output(component_id="live_hyp3", component_property="figure"), 
                    Input('graph-update', 'n_intervals'))   
        def update_graphHYP3(n):
            update_hyp = updateHyperParm(self, hyp.order[3])
            layout = {'title': 'Covariance module outputscale','margin': {'l': 40, 'r': 30, 't': 40, 'b': 30}}
            update_hyp['layout'] = layout
            return update_hyp
        
        @self.app.callback(Output(component_id="live_hyp4", component_property="figure"), 
                    Input('graph-update', 'n_intervals'))   
        def update_graphHYP4(n):
            update_hyp = updateHyperParm(self, hyp.order[4])
            layout = {'title': 'Covariance module lengthscale','margin': {'l': 40, 'r': 30, 't': 40, 'b': 30}}
            update_hyp['layout'] = layout
            return update_hyp
        
        @self.app.callback(Output(component_id="live_hyp5", component_property="figure"), 
                    Input('graph-update', 'n_intervals'))   
        def update_graphHYP5(n):
            update_hyp = updateHyperParm(self, hyp.order[5])
            layout = {'title': hyp.order[5],'margin': {'l': 40, 'r': 30, 't': 40, 'b': 30}}
            update_hyp['layout'] = layout
            return update_hyp
        
        @self.app.callback(Output(component_id="live_hyp6", component_property="figure"), 
                    Input('graph-update', 'n_intervals'))   
        def update_graphHYP6(n):
            update_hyp = updateHyperParm(self, hyp.order[6])
            layout = {'title': hyp.order[6],'margin': {'l': 40, 'r': 30, 't': 40, 'b': 30}}
            update_hyp['layout'] = layout
            return update_hyp
        
        @self.app.callback(Output(component_id="live_cost", component_property="figure"), 
                    Input('graph-update2', 'n_intervals'))  
        def updateLiveCost(n):   
            data = go.Scatter(y=self.GPy, mode="lines")
            layout = go.Layout(xaxis = dict(title='Iteration'),yaxis=dict(title=''),title='Cost')
            return {'data': [data], 'layout': layout}

        @self.app.callback(Output(component_id="server_flag", component_property="color"),
                            Input('graph-update2', 'n_intervals'))
        def updateServerBadge(n):
            if self.flags['server'] == 'ON':
                server_color = 'success'
            elif self.flags['server'] ==  'OFF':
                server_color = 'danger'
            else:
                server_color == 'secondary'
            return server_color

        @self.app.callback(Output(component_id="opt_flag", component_property="color"),
                           Input('graph-update2', 'n_intervals'))
        def updateOptBadge(n):
            if self.flags['optimization'] == 'DONE':
                opt_color = 'success'
            elif self.flags['optimization'] == 'OFF':
                opt_color = 'danger'
            elif self.flags['optimization'] == 'EXPLORATION':
                opt_color = 'warning'
            elif self.flags['optimization'] == 'OPTIMIZATION':
                opt_color = 'info'
            else:
                opt_color = 'secondary'
            return opt_color
        

        @self.app.callback(
            Output('graph-update', 'disabled'),
            Input('resume_button', 'n_clicks'),
            Input('pause_button', 'n_clicks'))
        def resume_opt(n_resume, n_pause):
            if (None == n_resume) and (None== n_pause):
                return True #state
            if "resume_button" == ctx.triggered_id:
                msg = {"opt_comand": 'RESUME'}
                requests.post(f'http://{self.serverIP}:{self.serverPort}/OptState', json=msg)
                return False
            elif "pause_button" == ctx.triggered_id:
                msg = {"opt_comand": 'PAUSE'}
                requests.post(f'http://{self.serverIP}:{self.serverPort}/OptState', json=msg)
                return True
            
            
        @self.app.callback(
            Output('submit_button', 'children'),
            Input('submit_button', 'n_clicks'),
            State('parm_slider', 'value'),
            State('GP-dropdown', 'value'),
            State('Acq-dropdown', 'value'),
            State('parmBox','children'),
            State('opt_time', 'value'),prevent_initial_call=True)
        def submit(n_submit, n_parm, GP, Acq, parmRanges, opt_time): 
            if "submit_button" == ctx.triggered_id:
                boxcouples = [[]for i in range(n_parm)]
                for i in range(n_parm):
                    boxcouples[i]=[parmRanges['props']['children'][i]['props']['children'][2]
                                ['props']['children'][j]['props']['value'] for j in range(2)]
                    
                config['Optimization']['n_parms'] = n_parm
                config['Optimization']['GP'] = GP
                config['Optimization']['acquisition'] = Acq
                if n_parm == 1:
                    config['Optimization']['range'] = boxcouples[0]
                else: 
                    config['Optimization']['range'] = boxcouples
                
                config['Cost']['avg_time'] = opt_time

                config_list = [n_parm, GP, Acq, parmRanges, opt_time]
                if not(None in config_list):
                    with open('ECG_config.yml', 'w') as file:
                        yaml.dump(config, file)
                    return 'SUBMITTED'
                else:
                    return 'SUBMIT'
                

        @self.app.callback(Output("hidden-div", 'children', allow_duplicate=True),
                           Input('clear_button', 'n_clicks'),
                           prevent_initial_call=True)
        def clear_server(n):
            if n is not None and "clear_button" == ctx.triggered_id:
                reset(self) 
                requests.post(f'http://{self.serverIP}:{self.serverPort}/OptimizationData')
        
    
                