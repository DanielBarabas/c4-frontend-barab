import pandas as pd
import dash
from dash import dcc, html
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from dash.exceptions import PreventUpdate
from plotly.graph_objects import Figure, Bar
from dash import callback
import dash_bootstrap_components as dbc
import altair as alt
import query


category_options = [
    "Sex & Nudity",
    "Violence & Gore",
    "Profanity",
    "Alcohol, Drugs & Smoking",
    "Frightening & Intense Scenes",
]
severity_options = ["Severe", "Moderate", "Mild"]


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Top 5 highest consensus rate on parental reviews"),
        dcc.Dropdown(
            id="cat-dropdown",
            options=[
                {"label": category, "value": category} for category in category_options
            ],
            value="Sex & Nudity",
            clearable=False,
        ),
        dcc.Dropdown(
            id="level-dropdown",
            options=[
                {"label": severity, "value": severity} for severity in severity_options
            ],
            value="Severe",
            clearable=False,
        ),
        html.Div(id="altair-chart"),
    ]
)


@app.callback(
    Output("altair-chart", "children"),
    [Input("cat-dropdown", "value"), Input("level-dropdown", "value")],
)
def update_graph(selected_cat, selected_level):
    query_result = query.query_plot([selected_cat, selected_level])

    if type(query_result) == str:
        return html.Div(query_result)

    df_to_plot = pd.DataFrame(query_result)
    df_to_plot.columns = ["title", "rate"]

    chart = (
        alt.Chart(df_to_plot)
        .mark_bar()
        .encode(x=alt.X("title", sort="ascending"), y="rate", tooltip=["title", "rate"])
        .properties(
            width="container",
            height=400,
            title=f"Rates for {selected_cat} - {selected_level}",
        )
        .interactive()
    )

    return html.Div(
        [
            html.Iframe(
                sandbox="allow-scripts",
                id="plot",
                height="600px",
                width="100%",
                style={"border-width": "0"},
                srcDoc=chart.to_html(),
            )
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
