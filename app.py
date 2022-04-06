import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
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

sub_categories = ['Bookcases', 'Chairs', 'Labels', 'Tables', 'Storage',
       'Furnishings', 'Art', 'Phones', 'Binders', 'Appliances', 'Paper',
       'Accessories', 'Envelopes', 'Fasteners', 'Supplies', 'Machines',
       'Copiers']

# State name to code
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

df['State'] = df['State'].map(lambda x: us_state_to_abbrev[x])

# list of state codes

states_codes = sorted(df['State'].unique())

################################################RadioitemComponent#############################################################

sub_categories_options = [dict(label=sub_category.replace('_', ' '), value=sub_category) for sub_category in sub_categories]

radio_interaction = dcc.RadioItems(
        id='interaction',
        options=sub_categories_options,
        value='Bookcases',
        labelStyle={'display': 'block'}
    )

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
        html.Div([html.Div([GRAFICOS_NUNO], style={'text-align':'justify', 'white-space': 'pre-wrap'})], style={'float': 'left', 'width': '19%'}),
        html.Div([
            html.Div([
                html.Div([html.Label('Product Sub-Categories'), radio_interaction], style={'width': "20%"}),
                html.Div([dcc.Graph(id='choropleth_graph')], style={'width': "80%"})], style={'display': 'flex'}),
            html.Div([
                html.H3('Sales and Profit Graph'),
                html.Div([html.Div([GRAFICOS_NUNO], style={'text-align':'justify', 'white-space': 'pre-wrap'})]),
                dcc.Graph(id='bar_charts', figure=sales_profit_fig)
            ]),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Yearly Profit Graph'),
                            html.Div([html.Div([GRAFICOS_NUNO], style={'text-align':'justify', 'white-space': 'pre-wrap'})]),
                            dcc.Graph(id='g1', figure=lineplot_profit_fig)
                        ], style={'width': '48%', 'display': 'inline-block'}),
                        html.Div([
                            html.H3('Sunburst, or something...'),
                            html.Div([html.Div([GRAFICOS_NUNO], style={'text-align':'justify', 'white-space': 'pre-wrap'})]),
                            dcc.Graph(id='g2', figure=lineplot_profit_fig)
                        ], style={'width': '48%', 'display': 'inline-block'})])]),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Stacked'),
                            html.Div([html.Div([GRAFICOS_NUNO], style={'text-align':'justify', 'white-space': 'pre-wrap'})]),
                            dcc.Graph(id='g3', figure=stacked)
                        ], style={'width': '48%', 'display': 'inline-block'}),
                        html.Div([
                            html.H3('Pie'),
                            html.Div([html.Div([GRAFICOS_NUNO], style={'text-align':'justify', 'white-space': 'pre-wrap'})]),
                            dcc.Graph(id='g4', figure=pie)
                        ], style={'width': '48%', 'display': 'inline-block'}),
                    ])])

            ])
        ], style={'float': 'right', 'width': '80%'})

    ])
])

##############################################callback#############################################################################

@app.callback(
    Output('choropleth_graph', 'figure'),
    Input('interaction', 'value')
)

##############################################Graph################################################################################


# Building Choropleth Graph
def plot(subgroup):

    # I have to query the data to get only the sub_categories I want!!!!!

    df_map = df.groupby(["Sub-Category", "State"]).sum("Quantity")["Quantity"]

    d = dict.fromkeys(states_codes, 0)
    z = dict(df_map[subgroup])

    for key in z:
        d[key] = z[key]
    result = pd.Series(d)


    data_choropleth = dict(type='choropleth',
                           locations=states_codes,
                           #There are three ways to 'merge' your data with the data pre embedded in the map
                           locationmode='USA-states',
                           z=result.astype(float),
                           colorscale='Reds',
                           colorbar=dict(title='Product Quantity')
                          )

    layout_choropleth = dict(geo=dict(scope='usa'),
                             title=dict(text='United States Map of Purchases',
                                        x=.5 # Title relative position according to the xaxis, range (0,1)
                                       )
                            )

    fig = go.Figure(data=data_choropleth, layout=layout_choropleth)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
