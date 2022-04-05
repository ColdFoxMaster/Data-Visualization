import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go

# Dataset 'Processing'

df = pd.read_csv('superstore.csv', encoding='ISO-8859-1')

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

#################################################APP_LAYOUT####################################################################

app = dash.Dash(__name__)

server = app.server


# I have to do the app layout!!!!!!!

app.layout = html.Div([

    html.Div([
        html.H1('SuperStore'),
    ]),

    html.Div([
        html.Div([
            html.Label('Product Sub-Categories'),
            radio_interaction
        ], style={'width': "20%"}),

        html.Div([
            dcc.Graph(id='choropleth_graph')
        ], style={'width': "80%"})
    ], style={'display': 'flex'})
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
                             title=dict(text='World Choropleth Map',
                                        x=.5 # Title relative position according to the xaxis, range (0,1)
                                       )
                            )

    fig = go.Figure(data=data_choropleth, layout=layout_choropleth)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)