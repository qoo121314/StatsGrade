import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os

def fetch_group_name(data,student,Score1,Score2,new):
    data[new]=np.zeros(len(data.index))
    for name, group in data.groupby([Score1,Score2]):
        data.loc[data[data[Score1]==name[0]][data[Score2]==name[1]][new].index,new]=str(" ".join(group[student].values))
    return data

def bubble_dict(dictionary , dataframe):
    keys=list(dictionary.keys())
    values=list(dictionary.values())
    values.pop()
    values.insert(0, dataframe.columns[3])
    
    bubbledict=dict(zip(keys, values))
    
    return bubbledict


df = pd.read_csv('grade.csv')

option_dict ={  i:i for i in df.columns[3:]}
bubble_dict= bubble_dict(option_dict,df)


if os.path.exists('bubblegrade.h5'):
    data=pd.read_hdf('bubblegrade.h5',key='data')
else:
    for i in df.columns[3:]:
        fetch_group_name(df,df.columns[0],i,bubble_dict[i],i+bubble_dict[i])
    h5 = pd.HDFStore('bubblegrade.h5','w')
    h5['data'] = df
    df = pd.read_csv('grade.csv')
    h5.close()
