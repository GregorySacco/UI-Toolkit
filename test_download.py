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

import numpy as np
import dash
from dash import html, dcc


import plotly.graph_objects as go
import numpy as np

# Generazione dei dati di esempio
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))
A = np.cos(X)
B = np.sin(Y)
C = np.cos(X*Y)
D = np.sin(X/Y)

data = []
# Creazione del plot di superficie
data1=go.Surface(
        x=X, y=Y, z=Z,
        surfacecolor=A,  # Colore in base ad A
        colorscale='Viridis',
        cmin=np.min(A),
        cmax=np.max(A),
        name='A',
        showscale=False
    )
data.append(data1)
data2 = go.Surface(
        x=X, y=Y, z=Z,
        surfacecolor=B,  # Colore in base a B
        colorscale='Reds',
        cmin=np.min(B),
        cmax=np.max(B),
        name='B',
        showscale=False
    ),
data.append(data2)
data3 = go.Surface(
        x=X, y=Y, z=Z,
        surfacecolor=D,  # Colore in base a D
        colorscale='Blues',
        cmin=np.min(D),
        cmax=np.max(D),
        name='D',
        showscale=False
    ),
data.append(data3)

data4 = go.Surface(
        x=X, y=Y, z=Z,
        surfacecolor=C,  # Colore in base a C
        colorscale='Greens',
        cmin=np.min(C),
        cmax=np.max(C),
        name='C',
        showscale=False
    )
data.append(data4)
print(data)
# data = [[data1], [data2], [data3], [data4]]

fig = go.Figure(data)

# Layout del grafico
fig.update_layout(
    title='Superficie in 7 dimensioni',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        aspectmode='cube'
    )
)

# Visualizzazione del grafico
fig.show()


