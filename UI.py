import dash
from dash import html, dcc, ctx
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go
import numpy as np
import yaml
import requests
from layouts import * 
from callbacks import *


class UI:
    def __init__(self):
        reset(self)
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
                download_data(self,config)
           
        
        @self.app.callback(Output("hidden-div", 'children', allow_duplicate=True),
                    Input('ECG_timer', 'n_intervals'),
                    prevent_initial_call=True)
        def download_ECG(n):
            if n is not None:
                self.dataECG = requests.get('http://127.0.0.1:5000/polarECG').json()


        @self.app.callback(Output('parmBox','children'),
                    Input('parm_slider','value'),)
        def update_parmBox(n):
            minmax = {1: "min", 2:"max"}
            return html.Div(
                    [html.Div([
                        html.Br(),
                        html.H5(f'Parameter {i+1}'),
                        html.Div([dcc.Input(id=f'input{i}{j}', type='number', placeholder=minmax[j+1],
                                            persistence=True, persistence_type='memory') for j in range(2)])]) for i in range(n)]) 
            

        @self.app.callback(Output(component_id="live_GP", component_property="figure"), 
                    Input('graph-update', 'n_intervals'))   
        def update_graphGP(n):
            figure_update = updateLiveGP(self, config)
            return figure_update
                

        # @self.app.callback(Output(component_id="live_Acq", component_property="figure"), 
        #               Input('graph-update', 'n_intervals'))   
        # def update_graphACQ(n):
            # updateAcq = updateAcvqGraph(self, config)
            # return updateAcq

    
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
            update_figureParmIter = updateParmIterationGraph(self, n_parm)
            return update_figureParmIter


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
                reset(self)
        
    
                

        
