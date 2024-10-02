# Importa las bibliotecas necesarias
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Lista de estaciones meteorológicas identificadas por sus códigos.
stations = ['78526', '72566', '04301', '94328', '64753']

# Lista de variables meteorológicas que se pueden visualizar.
variables = ['tavg', 'tmin', 'tmax', 'prcp', 'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun']

# Inicializa aplicación Dash
app = Dash(__name__)

# Configuración del diseño de la aplicación.
app.layout = html.Div([
    html.Div(children='Dash con datos de Meteostat'),  # Título
    html.Hr(),  

    # Menú para seleccionar una estación.
    dcc.Dropdown(id='station-dropdown', options=[{'label': i, 'value': i} for i in stations], value=stations[0]),

    # Menú para seleccionar la variable meteorológica
    dcc.Dropdown(id='variable-dropdown', options=[{'label': i, 'value': i} for i in variables], value='tavg'),
    dcc.Graph(id='time-series-chart')
])

# Callback para actualizar la grafica
@callback(
    Output('time-series-chart', 'figure'),
    [Input('station-dropdown', 'value'),
     Input('variable-dropdown', 'value')]
)
def update_graph(selected_station, selected_variable):
    data_url = f'https://cdat.uprh.edu/~eramos/data/{selected_station}.csv'
    df = pd.read_csv(data_url, header=None, names=['date', 'tavg', 'tmin', 'tmax', 'prcp', 'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun'])

    # Crea la grafica de líneas
    fig = px.line(df, x='date', y=selected_variable, title=f'Station {selected_station} - {selected_variable}')
    fig.update_layout(title_x=0.5)
    return fig

# Ejecuta la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
