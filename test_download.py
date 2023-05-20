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

            

# main = app()
# if __name__ == '__main__':
#             main.app.run_server(debug=True, port = 8080) # host='0.0.0.0')

# import matplotlib.pyplot as plt
# import numpy as np

# # Dati delle tre variabili
# x = [1, 2, 3, 4, 5]
# y = [2, 4, 1, 5, 3]
# z = [3, 1, 5, 2, 4]
# data= []

# # Valori della quarta variabile per l'opacità
# fourth_variable = [1, 2, 3, 4, 5]

# # Valori della quinta variabile per la dimensione dei puntini
# fifth_variable = [1, 2, 3, 4, 5]

# # Normalizzazione della quarta variabile tra 0 e 1 per l'opacità
# opacity = np.interp(fourth_variable, (np.min(fourth_variable), np.max(fourth_variable)), (0.1, 1.0))
# print(opacity[0])

# # Normalizzazione della quinta variabile per la dimensione dei puntini
# size = np.interp(fifth_variable, (np.min(fifth_variable), np.max(fifth_variable)), (10, 100))

# # Creazione del grafico 3D
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Rappresentazione dei punti con opacità e dimensione dei puntini basate sulle variabili
# for i in range(len(x)):

#     scatter = ax.scatter(x[i], y[i], z[i], c='b', alpha=opacity[i], s=size[i])


# # Etichette degli assi
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')

# # Visualizzazione del grafico
# plt.show()

import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import dash
from dash import html, dcc

x = [[1], [2], [3], [4], [5]]
y = [[2], [4], [1], [5], [3]]
z = [[3], [1], [5], [2], [4]]

fourth_variable = [1, 5, 2, 4, 3]
fifth_variable = [4, 1, 2, 3, 5]

opacity = np.interp(fourth_variable, (np.min(fourth_variable), np.max(fourth_variable)), (0.1, 1.0))

size = np.interp(fifth_variable, (np.min(fifth_variable), np.max(fifth_variable)), (2, 12))

traces= []
for i in range(len(x)):
    trace = go.Scatter3d(x=list(x[i]),y=list(y[i]),z=list(z[i]),
        mode='markers',
        showlegend=False,
        marker=dict(
            color='blue',
            opacity=opacity[i],
            size=size[i]
        )
    )
    traces.append(trace)

layout = go.Layout(scene=dict(xaxis_title='X',yaxis_title='Y',zaxis_title='Z'))

fig = go.Figure(data=traces, layout=layout)

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)

