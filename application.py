import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np


df = pd.read_csv('grade1.csv')

bubble_dict={'暑期第一次小考':'暑期第一次小考','暑期第二次小考':'暑期第一次小考','暑期第三次小考':'暑期第二次小考'}

def fetch_group_name(data,student,Score1,Score2,new):
    df['RN']=np.zeros(100)
    for name, group in data.groupby([Score1,Score2]):
        data.loc[data[data[Score1]==name[0]][data[Score2]==name[1]][new].index,new]=str(" ".join(group[student].values))
    return data

def textname(text,name):
    if text is None:
        text = name
    else:
        text.append(name)
    return text

app=dash.Dash()

app.layout=html.Div([
    
    html.Div([html.H1('張翔統計學小考成績')],  
    style={
            'textAlign': 'center'
        }),
    
    html.Div([
    
    dcc.Dropdown(id='season',
        options=[
            {'label': '暑期第一次小考', 'value': '暑期第一次小考'},
            {'label': '暑期第二次小考', 'value': '暑期第二次小考'},
            {'label': '暑期第三次小考', 'value': '暑期第三次小考'}
        ],
        value='暑期第一次小考'
    )],style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Dropdown(id='graph_type',
        options=[
            {'label': '盒鬚圖', 'value': '盒鬚圖'},
            {'label': '氣泡圖', 'value': '氣泡圖'}
        ],
        value='盒鬚圖'
        )],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

    dcc.Graph(id='output-graph'),    
    html.Div([
    html.Pre(id='hover-data', style={'paddingTop':35})
    ], style={'width':'30%'})

],style={'padding':10})

@app.callback(
    Output('output-graph', 'figure'),
    [Input('season', 'value'),
    Input('graph_type', 'value')]
)
def update_output_div(input_season,graph_type):
    if graph_type == '盒鬚圖':
        return {
        'data':[go.Box(y=df[input_season], name= region ) for region in df['班級'].unique() ],

        'layout': go.Layout (title=input_season+"   "+graph_type)}
    elif graph_type == '氣泡圖':
            return {
        'data':[go.Scatter(
            x=df[df['班級']==region][bubble_dict[input_season]],
            y=df[df['班級']==region][input_season], 
            name= region,
            mode='markers',
            text= fetch_group_name(df,'姓名',input_season,bubble_dict[input_season],'RN')[df['班級']==region]['RN']#待釐清,
            ,opacity=0.5,
            )
            for region in df['班級'].unique() ],

        'layout': go.Layout (title=input_season+"   "+graph_type,
                            xaxis=dict(title=bubble_dict[input_season]+'成績'),
                            yaxis=dict(title=input_season+'成績'),
                                hovermode='closest')
    }

if __name__=='__main__':
    app.run_server(debug=True)
