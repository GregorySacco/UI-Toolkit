import numpy as np
import math
import plotly.graph_objects as go
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import matplotlib as mpl
import matplotlib.pyplot as plt

data=[-28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023, -28.184850692749023]

n = len(data)
matrix_size = int(math.sqrt(n))
matrix_data = [data[i:i+matrix_size] for i in range(0, n, matrix_size)]
nx,ny = (30,30)
x = np.linspace(0,85, nx)
y= np.linspace(0,85, ny)
xv, yv = np.meshgrid(x,y)

x_scale_ratio = 0.7  # Rapporto di scala per l'asse x (cambia come desiderato)
y_scale_ratio = 0.7  # Rapporto di scala per l'asse y (cambia come desiderato)
z_scale_ratio = 0.15  # Rapporto di scala per l'asse z (cambia come desiderato)

fig = go.Figure(data=[go.Surface(x=x, y=y, z=matrix_data)],
                layout=go.Layout(scene=dict(xaxis_title='Parameter 1',
                                            yaxis_title='Parameter 2',
                                            zaxis_title='Cost',
                                            aspectmode='manual',
                                            aspectratio=dict(x=x_scale_ratio,
                                                             y=y_scale_ratio,
                                                             z=z_scale_ratio)),
                                 width=800,
                                 margin=dict(r=10, b=40, l=100, t=20)))

fig.show()
