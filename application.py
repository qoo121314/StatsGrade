import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

def fetch_group_name(data,student,Score1,Score2,new):
    data[new]=np.zeros(len(data.index))
    for name, group in data.groupby([Score1,Score2]):
        data.loc[data[data[Score1]==name[0]][data[Score2]==name[1]][new].index,new]=str(" ".join(group[student].values))
    return data[[student,data.columns[1],new]]

def bubble_dict(dictionary , dataframe):
    keys=list(dictionary.keys())
    values=list(dictionary.values())
    values.pop()
    values.insert(0, dataframe.columns[2])
    
    bubbledict=dict(zip(keys, values))
    
    return bubbledict


df = pd.read_csv('grade1.csv')

option_dict ={  i:i for i in df.columns[2:]}
bubble_dict= bubble_dict(option_dict,df)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                meta_tags=[
                    {'name': "viewport",
                    'content': "width=500",
                    'initial-scale': 1}
                ])
application = app.server

app.layout=html.Div([
    
    html.Div([html.H1('張翔統計學小考成績')],  
    style={
            'textAlign': 'center'
        }),
    
    html.Div([
    
    dcc.Dropdown(id='season',
        options=[dict(label=i ,value=i) 
                for i in df.columns[2:]
        ],
        value=df.columns[-1]
    )],style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Dropdown(id='graph_type',
        options=[
            {'label': '盒鬚圖', 'value': '盒鬚圖'},
            {'label': '氣泡圖', 'value': '氣泡圖'},
            {'label': '成績表', 'value': '成績表'}
        ],
        value='盒鬚圖'
        )],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

    dcc.Graph(id='output-graph'),    
    html.Div([
    html.Pre(id='hover-data', style={'paddingTop':35})
    ], style={'width':'30%'})
],style={'padding':10}
)

@app.callback(
    Output('output-graph', 'figure'),
    [Input('season', 'value'),
    Input('graph_type', 'value')]
)
def update_output_div(input_season,graph_type):
    if graph_type == '盒鬚圖':
        return {
        'data':[go.Box(y=df[input_season], name= region ) for region in df[df.columns[1]].unique() ],

        'layout': go.Layout (title=input_season+"   "+graph_type)}
    elif graph_type == '氣泡圖':
            return {
        'data':[go.Scatter(
            x=df[df[df.columns[1]]==region][bubble_dict[input_season]],
            y=df[df[df.columns[1]]==region][input_season], 
            name= region,
            mode='markers',
            text= fetch_group_name(df,df.columns[0],input_season,bubble_dict[input_season],'RN')[df[df.columns[1]]==region]['RN']
            ,opacity=0.5,
            )
            for region in df[df.columns[1]].unique() ],

        'layout': go.Layout (title=input_season+"   "+graph_type,
                            xaxis=dict(title=bubble_dict[input_season]+'成績'),
                            yaxis=dict(title=input_season+'成績'),
                                hovermode='closest')}
    elif graph_type == '成績表':
        return {'data':[go.Table(header=dict(values=[df.columns[0],df.columns[1],input_season]),
                        cells=dict(values=[
                            df[[df.columns[0],df.columns[1],input_season]].dropna().sort_values(by=[input_season],ascending=False)[df.columns[0]],
                            df[[df.columns[0],df.columns[1],input_season]].dropna().sort_values(by=[input_season],ascending=False)[df.columns[1]],
                            df[[df.columns[0],df.columns[1],input_season]].dropna().sort_values(by=[input_season],ascending=False)[input_season]
                       ]),)]
        }

if __name__ == '__main__':
    application.run
