import dash
from dash import html, dcc, ctx
from dash.dependencies import Input, Output, State
from flask import Flask
from dash.dependencies import Input, Output
import requests


class app:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.app.layout = html.Div([
            html.H1('Print data on terminal'),
            html.Button('print', id='button'),
            html.Div(id='output'),
            html.Div(id='update'),
            dcc.Interval(id='trigger', interval= 500)
        ])
        self.data = {}

        @self.app.callback(Output('output', 'children'), 
                        [Input('button', 'n_clicks')])
        def run_script(n_clicks):
            if "button" == ctx.triggered_id:
                print(self.data['polar ECG'])
                # print(self.data['Change_parm'])
                #print(self.data['plot_data_GP'])
                
                return 'data printed'
            
        @self.app.callback(Output('update', 'children'),
                        Input('trigger', 'n_intervals'))
        def update_server(n):
            if n is not None:
                self.data = requests.get('http://127.0.0.1:5000/OptimizationData').json()

            

main = app()
if __name__ == '__main__':
            main.app.run_server(debug=True, port = 8080) # host='0.0.0.0')