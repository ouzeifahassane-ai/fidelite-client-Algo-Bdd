import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_data():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    df = pd.read_sql("SELECT * FROM scoring_clients", conn)
    conn.close()
    return df

df = get_data()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Fidélité Client", style={'textAlign': 'center', 'color': '#2c3e50'}),

    # KPIs
    html.Div([
        html.Div([html.H3("Total Clients"), html.H2(len(df))], className='kpi'),
        html.Div([html.H3("Score Moyen"), html.H2(round(df['score_fidelite'].mean(), 1))], className='kpi'),
        html.Div([html.H3("Clients Gold"), html.H2(len(df[df['segment']=='Gold']))], className='kpi'),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px'}),

    # Filtre
    html.Div([
        html.Label("Filtrer par segment :"),
        dcc.Dropdown(
            id='filtre-segment',
            options=[{'label': s, 'value': s} for s in df['segment'].unique()],
            value=None,
            placeholder="Tous les segments",
            clearable=True
        )
    ], style={'width': '40%', 'margin': '20px auto'}),

    # Graphiques
    html.Div([
        dcc.Graph(id='graph-segments'),
        dcc.Graph(id='graph-points'),
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'})
])

@app.callback(
    Output('graph-segments', 'figure'),
    Output('graph-points', 'figure'),
    Input('filtre-segment', 'value')
)
def update_graphs(segment):
    filtered = df if segment is None else df[df['segment'] == segment]

    fig1 = px.pie(filtered, names='segment', title='Répartition par segment',
                  color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'})

    fig2 = px.bar(filtered.sort_values('score_fidelite', ascending=False),
                  x='nom', y='score_fidelite', color='segment',
                  title='Score de fidélité par client',
                  color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'})

    return fig1, fig2

if __name__ == '__main__':
    app.run(debug=True)