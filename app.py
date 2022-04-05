import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# our imports
from text_samples import GRAFICOS_NUNO

# Dataset loading
df = pd.read_csv('superstore.csv', encoding = "ISO-8859-1")

# Dataset 'Processing'

df['Year'] = pd.to_datetime(df['Ship Date']).dt.year # added a year column for easier data sorting
df.drop(df.index[df['Year'] == 2018], inplace = True) # 2018 has incomplete data, so we drop the whole year

# Sales and Profit chart
df_3bar = df.filter(['Sub-Category', 'Sales', 'Discount', 'Profit'], axis=1)
df_3bar['DiscountMoney'] = df_3bar['Discount'] * df_3bar['Sales']
del df_3bar['Discount']
df_3bar.rename(columns={'DiscountMoney':'Discount'}, inplace=True)
df_graph = df_3bar.groupby(['Sub-Category']).sum().reset_index()

# Lineplot profit by category by year
df_lineplot = df.filter(['Year', 'Category', 'Profit'], axis=1)
df_lineorganized = df_lineplot.groupby(['Year', 'Category'], as_index=False)['Profit'].sum()
dummies = pd.get_dummies(df_lineorganized['Category']).mul(df_lineorganized.Profit,0)
dummies['Year'] = df_lineorganized['Year']
df_linegraph = dummies.groupby(['Year']).sum().reset_index()

# Building our Graphs (nothing new here)
sales_profit_fig = px.bar(df_graph, x="Sub-Category", y=["Sales", "Profit"], barmode="group").update_layout(legend_title="Type")
lineplot_profit_fig = px.line(df_linegraph, x="Year", y=['Furniture', 'Office Supplies', 'Technology']).update_xaxes(dtick=1).update_layout(legend_title="Category")

stacked = px.histogram(df, x="Segment", y="Profit", color="Category", hover_data=['Segment'], barmode='stack')

pie = px.pie(df, values='Profit', names='Segment')

# The App itself
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1(children='Projeto something'),
    html.Div([
        html.Div([GRAFICOS_NUNO], style={'float': 'left', 'width': '19%'}),
        html.Div([
            html.Div([
                html.Div([GRAFICOS_NUNO]),
                html.Div([
                    html.H3('Sales and Profit Graph'),
                    dcc.Graph(id='g1', figure=sales_profit_fig)
                ], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([
                    html.H3('Yearly Profit Graph'),
                    dcc.Graph(id='g2', figure=lineplot_profit_fig)
                ], style={'width': '48%', 'display': 'inline-block'}),
            ])], style={'float': 'right', 'width': '80%'}),

        html.Div([
            html.Div([
                html.Div([GRAFICOS_NUNO]),
                html.Div([
                    html.H3('Stacked'),
                    dcc.Graph(id='g3', figure=stacked)
                ], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([
                    html.H3('Pie'),
                    dcc.Graph(id='g4', figure=pie)
                ], style={'width': '48%', 'display': 'inline-block'}),
            ])], style={'float': 'right', 'width': '80%'})

    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
