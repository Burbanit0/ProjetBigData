# Imports 
import seaborn as sns 
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go 

import dash
from dash import dcc
from dash import html 

# Source of data 
df = pd.read_csv('./33000-BORDEAUX_nettoye.csv')
df['prix_personne'] = df['PrixNuitee']/df['Capacite_accueil']

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]


if __name__ == '__main__':
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    # Figure 1: Heat map of price in Bordeaux
    fig1 = px.density_mapbox(df, lat='Latitude', lon='Longitude', z='prix_personne', radius=10,
                            center=dict(lat=44.84, lon=-0.562), zoom=13,
                            mapbox_style="open-street-map", range_color=[15,40])
  
    # Figure 2: Price per person
    fig2 = px.histogram(df, x='prix_personne')


    app.layout = html.Div(children = [
        html.Div([
            html.H1(children = f'Repartition des prix selon la localisation', style={'textAlign': 'center', 'color':'blue'}),
            dcc.Graph(id='HeatMap',figure=fig1),
        ]),
        html.Div([
            html.H1(children= f'Repartition du prix par personne', style={'textAlign': 'center', 'color':'blue'}),
            dcc.Graph(id='Repartition', figure=fig2),
        ]),
])    

app.run_server(debug=True) 