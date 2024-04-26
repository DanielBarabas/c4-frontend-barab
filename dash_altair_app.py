import pandas as pd
import dash
from dash import dcc, html
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import query
from config import load_config_iam
import os


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
            id="cat-dropdown1",
            options=[
                {"label": category, "value": category} for category in category_options
            ],
            value="Sex & Nudity",
            clearable=False,
        ),
        dcc.Dropdown(
            id="level-dropdown1",
            options=[
                {"label": severity, "value": severity} for severity in severity_options
            ],
            value="Severe",
            clearable=False,
        ),
        dcc.Dropdown(
            id="cat-dropdown2",
            options=[
                {"label": category, "value": category} for category in category_options
            ],
            value="Profanity",
            clearable=False,
        ),
        dcc.Dropdown(
            id="level-dropdown2",
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
    [
        Input("cat-dropdown1", "value"),
        Input("level-dropdown1", "value"),
        Input("cat-dropdown2", "value"),
        Input("level-dropdown2", "value"),
    ],
)
def update_graph(selected_cat1, selected_level1, selected_cat2, selected_level2):
    df_to_plot = query.query_plot_two_criteria(
        [selected_cat1, selected_level1, selected_cat2, selected_level2]
    )

    if type(df_to_plot) == str:
        return html.Div(df_to_plot)
    df_to_plot.to_csv("data/trial.csv")
    chart = (
        alt.Chart(df_to_plot)
        .mark_bar()
        .encode(
            x=alt.X("category", axis=None), y="rate", color="category", column="series"
        )
        .properties(
            width=200,
            height=300,
            title=f"Rates for {selected_level1} {selected_cat1} and {selected_level2}{selected_cat2}",
        )
        .configure_title(fontSize=20, anchor="middle")
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
    # Use the PORT environment variable if available, otherwise default to 8080
    port = int(os.environ.get("PORT", 8080))
    app.run_server(host="0.0.0.0", port=port)
