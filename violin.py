import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

df = pd.read_csv('superstore.csv', encoding='ISO-8859-1')

sub_categories = ['Bookcases', 'Chairs', 'Labels', 'Tables', 'Storage',
                  'Furnishings', 'Art', 'Phones', 'Binders', 'Appliances', 'Paper',
                  'Accessories', 'Envelopes', 'Fasteners', 'Supplies', 'Machines',
                  'Copiers']

plot = ['Violin', 'Boxplot']

sub_categories_options = [dict(label=sub_category.replace('_', ' '), value=sub_category) for sub_category in
                          sub_categories]

plot_options = [dict(label=sub_category.replace('_', ' '), value=sub_category) for sub_category in plot]

dropdown_sub_category = dcc.Dropdown(
    id='sub_category_option',
    options=sub_categories_options,
    value='Bookcases',
)

dropdown_plot = dcc.Dropdown(
    id='plot_options',
    options=plot_options,
    value='Violin',
)

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.P("Select the Sub-Category", style={"text-align": "center", "font-weight": "bold"}),
    dropdown_sub_category,
    dropdown_plot,
    dcc.Graph(id="boxes")
])


@app.callback(
    Output('boxes', 'figure'),
    [Input("plot_options", "value"), Input("sub_category_option", "value")],
)
def plot(plot_type, sub_category):
    cons = df.loc[(df["Segment"] == "Consumer") & (df["Sub-Category"] == sub_category)]["Sales"].round(2)
    corp = df.loc[(df["Segment"] == "Corporate") & (df["Sub-Category"] == sub_category)]["Sales"].round(2)
    home = df.loc[(df["Segment"] == "Home Office") & (df["Sub-Category"] == sub_category)]["Sales"].round(2)

    trace0 = go.Box(
        y=cons,
        name="Consumer",
        boxpoints=False
    )

    trace1 = go.Box(
        y=corp,
        name="Corporate",
        boxpoints=False
    )

    trace2 = go.Box(
        y=home,
        name="Home Office",
        boxpoints=False
    )
    if plot_type == "Violin":
        trace0 = go.Violin(
            y=cons,
            name="Consumer",

        )

        trace1 = go.Violin(
            y=corp,
            name="Corporate",

        )

        trace2 = go.Violin(
            y=home,
            name="Home Office",

        )

    data = [trace0, trace1, trace2]
    layout = go.Layout(title='Distribution of sales by customer type and Sub-Category')

    fig = go.Figure(data=data, layout=layout)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
