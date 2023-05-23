# import dash
# from dash import html, dcc, ctx
# from dash.dependencies import Input, Output, State
# from flask import Flask
# from dash.dependencies import Input, Output
# import requests


# class app:
#     def __init__(self):
#         self.app = dash.Dash(__name__)
#         self.app.layout = html.Div([
#             html.H1('Print data on terminal'),
#             html.Button('print', id='button'),
#             html.Div(id='output'),
#             html.Div(id='update'),
#             dcc.Interval(id='trigger', interval= 500)
#         ])
#         self.data = {}

#         @self.app.callback(Output('output', 'children'), 
#                         [Input('button', 'n_clicks')])
#         def run_script(n_clicks):
#             if "button" == ctx.triggered_id:
#                 print(self.data['polar ECG'])
#                 # print(self.data['Change_parm'])
#                 #print(self.data['plot_data_GP'])
                
#                 return 'data printed'
            
#         @self.app.callback(Output('update', 'children'),
#                         Input('trigger', 'n_intervals'))
#         def update_server(n):
#             if n is not None:
#                 self.data = requests.get('http://127.0.0.1:5000/OptimizationData').json()

            

import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import dash
from dash import html, dcc


ranges = [0.0, 0.85]

parm1 = [0.18, 0.52, 0.32, 0.14, 0.75]
parm2 = [0.72, 0.84, 0.12, 0.05, 0.37]
parm3 = [0.1, 0.55, 0.32, 0.7, 0.85]
parm4 = [0.4, 0.08, 0.2, 0.34, 0.65]
parm5 = [0.0, 0.85, 0.54, 0.0, 0.85]
parm6 = [0.85, 0.0, 0.23, 0.0, 0.85]

cost = [-10, -21, -25, -32, -14]


opacity = np.interp(parm3, (np.min(ranges), np.max(ranges)), (0.2, 1.0))
size = np.interp(parm4, (np.min(ranges), np.max(ranges)), (2, 12))
normalized_green = [(value - min(ranges)) / (max(ranges) - min(ranges)) for value in parm5]
normalized_blue = [(value - min(ranges)) / (max(ranges) - min(ranges)) for value in parm6]
colors = ['rgb({}, {}, {})'.format(0, int(255 * (green)), int(255 * (blue))) for green, blue in zip(normalized_green, normalized_blue)]

hover_info = [[f'parm1: {x}<br>parm2: {y}<br>parm3: {fv}<br>parm4: {sv}<br>parm5: {tv}<br>parm6: {uv}<br>cost: {z}']
              for x, y, fv, sv, tv, uv, z in zip(parm1, parm2, parm3, parm4, parm5, parm6, cost)]

samples= []
for i in range(len(parm1)):
    sample = go.Scatter3d(x=np.array(parm1[i]),y=np.array(parm2[i]),z=np.array(cost[i]),
        mode='markers',
        showlegend=False,
        marker=dict(color=colors[i],opacity=opacity[i],size=size[i]),
        hovertemplate='%{customdata}', 
        customdata=hover_info[i]
    )
    samples.append(sample)

layout = go.Layout(scene=dict(xaxis_title='param1',yaxis_title='param2',zaxis_title='Cost'))
fig = go.Figure(data=samples, layout=layout)

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
